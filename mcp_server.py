import os
import glob
import json
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AgenticVisionServer")
VISION_API_URL = "http://localhost:8000/analyze"

@mcp.tool()
async def check_latest_camera_record() -> str:
    """
    Sistemdeki 'images' klasörüne bakar, en son şantiye kamera kaydını bulur ve analiz için İSG API'sine gönderir.
    
    Bilgi: Arka plandaki API (FastAPI), analiz sonuçlarını her çalışmada otonom olarak Supabase veritabanına kaydetmektedir.
    
    Görev: API'den dönen JSON sonucunu tarafsızca incele. Eğer API sonuçlarında baret veya yelek eksikliği ('no_helmet', 'no_vest') 
    tespit edilmişse, bu durumu vurgulayan bir İSG raporu sun.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "images") 
        
        image_files = glob.glob(os.path.join(images_dir, "*.jpg")) + glob.glob(os.path.join(images_dir, "*.png"))
        
        if not image_files:
            return "Sistem Mesajı: 'images' klasöründe incelenecek herhangi bir kamera kaydı bulunamadı."
            
        latest_image_path = max(image_files, key=os.path.getctime)
        file_name = os.path.basename(latest_image_path)
        
        with open(latest_image_path, "rb") as f:
            files = {"file": (file_name, f, "image/jpeg")}
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(VISION_API_URL, files=files)
                
        if response.status_code == 200:
            result = response.json()
            return f"İncelenen Dosya: {file_name}\nAnaliz Başarılı:\nÖzet: {result['summary']}\nDetaylı Tespitler: {json.dumps(result['detections'], indent=2)}\nNot: Bu veriler API tarafından Supabase'e işlenmiştir."
        else:
            return f"API Hatası: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Beklenmeyen bir hata oluştu: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')