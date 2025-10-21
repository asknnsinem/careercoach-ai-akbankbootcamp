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

## 🧾 Kullanılan Datasetler

### 1️⃣ [LinkedIn Job Postings Dataset](https://huggingface.co/datasets/xanderios/linkedin-job-postings)
- Kaynak: Hugging Face  
- İçerik: Gerçek LinkedIn iş ilanlarından toplanan başlık, açıklama, konum ve sektör bilgileri.  
- Boyut: ~3.2M satır  
- Kullanım:  
  - **Yalnızca yazılım geliştirici / mühendislik ilanları** filtrelendi.  
  - `build_vector_db()` fonksiyonu bu ilanları vektör embedding'e dönüştürerek `Chroma` veritabanına kaydetti.  
  - RAG pipeline’ı bu ilanları kullanarak kullanıcının CV’sine en benzer 5 ilanı seçiyor.  

---

### 2️⃣ [Sentence-Transformers: Paraphrase Multilingual MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- Tür: Çok dilli embedding modeli  
- Rolü: CV ve iş ilanı metinlerinin **vektör temsillerini** oluşturur  
- Avantajı: Türkçe dahil 50+ dil desteği  
- Kullanım: LangChain `HuggingFaceEmbeddings` aracılığıyla çağrılır.  

---

### 3️⃣ [facebook/m2m100_418M](https://huggingface.co/facebook/m2m100_418M)
- Tür: Çok dilli çeviri modeli  
- Rolü: Türkçe CV’leri İngilizceye çevirerek Gemini modeline gönderir  
- Kullanım:  
  - `translate_to_en()` fonksiyonu içinde çağrılır.  
  - `src_lang = "tr"` → `en` dönüşümü yapılır.  

---

## 🌐 Web Arayüzü

Arayüz Özellikleri:

- 📎 PDF CV yükleme veya metin girişi

- 🎯 Hedef pozisyon girme (opsiyonel)

- 🧮 Uygunluk yüzdesi + AI değerlendirmesi

- 🔍 Pozisyon Önerisi

Demo Linki:
🔗 (örnek) https://careercoach-ai.streamlit.app

## 📊 Örnek Çıktı

🎯 Pozisyon: Yazılım Mühendisi
📊 Uyum: %82
🧠 Değerlendirme:

Adayın yazılım geliştirme tecrübesi güçlü. Ancak bulut teknolojileri (AWS, GCP) tarafında daha fazla deneyim kazanması faydalı olur.

💼 Önerilen Pozisyonlar:

Backend Developer

Python Engineer

Full Stack Developer

## 🏁 Katkıda Bulunanlar

Geliştirici:
- **👤 Sinem Aşkın**
- **📧 askinnsinem@gmail.com**
- **🏫 Akbank GenAI Bootcamp — 2025**

