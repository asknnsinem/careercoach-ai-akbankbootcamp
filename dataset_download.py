from datasets import load_dataset
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

print("📦 Dataset indiriliyor...")

# Verisetini indir (sadece ilk 3000 kayıt)
dataset = load_dataset("xanderios/linkedin-job-postings", split="train[:2000]")

# Pandas DataFrame'e dönüştür
df = pd.DataFrame(dataset)

print("Kolonlar:", df.columns.tolist())

# Gerekirse kolon isimlerini düzenle
# df.rename(columns={'jobtitle': 'title', 'jobdescription': 'description'}, inplace=True)

# CSV olarak kaydet
output_path = "data/job_postings.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ Dataset indirildi ve kaydedildi: {output_path}")
print(f"Toplam kayıt sayısı: {len(df)}")
