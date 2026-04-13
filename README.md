👷‍♂️ Agentic Vision: Otonom İSG Denetim Ajanı (MCP + YOLOv8 + Supabase)
Bu proje, Büyük Dil Modellerine (LLM) gerçek dünyayı "görme", "yorumlama" ve "aksiyon alma" yeteneği kazandıran, Model Context Protocol (MCP) tabanlı otonom bir İş Sağlığı ve Güvenliği (İSG) denetim sistemidir.

Standart nesne tespiti projelerinden farkı, bir "Agentic Workflow" (Ajan Tabanlı İş Akışı) üzerine inşa edilmiş olmasıdır. Claude 3.5 Sonnet, sistemdeki kamera kayıtlarını otonom olarak bulur, analiz ettirir ve İSG mevzuatına göre risk raporu üretir.

🚀 Öne Çıkan Özellikler
Model Context Protocol (MCP): LLM'in yerel dosya sistemine ve özel API'lere güvenli erişimi.

Otonom Analiz: "images" klasörüne düşen son görüntüyü otomatik tespit ve analiz etme.

Akıllı Raporlama: Ham JSON verisini 6331 sayılı İSG Kanunu'na göre anlamlı bir rapora dönüştürme.

Kurumsal Hafıza: Tüm ihlallerin anlık olarak Supabase (PostgreSQL) veritabanına loglanması.

Modern Mimari: FastAPI (Asenkron) + Roboflow (Cloud Inference).

🛠️ Sistem Mimarisi
Kod snippet'i
graph TD
    A[Claude Desktop / LLM] -->|MCP Request| B(MCP Server - FastMCP)
    B -->|Scan Images| C{Local Storage}
    B -->|POST /analyze| D[FastAPI Backend]
    D -->|Inference Request| E((Roboflow Cloud API))
    E -->|JSON Result| D
    D -->|Insert Log| F[(Supabase DB)]
    D -->|Formatted Result| B
    B -->|Agentic Report| A
📦 Kurulum
Depoyu Klonlayın:

Bash
git clone https://github.com/fatihberkanteren/agentic-vision-server.git
cd agentic-vision-server
Ortamı Hazırlayın (Conda/Venv):

Bash
conda create -n agentic-vision python=3.10 -y
conda activate agentic-vision
pip install -r requirements.txt
Çevre Değişkenlerini Ayarlayın:.env dosyası oluşturun ve bilgilerinizi girin:

Plaintext
ROBOFLOW_API_KEY=your_api_key
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_service_key
⚙️ Claude Desktop Entegrasyonu
Claude Desktop ayarlarınızdaki (claude_desktop_config.json) mcpServers kısmına şunu ekleyin:

JSON
{
  "mcpServers": {
    "agentic-vision": {
      "command": "C:/path/to/your/python.exe",
      "args": ["mcp_server.py"]
    }
  }
}
🎯 Kullanım Senaryosu
Sistem ayağa kalktıktan sonra Claude'a şu komutu vermeniz yeterlidir:

"Saha kameralarını kontrol et, İSG ihlali varsa raporla ve veritabanına logla."

Ajan, images/ klasöründeki son fotoğrafı bulacak, bareti/yeleği eksik personeli tespit edecek ve size profesyonel bir denetim raporu sunacaktır.