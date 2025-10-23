import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# ---------------------------------------------------------
# 🔹 Ortam değişkenlerini yükle
# ---------------------------------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------------------------------------------------
# 🔹 Çeviri modeli (Türkçe → İngilizce)
# ---------------------------------------------------------
model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

def translate_to_en(text: str):
    if not isinstance(text, str) or text.strip() == "":
        return ""
    tokenizer.src_lang = "tr"
    encoded = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id("en"))
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

# ---------------------------------------------------------
# 🔹 Vektör veritabanı oluşturma
# ---------------------------------------------------------
def build_vector_db():
    """Tüm ilanlardan embedding tabanı oluşturur (filtre yok)."""
    df = pd.read_csv("data/job_postings.csv")

    # Sadece gerekli sütunları al
    if "title" in df.columns and "description" in df.columns:
        df = df[["title", "description"]].dropna()
    else:
        raise ValueError(f"⚠️ Beklenen kolonlar bulunamadı. Mevcut kolonlar: {df.columns.tolist()}")

    # İlan metinlerini birleştir
    texts = [f"Title: {t}\nDescription: {d}" for t, d in zip(df["title"], df["description"])]

    # Embedding modeli
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    # Chroma veritabanını oluştur
    db = Chroma.from_texts(texts, embedding=embeddings, persist_directory="./chroma_jobs")
    db.persist()

    print(f"✅ {len(df)} ilan Chroma veritabanına kaydedildi.")
    return db


# ---------------------------------------------------------
# 🔹 CV Karşılaştırma (Gemini)
# ---------------------------------------------------------
def query_rag(cv_text, job_title=None):
    """Kullanıcının CV'si ve (isteğe bağlı) pozisyon başlığına göre en alakalı ilanları bulur ve Gemini ile değerlendirir."""
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    db = Chroma(persist_directory="./chroma_software_jobs", embedding_function=embeddings)

    # 1️⃣ CV + başlığı tek metin haline getir
    query_text = f"{job_title or ''} {cv_text}"

    # 2️⃣ Bu metnin embedding'ini çıkar
    query_emb = embeddings.embed_query(query_text)

    # 3️⃣ En benzer 5 ilanı getir
    results = db.similarity_search_by_vector(query_emb, k=5)
    postings = "\n\n".join([r.page_content for r in results])

    # 4️⃣ Gemini modeli
    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = f"""
Aşağıda bir adayın özgeçmişi (CV) ve benzer iş ilanları verilmiştir.
Senin görevin:
- Adayın becerilerini ve deneyimini değerlendir.
- İlanlardaki gereksinimlerle karşılaştır.
- Genel uyum oranını tahmin et (0–100).
- Türkçe kısa bir özet oluştur (güçlü yönler, geliştirmesi gerekenler).
- En uygun 3 pozisyonu öner.

---
🧑‍💼 CV + Başlık:
{cv_text}

💼 Benzer İlanlar:
{postings}

---
Cevabını tam JSON formatında döndür:
{{
  "match_percentage": <oran>,
  "summary_tr": "<türkçe özet>",
  "suggested_jobs": ["Pozisyon 1", "Pozisyon 2", "Pozisyon 3"]
}}
"""

    # 5️⃣ Gemini'ye gönder
    response = model.generate_content(prompt)

    try:
        text_output = (
            response.text
            if hasattr(response, "text")
            else response.candidates[0].content.parts[0].text
        )
        start = text_output.find("{")
        end = text_output.rfind("}") + 1
        json_str = text_output[start:end]
        data = json.loads(json_str)

    except Exception as e:
        print("⚠️ JSON ayrıştırma hatası:", e)
        print("🔎 Modelden gelen ham çıktı:", text_output if 'text_output' in locals() else str(response))
        data = {
            "match_percentage": 0,
            "summary_tr": "Model yanıtını düzgün biçimde çözemedi.",
            "suggested_jobs": []
        }

    data["match_percentage"] = max(0, min(float(data.get("match_percentage", 0)), 100))
    return data
