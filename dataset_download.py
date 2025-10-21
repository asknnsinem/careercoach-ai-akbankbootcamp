from datasets import load_dataset
import pandas as pd

print("📦 Dataset indiriliyor...")

dataset = load_dataset("xanderios/linkedin-job-postings")    
df = pd.DataFrame(dataset["train"])
print("Kolonlar:", df.columns.tolist())

# Gerekirse title/description sütun adlarını kontrol et
# örnek: df.rename(columns={'jobtitle':'title', 'jobdescription':'description'}, inplace=True)

df.to_csv("data/job_postings.csv", index=False, encoding="utf-8-sig")
print("✅ Dataset indirildi ve kaydedildi: data/job_postings.csv")
print(f"Toplam kayıt sayısı: {len(df)}")
