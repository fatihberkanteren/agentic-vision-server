from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import httpx
import base64
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI(
    title="Agentic Vision API - İSG (Cloud Inference)",
    description="İş Sağlığı ve Güvenliği için bulut tabanlı yapay zeka görüş sunucusu.",
    version="1.0.0"
)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# API Bilgileri
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
MODEL_ENDPOINT = "ppe-fruwx/5"

@app.get("/")
async def root():
    return {"message": "İSG Sistemi (Bulut API) Ayakta! Test için /docs adresine gidin."}

def log_to_supabase(filename, summary, detections):
    """Tespit sonuçlarını veritabanına kaydeder."""
    # Eğer 'no_helmet' veya 'no_vest' varsa ihlal olarak işaretle
    has_violation = any(d['class_name'] in ['no_helmet', 'no_vest'] for d in detections)
    
    data = {
        "filename": filename,
        "summary": summary,
        "detection_details": detections,
        "violation_found": has_violation
    }
    
    # Supabase'e gönder
    supabase.table("isg_logs").insert(data).execute()

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Görüntüyü buluttaki modele (Inference API) gönderip sonucu döner."""
    
    # 1. Görüntüyü Base64 formatına çevir (Roboflow API'sinin beklediği format)
    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode("ascii")
    
    # 2. Doğru URL'yi oluştur
    upload_url = f"https://detect.roboflow.com/{MODEL_ENDPOINT}?api_key={ROBOFLOW_API_KEY}"
    
    # 3. Asenkron HTTP isteğini at
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            upload_url,
            data=image_b64,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
    # 4. Hata kontrolü
    if response.status_code != 200:
        return JSONResponse(
            content={"error": f"API Hatası: {response.text}"}, 
            status_code=500
        )
        
    api_result = response.json()
    
    # 5. Roboflow'un yanıtını ayrıştır
    detections = []
    class_counts = {}
    
    for prediction in api_result.get("predictions", []):
        class_name = prediction["class"]
        confidence = prediction["confidence"]
        
        # Sınıfları say (Örn: 2 baret, 1 yelek)
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        # Merkez (x,y) formatından Kutu (x_min, y_min, x_max, y_max) formatına çevir
        x_min = prediction["x"] - (prediction["width"] / 2)
        y_min = prediction["y"] - (prediction["height"] / 2)
        x_max = prediction["x"] + (prediction["width"] / 2)
        y_max = prediction["y"] + (prediction["height"] / 2)
        
        detections.append({
            "class_name": class_name,
            "confidence": round(confidence, 2),
            "bbox": [round(x_min, 1), round(y_min, 1), round(x_max, 1), round(y_max, 1)]
        })

    # 6. Dinamik özet oluştur
    summary_text = ", ".join([f"{count} adet {name}" for name, count in class_counts.items()])
    if not summary_text:
        summary_text = "Hiçbir İSG donanımı tespit edilemedi."

    log_to_supabase(file.filename, summary_text, detections)
    
    return JSONResponse(content={
        "filename": file.filename,
        "summary": summary_text,
        "detections": detections
    })
