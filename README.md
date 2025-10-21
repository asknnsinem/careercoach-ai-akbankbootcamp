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
3️⃣ Sanal Ortam Oluşturma
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
4️⃣ Dataset Kurulumu
```bash
#data klasörü oluşturulmuş olmalı
python dataset_download.py
``` 
 
5️⃣ Uygulamayı Çalıştırma
```bash
streamlit run app.py
```

🧩 Çözüm Mimarisi
```bash
📄 CV veya metin girişi
     ↓
🌍 Çeviri (Türkçe → İngilizce)
     ↓
🔍 Embedding çıkarımı
     ↓
🧠 Chroma veritabanında benzer ilan arama
     ↓
🤖 Gemini API (değerlendirme, özet, skor, öneriler)
     ↓
💬 Streamlit arayüzünde sonuçların gösterimi

```
## 🧠 RAG mimarisi:
- **Retriever** → Top-5 ilanları getirir
- **Augmenter** → Bu ilanları LLM’e (Gemini) gönderir
- **Generator** → LLM cevabını JSON formatında üretir ve UI’ye döner

## 🌐 Web Arayüzü

Arayüz Özellikleri:

- 📎 PDF CV yükleme veya metin girişi

- 🎯 Hedef pozisyon girme (opsiyonel)

- 🧮 Uygunluk yüzdesi + AI değerlendirmesi

- 🔍 Pozisyon Önerisi

Demo Linki:
🔗 (örnek) https://careercoach-ai.streamlit.app


## 🏁 Katkıda Bulunanlar

Geliştirici:
- **👤 Sinem Aşkın**
- **📧 askinnsinem@gmail.com**
- **🏫 Akbank GenAI Bootcamp — 2025**

