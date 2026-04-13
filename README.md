👷‍♂️ Agentic Vision: Otonom İSG Denetim AjanıModel Context Protocol (MCP) tabanlı, LLM güdümlü otonom güvenlik denetim sistemi.📖 Proje HakkındaAgentic Vision, standart bir nesne tespiti projesinden çok daha fazlasıdır. Bu sistem, Claude 3.5 Sonnet gibi gelişmiş Büyük Dil Modellerine (LLM) gerçek dünyayı görme, yorumlama ve aksiyon alma yeteneği kazandıran bir "Yapay Zeka Ajanı" mimarisidir.🧠 Neden "Agentic"?Sistem sadece bir görüntüdeki nesneleri saymaz; Model Context Protocol (MCP) kullanarak yerel dosya sistemini aktif olarak tarar, en güncel kamera kaydını kendisi seçer, analiz API'sini tetikler ve elde ettiği sonuçları 6331 sayılı İş Sağlığı ve Güvenliği Kanunu çerçevesinde profesyonel bir rapora dönüştürerek Supabase veritabanına kalıcı olarak işler.🏗️ Sistem MimarisiAşağıdaki şema, uçtan uca veri akışını ve ajan tabanlı iş akışını göstermektedir:graph TD
    User([👤 Kullanıcı]) -->|Soru: İSG kontrolü yap| Claude[🧠 Claude 3.5 Sonnet]
    Claude -->|MCP Tool Call| MCP_Server{⚙️ MCP Server}
    MCP_Server -->|Otonom Dosya Tarama| Local_Storage[(📁 images/ Folder)]
    MCP_Server -->|POST /analyze| FastAPI[🚀 FastAPI Backend]
    FastAPI -->|Inference Request| Roboflow((☁️ Roboflow Cloud API))
    FastAPI -->|Log Kaydı| Supabase[(🗄️ Supabase DB)]
    Roboflow -.->|Tespit Verisi| FastAPI
    FastAPI -.->|JSON Result| MCP_Server
    MCP_Server -.->|Rapor Verisi| Claude
    Claude -->|Dinamik Dashboard Raporu| User
✨ Öne Çıkan Özellikler🤖 Otonom Keşif: Ajanın, dosya yoluna ihtiyaç duymadan en güncel kaydı kendisinin bulması.👁️ Yüksek Doğruluk: YOLOv8 mimarisi ile eğitilmiş modeller üzerinden baret ve yelek tespiti.💾 Kurumsal Hafıza: Her denetimin anlık olarak PostgreSQL (Supabase) üzerine loglanması.📜 Mevzuat Entegrasyonu: Ham verilerin İSG hukukuna uygun rapor formatına dönüştürülmesi.🔌 MCP Standartları: Anthropic'in en yeni Model Context Protocol standartlarına tam uyum.🚀 Kurulum ve Başlatma1. Ortam Hazırlığı# Repo'yu klonlayın
git clone [https://github.com/fatihberkanteren/agentic-vision-server.git](https://github.com/fatihberkanteren/agentic-vision-server.git)
cd agentic-vision-server

# Sanal ortam oluşturun
conda create -n agentic-vision python=3.10 -y
conda activate agentic-vision
pip install -r requirements.txt
2. Yapılandırma (.env)Ana dizinde bir .env dosyası oluşturun ve aşağıdaki anahtarları girin:ROBOFLOW_API_KEY=...
SUPABASE_URL=...
SUPABASE_KEY=...
3. Servisleri BaşlatınTerminal 1 (Backend API):uvicorn main:app --reload
Terminal 2 (MCP Server):python mcp_server.py
⚙️ Claude Desktop EntegrasyonuClaude Desktop uygulamasında bu ajanı aktif etmek için claude_desktop_config.json dosyanıza aşağıdaki sunucu tanımını ekleyin:{
  "mcpServers": {
    "agentic-vision": {
      "command": "C:/path/to/python.exe",
      "args": ["C:/path/to/agentic-vision-server/mcp_server.py"]
    }
  }
}
Not: Windows kullanıcıları dosya yollarında / yerine \\ kullanabilir veya yolların doğruluğundan emin olmalıdır.📈 Kullanım ÖrneğiSistem hazır olduğunda Claude'a şu komutu vermeniz yeterlidir:"Saha kameralarını kontrol et, bir ihlal varsa acil rapor oluştur."Sonuç: Claude arka planda analyze_image_for_safety aracını çalıştırır, images/ klasöründeki son fotoğrafı analiz eder ve size bareti/yeleği olmayan personelin listesini, güven skorlarını ve veritabanı kayıt teyidini sunar.👨‍💻 GeliştiriciFatih Berkant ERENLinkedInGitHubBu proje, Model Context Protocol (MCP) ve Agentic AI kavramlarını endüstriyel senaryolarda test etmek amacıyla geliştirilmiştir.
