👷‍♂️ Agentic Vision: Otonom İSG Denetim Ajanı 🚀

Model Context Protocol (MCP) + YOLOv8 + FastAPI + Supabase

Bu proje, Büyük Dil Modellerine (LLM) gerçek dünyayı görme, yorumlama ve aksiyon alma yeteneği kazandıran, Model Context Protocol (MCP) tabanlı otonom bir İş Sağlığı ve Güvenliği (İSG) denetim sistemidir.

🌟 Neden Agentic Vision?

Standart nesne tespiti projelerinden farklı olarak bu sistem, bir "Agentic Workflow" üzerine inşa edilmiştir. LLM sadece bir sonuç üretmez; yerel dosya sistemini tarar, API'leri tetikler ve elde ettiği veriyi yasal mevzuat (6331 Sayılı İSG Kanunu) çerçevesinde anlamlandırarak kurumsal hafızaya (Database) kaydeder.

✨ Öne Çıkan Özellikler

🤖 Otonom Karar Alma: LLM'in dosya sistemindeki en güncel kamera kaydını kendisinin bulup analiz etmesi.

⚡ Hızlı Analiz (Inference): YOLOv8 tabanlı mimari ile yüksek doğrulukta baret ve yelek tespiti.

📊 Akıllı Raporlama: Ham JSON verisinden profesyonel, okunabilir İSG denetim raporları üretme.

🛡️ Güvenli Loglama: Tespit edilen her ihlalin anlık olarak Supabase PostgreSQL üzerine işlenmesi.

🏗️ Sistem Mimarisi

graph TD
    A[Claude Desktop / LLM] -->|MCP Request| B(MCP Server - FastMCP)
    B -->|Scan Images| C{Local Storage}
    B -->|POST /analyze| D[FastAPI Backend]
    D -->|Inference Request| E((Roboflow Cloud API))
    E -->|JSON Result| D
    D -->|Insert Log| F[(Supabase DB)]
    D -->|Formatted Result| B
    B -->|Agentic Report| A


🚀 Hızlı Başlangıç

1. Depoyu Klonlayın

git clone [https://github.com/fatihberkanteren/agentic-vision-server.git](https://github.com/fatihberkanteren/agentic-vision-server.git)
cd agentic-vision-server


2. Bağımlılıkları Kurun

conda create -n agentic-vision python=3.10 -y
conda activate agentic-vision
pip install -r requirements.txt


3. Çevre Değişkenleri (.env)

Proje ana dizininde bir .env dosyası oluşturun:

ROBOFLOW_API_KEY=your_api_key
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_service_key


⚙️ Claude Desktop Entegrasyonu

Claude Desktop ayarlarınızdaki (claude_desktop_config.json) mcpServers kısmına aşağıdaki bloğu ekleyin:

{
  "mcpServers": {
    "agentic-vision": {
      "command": "C:/path/to/your/python.exe",
      "args": ["C:/path/to/your/project/mcp_server.py"]
    }
  }
}


Not: Windows kullanıcıları python.exe ve mcp_server.py için tam dosya yolunu (Absolute Path) kullanmalıdır.

🎯 Örnek Çıktı (Demo)

Sisteme tek bir komut vermeniz yeterlidir:

"Saha kameralarını kontrol et, İSG ihlali varsa raporla."

Sistem Yanıtı:

Dosya

Bölge

İhlal Türü

Güven Skoru

kamera_04.jpg

Bölge B

Baret Eksik (no_helmet)

%92

👨‍💻 Geliştirici

Fatih Berkant EREN - LinkedIn | GitHub
