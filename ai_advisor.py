# ai_advisor.py - MODUL KECERDASAN BUATAN (GEMINI 2.5)

import google.generativeai as genai
import config
import json

class AIAdvisor:
    def __init__(self):
        # Cek API Key
        if not config.GEMINI_API_KEY:
            print("⚠️ GEMINI_API_KEY belum diisi di .env!")
            self.model = None
            return
            
        # Konfigurasi Gemini
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            # Menggunakan model 2.5 Flash (Terbaru & Cepat)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            print("✅ Otak AI Aktif: Gemini 2.5 Flash")
        except Exception as e:
            print(f"Error Konfigurasi AI: {e}")
            self.model = None

    def analyze_market_clusters(self, bulk_data):
        """
        Fungsi BLUE OCEAN: Membandingkan performa antar Sub-Niche.
        Input: List of dict [{'title': '...', 'views': ..., 'keyword_source': '...'}]
        """
        if not self.model: return "<h3>Error: Otak AI belum aktif.</h3>"

        # 1. Siapkan Data untuk AI
        data_str = "DATA VIDEO PER SUB-NICHE:\n"
        # ambil  data video satu persatu dari bulk_data hasil scraping  
        for i, item in enumerate(bulk_data):
            # Kita beritahu AI video ini datang dari keyword mana
            data_str += f"- [Sub-Topik: {item['keyword_source']}] Judul: {item['title']} ({item['views']} views)\n"
            # lalu ditaro variable data_str

        # 2. Prompt Engineering (Blue Ocean Strategy)
        prompt = f"""
        Kamu adalah Pakar Strategi Konten "Blue Ocean".
        Tugasmu adalah mencari CELAH PASAR dari data video berikut.
        
        {data_str}
        
        INSTRUKSI ANALISIS:
        1. Bandingkan performa antar "Sub-Topik".
        2. Cari Sub-Topik mana yang memiliki Views Tinggi tapi persaingannya terlihat spesifik (Blue Ocean).
        3. Identifikasi "Winner" (Pemenang) dan "Loser" (Topik jenuh).
        
        OUTPUT HTML (Langsung kode HTML tanpa markdown):
        
        <h3>🏆 BLUE OCEAN FOUND: [NAMA SUB-TOPIK PEMENANG]</h3>
        <p><b>Potensi Views:</b> Tinggi | <b>Status:</b> Low Competition (Celah Pasar)</p>
        <p><i>Kenapa ini menang? Karena audiens di sub-topik ini sangat aktif mencari konten tentang [ALASAN], sementara konten yang ada masih terbatas.</i></p>
        
        <div style='background-color:#e8f5e9; padding:15px; border-radius:8px; border-left: 5px solid #2e7d32;'>
            <b>🚀 STRATEGI EKSEKUSI:</b>
            <br>Fokus bahas sub-topik: <b>[NAMA SUB-TOPIK PEMENANG]</b>.
            <br><b>Ide Judul Viral:</b>
            <ul>
                <li>[IDE JUDUL 1 - Pancing Emosi]</li>
                <li>[IDE JUDUL 2 - Pancing Penasaran]</li>
            </ul>
        </div>
        
        <hr>
        <h4>📊 Perbandingan Sub-Niche Lain:</h4>
        <ul>
            <li><b>[Sub-Topik B]</b>: [Analisis singkat kenapa ini kalah/jenuh]</li>
            <li><b>[Sub-Topik C]</b>: [Analisis singkat]</li>
        </ul>
        """
        
        try:
            # mengirim prompt diatas abis itu google merespon, lalu mengirim balik jawabannya ke variable response
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"<p style='color:red'>Gagal analisis AI: {str(e)}</p>"

    def generate_content_outline(self, topic_title, transcript_text):
        """
        Fungsi MINING: Membuat Outline dari Transkrip Video Viral.
        Input: Judul Topik, Teks Transkrip (bisa panjang).
        """
        if not self.model: return "Error AI."

        # Potong transkrip jika kepanjangan
        safe_text = transcript_text[:30000] 
        
        prompt = f"""
        Saya ingin membuat video YouTube Shorts tentang topik: "{topic_title}".
        Berikut adalah transkrip dari video viral kompetitor sebagai bahan riset:
        
        --- AWAL TRANSKRIP ---
        {safe_text}
        --- AKHIR TRANSKRIP ---
        
        Tugasmu: Lakukan CONTENT MINING.
        Ekstrak pola sukses dari materi ini dan buatkan Outline Video Baru untuk saya (JANGAN COPY PASTE, tapi ATM - Amati Tiru Modifikasi).
        
        Output HTML (Tanpa markdown):
        <h3>📝 OUTLINE KONTEN: {topic_title}</h3>
        
        <ul>
        <li><b>HOOK (0-3 detik):</b> [Kalimat pembuka yang bikin penasaran]</li>
        <li><b>INTI MATERI:</b>
            <ul>
                <li>Poin 1: ...</li>
                <li>Poin 2: ...</li>
            </ul>
        </li>
        <li><b>CTA (Call to Action):</b> [Kalimat penutup]</li>
        </ul>
        
        <div style='background-color:#fff3e0; padding:10px; border-radius:5px;'>
            <b>💡 Kunci Viral (Mining Result):</b>
            <br>Video referensi sukses karena menggunakan kata kunci: <b>[KEYWORDS]</b>.
        </div>
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gagal mining konten: {str(e)}"