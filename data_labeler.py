# data_labeler.py

import json
import pandas as pd
import numpy as np
import sys
import os

# Mengimpor modul OCR
# Pastikan ocr_processor.py sudah diperbarui dengan fitur threading!
try:
    from ocr_processor import OCRProcessor
except ImportError:
    print("🚨 ERROR: ocr_processor.py tidak ditemukan. Pastikan file ada di folder yang sama.")
    sys.exit(1)

# --- Konfigurasi File ---
INPUT_FILE = 'raw_shorts_data.json'
OUTPUT_FILE_CSV = 'shorts_training_data.csv'

# Threshold untuk pelabelan (Bisa disesuaikan)
SUCCESS_PERCENTILE = 75 

def process_and_label_data():
    """Memuat data mentah, menjalankan OCR Batch, menghitung WPI, dan melabeli data."""
    
    # 1. Muat Data Mentah (JSON)
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        df = pd.DataFrame(raw_data)
        print(f"-> Berhasil memuat {len(df)} baris data mentah.")
    except FileNotFoundError:
        print(f"🚨 ERROR: File {INPUT_FILE} tidak ditemukan. Jalankan data_collector.py terlebih dahulu.")
        return
        
    # Pastikan Views numeric & handle NaN
    df['views'] = pd.to_numeric(df['views'], errors='coerce').fillna(0)
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0)
    df['comments'] = pd.to_numeric(df['comments'], errors='coerce').fillna(0)
    
    # Hapus baris dengan views nol atau terlalu sedikit (sampah)
    df = df[df['views'] > 100].copy()
    
    # ====================================================================
    # 2. PROSES OCR (BATCH PARALLEL PROCESSING) - BAGIAN BARU
    # ====================================================================
    print("\n[MULAI EKSTRAKSI FITUR VISUAL (OCR)]")
    try:
        ocr = OCRProcessor()
        
        # Siapkan data untuk threading (butuh ID dan URL Thumbnail)
        video_list_dict = df[['id', 'thumbnail']].to_dict('records')
        
        # Jalankan Download & OCR secara Paralel (8 Threads)
        # Ini akan otomatis mengecek Cache dulu, jadi hemat kuota
        ocr.process_batch_concurrently(video_list_dict, max_workers=8)
        
        print("-> Menggabungkan hasil OCR ke DataFrame...")
        
        # Ambil nilai density dari cache OCR dan masukkan ke kolom baru
        # Jika gagal/kosong, isi dengan 0.0
        df['ocr_text_density'] = df['id'].apply(lambda x: ocr.cache.get(x, 0.0))
        
        print(f"✅ OCR Selesai. Kolom 'ocr_text_density' berhasil ditambahkan.")
        
    except Exception as e:
        print(f"⚠️ WARNING: Gagal menjalankan OCR. Menggunakan nilai default 0.0. Error: {e}")
        df['ocr_text_density'] = 0.0
    # ====================================================================

    
    # 3. Hitung Metrik Kinerja (WPI & Engagement)
    
    # Engagement Rate (ER)
    df['engagement_rate'] = (df['likes'] + df['comments']) / df['views']
    
    # WPI (Weighted Performance Index)
    df['wpi_score'] = df['engagement_rate'] * 1000 # Scaling score
    
    
    # 4. Pelabelan Data (Target Variabel y)
    
    # Tentukan ambang batas WPI
    threshold = df['wpi_score'].quantile(SUCCESS_PERCENTILE / 100)
    print(f"\n-> Threshold WPI untuk [SUCCESS]: {threshold:.4f}")
    
    # Lakukan pelabelan: 1 jika di atas threshold, 0 jika di bawah.
    df['is_success'] = np.where(df['wpi_score'] >= threshold, 1, 0)
    
    
    # 5. Filter dan Simpan Data Akhir
    final_df = df.copy()
    
    # Statistik Label
    success_count = final_df['is_success'].sum()
    failure_count = len(final_df) - success_count
    
    print(f"\n[HASIL PELABELAN]")
    print(f"SUCCESS (Label 1): {success_count} data ({success_count / len(final_df) * 100:.2f}%)")
    print(f"FAILURE (Label 0): {failure_count} data")
    print(f"Total Data Siap: {len(final_df)}")
    
    # PENTING: Pastikan kolom OCR ikut tersimpan di CSV
    cols_to_save = ['id', 'title', 'tags', 'views', 'engagement_rate', 'wpi_score', 'ocr_text_density', 'is_success']
    
    # Hanya simpan kolom yang benar-benar ada (defensif)
    existing_cols = [c for c in cols_to_save if c in final_df.columns]
    
    final_df[existing_cols].to_csv(OUTPUT_FILE_CSV, index=False, encoding='utf-8')
    print(f"✅ Data Training Riil berhasil disimpan di: {OUTPUT_FILE_CSV}")

if __name__ == "__main__":
    process_and_label_data()