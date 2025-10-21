import streamlit as st
from utils import extract_text_from_pdf
from rag_pipeline import build_vector_db, query_rag
import os

if not os.path.exists("data/job_postings.csv"):
    with st.spinner("📦 Dataset indiriliyor..."):
        import dataset_download
st.set_page_config(page_title="KariyerKoçu AI", page_icon="💼")

# -------------------------------
# 🔹 Başlık ve Açıklama
# -------------------------------
st.title("💼 KariyerKoçu AI — CV & Uyum Analizi (Yapay Zekâ Destekli)")
st.write(
    "CV’nizi yükleyin veya metin olarak girin. "
    "Pozisyon girerseniz o pozisyona göre değerlendirme yapılır; "
    "boş bırakırsanız sistem genel ilanlar üzerinden analiz yapar. "
    "Değerlendirme gemini-2.5-pro tarafından yapılır."
)

# -------------------------------
# 🔹 Kullanıcı Girdileri
# -------------------------------
uploaded_file = st.file_uploader("📄 CV yükle (PDF)", type=["pdf"])
cv_text_input = st.text_area("✍️ CV metni (PDF yüklemezseniz buraya yazın)")
job_title = st.text_input("🎯 Hedef pozisyon (ör: Software Developer, Data Engineer)")

# -------------------------------
# 🔹 Vektör DB Oluşturma
# -------------------------------
if st.button("🔍 Vektör Veritabanını Hazırla"):
    if not os.path.exists("chroma_software_jobs"):
        with st.spinner("Veritabanı hazırlanıyor... (ilk defa yapılıyor)"):
            build_vector_db()
        st.success("✅ Vektör veritabanı oluşturuldu!")
    else:
        st.info("ℹ️ Veritabanı zaten hazır, yeniden oluşturmaya gerek yok.")

# -------------------------------
# 🔹 Analiz Başlatma
# -------------------------------
if uploaded_file or cv_text_input:
    if st.button("🚀 Analiz Et (Yapay Zekâ ile)"):
        with st.spinner("Yapay zekâ analizi yapılıyor, lütfen bekleyin..."):
            cv_text = extract_text_from_pdf(uploaded_file) if uploaded_file else cv_text_input
            result = query_rag(cv_text, job_title)

        st.subheader("📊 Uygunluk Skoru")
        score = result.get("match_percentage", 0)
        st.progress(score / 100)
        st.write(f"**{score}% Ortalama Uyum**")

        st.subheader("🧠 Değerlendirme (Yapay Zekâ Yorumu)")
        st.write(result.get("summary_tr", "Değerlendirme oluşturulamadı."))

        st.subheader("💼 Önerilen Pozisyonlar")
        suggested = result.get("suggested_jobs", [])
        if suggested:
            for job in suggested:
                st.markdown(f"- {job}")
        else:
            st.info("Henüz önerilen pozisyon bulunamadı.")
else:
    st.info("📎 CV yükleyin veya metin girin, ardından 'Analiz Et' butonuna basın.")
