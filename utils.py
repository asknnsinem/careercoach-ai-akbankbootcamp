import fitz  # PyMuPDF
import tempfile
import os
import time

def safe_remove(path):
    """Windows dosya kilidi sorunlarını önlemek için güvenli silme."""
    for _ in range(3):
        try:
            if os.path.exists(path):
                os.remove(path)
            return
        except PermissionError:
            time.sleep(0.5)
    print(f"⚠️ Dosya silinemedi (kilitli olabilir): {path}")

def extract_text_from_pdf(uploaded_file):
    """PDF'den doğrudan metin çıkarımı (fitz ile)."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        tmp_pdf_path = tmp_pdf.name

    text = ""
    try:
        doc = fitz.open(tmp_pdf_path)
        for page in doc:
            # 'blocks' metotları tablo ve layout'larda daha kararlı
            page_text = page.get_text("text")
            if isinstance(page_text, list):
                page_text = " ".join(page_text)
            text += page_text
        doc.close()
    except Exception as e:
        print("⚠️ PDF metin çıkarımı hatası:", e)
        text = ""
    finally:
        safe_remove(tmp_pdf_path)

    return text.strip()
