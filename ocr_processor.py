# ocr_processor.py

import cv2
import numpy as np
import pytesseract
import requests
from PIL import Image
from io import BytesIO
import config
import os
import json
import concurrent.futures # Library untuk Multi-threading
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OCRProcessor:
    """
    Class OCR Cerdas dengan fitur:
    1. Caching (Menyimpan hasil agar tidak download ulang).
    2. Multi-threading (Download paralel).
    3. Retry Mechanism (Tahan banting koneksi buruk).
    """
    
    CACHE_FILE = 'ocr_cache.json'

    def __init__(self):
        # 1. Setup Tesseract
        try:
            pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
        except Exception as e:
            print(f"🚨 ERROR: Config Tesseract salah: {e}")

        # 2. Setup Session dengan Retry (Anti-Gagal)
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        # 3. Load Cache (Agar hemat kuota & waktu)
        self.cache = self._load_cache()
        print(f"-> OCR Processor siap. {len(self.cache)} data tersimpan di cache.")

    def _load_cache(self):
        """Membaca file cache jika ada."""
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_cache_entry(self, video_id, density_score):
        """Menyimpan satu entri ke file JSON (Checkpointing)."""
        self.cache[video_id] = density_score
        # Kita append/rewrite file json (Untuk performa tinggi, idealnya di akhir batch, 
        # tapi untuk keamanan data, kita save sering-sering).
        with open(self.CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f)

    def analyze_thumbnail_text_density(self, image_url: str, video_id: str = None) -> float:
        """
        Versi Cerdas: Cek Cache dulu, baru download jika belum ada.
        """
        # 1. Cek Cache (Hemat Resource)
        if video_id and video_id in self.cache:
            # Jika sudah pernah diproses, kembalikan nilai lama. Skip download!
            return self.cache[video_id]

        if not image_url:
            return 0.0

        try:
            # 2. Download Gambar (Pakai Session yang stabil)
            response = self.session.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content))
            
            # 3. Proses OCR
            text_result = pytesseract.image_to_string(img, lang='ind+eng')
            
            # 4. Hitung Density
            clean_text = ''.join(filter(str.isalnum or str.isspace, text_result)).lower()
            words = clean_text.split()
            density = len(set(words)) # Jumlah kata unik
            
            # 5. Simpan ke Cache jika ada ID
            if video_id:
                self._save_cache_entry(video_id, density)
                
            return density
        
        except Exception as e:
            # Jangan print error berlebihan agar log bersih, cukup return 0
            return 0.0

    def process_batch_concurrently(self, video_data_list: list, max_workers=5):
        """
        [BARU] Memproses ribuan video secara PARALEL.
        Jauh lebih cepat daripada loop biasa.
        """
        print(f"\n🚀 Memulai OCR Batch Processing untuk {len(video_data_list)} video...")
        print(f"   Mode: {max_workers} Threads (Parallel)")
        
        count_processed = 0
        
        # Fungsi pembantu untuk thread
        def process_item(video_item):
            vid_id = video_item.get('id')
            url = video_item.get('thumbnail')
            # Panggil fungsi analisis (otomatis cek cache)
            density = self.analyze_thumbnail_text_density(url, vid_id)
            return vid_id, density

        # Eksekusi Paralel
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit semua tugas
            future_to_video = {executor.submit(process_item, vid): vid for vid in video_data_list}
            
            for future in concurrent.futures.as_completed(future_to_video):
                vid_id, density = future.result()
                count_processed += 1
                if count_processed % 10 == 0:
                    print(f"   -> Progress: {count_processed}/{len(video_data_list)} (Cache/OCR OK)")
                    
        print("✅ OCR Batch Selesai.")