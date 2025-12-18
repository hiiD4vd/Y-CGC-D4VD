# data_collector.py

import json
from data_fetcher import DataFetcher
from core.video_case import VideoCase
import config
import sys
import os
import time

# Memastikan proyek bisa menemukan modul
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# --- KONFIGURASI PENGUMPULAN ---
OUTPUT_FILE = 'raw_shorts_data.json'
KEYWORD_FILE = 'keywords.json'
VIDEOS_PER_QUERY = 10 


# --- DAFTAR 250 KEYWORDS LENGKAP ---
# Niche: Pengembangan Diri, Life Hacks, Soft Skills, Sains Populer

def load_keywords():
    """Membaca daftar keyword dari file eksternal JSON."""
    try:
        with open(KEYWORD_FILE, 'r', encoding='utf-8') as f:
            keywords = json.load(f)
            print(f"-> Berhasil memuat {len(keywords)} keywords dari {KEYWORD_FILE}")
            return keywords
    except FileNotFoundError:
        print(f"🚨 ERROR: File {KEYWORD_FILE} tidak ditemukan!")
        return []
    except json.JSONDecodeError:
        print(f"🚨 ERROR: Format JSON di {KEYWORD_FILE} rusak!")
        return []


def collect_raw_data():
    fetcher = DataFetcher()
    all_raw_data = []
    
    # 1. Load Keywords dari File (Bukan Hardcode)
    keywords_list = load_keywords()
    
    if not keywords_list:
        return

    TARGET_TOTAL = len(keywords_list) * VIDEOS_PER_QUERY
    print(f"-> Target Data: {TARGET_TOTAL} Shorts...")
    
    for i, keyword in enumerate(keywords_list):
        print(f"   [{i+1}/{len(keywords_list)}] Mencari: '{keyword}'")
        
        # --- PERBAIKAN STABILITAS: JEDA WAKTU ---
        # Beri napas sedikit agar tidak dianggap spam oleh YouTube
        # Tidur 1 detik setiap request
        time.sleep(1) 
        
        try:
            video_list = fetcher.search_youtube_videos(keyword, max_results=VIDEOS_PER_QUERY)
            
            if video_list:
                for video in video_list:
                    all_raw_data.append({
                        'id': video.video_id,
                        'title': video.title,
                        'tags': video.raw_tags,
                        'views': video.raw_views,
                        'likes': video.raw_likes,
                        'comments': video.raw_comments,
                        'thumbnail': video.thumbnail_url # Pastikan ini tersimpan untuk OCR nanti
                    })
                print(f"     ✅ Dapat {len(video_list)} video.")
            else:
                print(f"     ⚠️ Nihil.")
                
        except Exception as e:
            print(f"     ❌ Error pada keyword ini: {e}")
    
    # Menyimpan ke file JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_raw_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Data mentah berhasil disimpan di {OUTPUT_FILE}")


if __name__ == "__main__":
    collect_raw_data()