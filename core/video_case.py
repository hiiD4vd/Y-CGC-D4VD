# core/video_case.py

class VideoCase:
    """
    Objek yang merepresentasikan satu video Shorts YouTube 
    dan menampung semua hasil Feature Engineering.
    """
    def __init__(self, video_id: str, title: str, raw_tags: list = None):
        # Data Mentah (Dari API YouTube)
        self.video_id = video_id
        self.title = title
        self.raw_tags = raw_tags if raw_tags is not None else []
        self.thumbnail_url = ""
        self.raw_script = ""
        self.raw_views = 0
        self.raw_likes = 0
        self.raw_comments = 0
        
        # --- Label Pelatihan (Wajib Ada) ---
        self.is_success = None  # True/False (SUCCESS/FAILURE)
        
        # --- Fitur Engineering Lanjutan (The Brilliance) ---
        
        # 1. Semantic Features (BERT/NLP)
        self.semantic_vector = None   # Vektor 768 dimensi (atau sesuai model BERT)
        self.narrative_density = 0.0  # Skor Kepadatan Informasi Skrip
        
        # 2. Visual & Emotional Proxies
        self.ocr_text_density = 0.0   # Kerapatan Teks pada Thumbnail
        self.title_emotion_score = 0.0 # Skor Emosi Judul
        self.proxy_content_quality = 0.0 # CQS Score
        
        # 3. Content Gap Features
        self.demand_score = 0.0       # Google Trends Search Volume
        self.supply_score = 0.0       # Jumlah video kompetitor
        self.gap_score = 0.0          # Hasil hitungan (Demand / Supply)

    def __repr__(self):
        """Representasi objek untuk debugging."""
        return f"VideoCase(ID={self.video_id}, Title='{self.title[:30]}...', Success={self.is_success})"