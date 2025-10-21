# 💼 KariyerKoçu AI — CV & Uyum Analizi  
### 🚀 Akbank GenAI Bootcamp Projesi  

KariyerKoçu AI, yapay zekâ destekli bir **özgeçmiş (CV) değerlendirme ve iş ilanı uyumluluk analiz** uygulamasıdır.  
Kullanıcı, PDF veya metin formatında CV’sini yükleyip bir pozisyon belirttiğinde sistem, **vektör tabanlı arama (RAG)** ve **Gemini LLM** kullanarak adayın iş ilanlarına olan uygunluğunu değerlendirir.

---

## 🧠 Proje Özeti  

- **Amaç:** CV içeriğini analiz ederek iş ilanlarına uygunluk oranını hesaplamak.  
- **Teknoloji:** RAG (Retrieval-Augmented Generation) + Google Gemini  
- **Girdi:** Kullanıcının CV’si (PDF/metin) ve opsiyonel hedef pozisyon  
- **Çıktı:**  
  - 📊 Uyum yüzdesi (0–100 arası)  
  - 💬 Türkçe özet (güçlü yönler & geliştirme önerileri)  
  - 💼 3 önerilen pozisyon  

---

## 🧩 Mimarisi  

```bash
kariyerkocu-ai/
├── app.py                 # Streamlit arayüzü
├── rag_pipeline.py        # RAG + Gemini analiz fonksiyonları
├── utils.py               # PDF → Word → Metin dönüşüm yardımcı fonksiyonları
├── data/
│   └── job_postings.csv   # İş ilanı veriseti
├── chroma_software_jobs/  # Vektör veritabanı (otomatik oluşturulur)
├── .env                   # GEMINI_API_KEY burada saklanır
└── requirements.txt       # Bağımlılıklar listesi
```

⚙️ Kurulum Rehberi
## 1️⃣ Depoyu klonla

```bash
git clone https://github.com/asknnsinem/careercoach-ai-akbankbootcamp.git
cd kariyerkocu-ai-akbankbootcamp
```

2️⃣ Ortam Değişkenleri (.env)
Proje kök dizinine bir .env dosyası oluşturun:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```
