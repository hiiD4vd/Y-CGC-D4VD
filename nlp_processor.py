# nlp_processor.py - FINAL STABLE VERSION (TF-IDF)

import numpy as np
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer # Pengganti BERT
import pandas as pd # Digunakan untuk simulasi data
from core.video_case import VideoCase

class NLPProcessor:
    """
    Class untuk mengelola Feature Engineering berbasis teks menggunakan TF-IDF.
    BERT diganti TF-IDF untuk stabilitas sistem.
    """
    def __init__(self):
        # Inisialisasi Vectorizer (akan dilatih nanti saat data siap)
        self.vectorizer = TfidfVectorizer()
        # Dimensi TF-IDF akan ditentukan saat training, kita gunakan placeholder 500
        self.embedding_dim = 500 
        print("-> NLP Processor siap. Menggunakan TF-IDF Vectorizer (100% Stabil).")

    def train_vectorizer(self, corpus: list):
        """ Melatih TF-IDF Vectorizer pada semua teks di dataset training. """
        self.vectorizer.fit(corpus)
        self.embedding_dim = len(self.vectorizer.vocabulary_)
        print(f"-> TF-IDF dilatih dengan {self.embedding_dim} fitur.")
        
    def get_semantic_embedding(self, text: str) -> np.ndarray:
        """
        Menghasilkan vektor semantik (embedding) dari teks menggunakan TF-IDF.
        
        Output: Vektor numerik yang merepresentasikan makna teks.
        """
        if not self.vectorizer.vocabulary_:
            # Jika vectorizer belum dilatih, kembalikan vektor nol sesuai ukuran placeholder
            return np.zeros(self.embedding_dim if self.embedding_dim > 0 else 500) 
            
        # Transformasi teks baru menjadi vektor TF-IDF
        # Penggunaan .toarray() penting untuk mengintegrasikan ke NumPy
        embedding = self.vectorizer.transform([text]).toarray().flatten()
        return embedding


    # --- Metode Kalkulasi Proxy (TIDAK BERUBAH) ---
    def analyze_narrative_density(self, script: str) -> float:
        if not script: return 0.0
        words = script.lower().split()
        unique_words = set(words)
        return len(unique_words) / len(words) if words else 0.0

    def calculate_proxy_cqs(self, raw_views: int, raw_likes: int, raw_comments: int) -> float:
        engagement = raw_likes + raw_comments
        if raw_views == 0: return 0.0
        cqs_score = engagement / raw_views
        return min(cqs_score, 0.10)

    def analyze_title_emotion(self, text: str) -> float:
        if not text: return 0.0
        toxic_keywords = ["gagal", "bodoh", "rahasia", "stop", "paksa", "jangan", "kuat", "buruk", "bahaya"]
        score = 0
        text_lower = text.lower()
        for keyword in toxic_keywords:
            if keyword in text_lower:
                score += 1
        total_words = len(text_lower.split())
        return score / total_words if total_words > 0 else 0.0
    
    def save_vectorizer(self, filepath='tfidf_vectorizer.pkl'):
        """Menyimpan Vectorizer yang sudah dilatih ke file."""
        joblib.dump(self.vectorizer, filepath)
        print(f"-> Vectorizer disimpan ke {filepath}")

    def load_vectorizer(self, filepath='tfidf_vectorizer.pkl'):
        """Memuat Vectorizer dari file."""
        if os.path.exists(filepath):
            self.vectorizer = joblib.load(filepath)
            self.embedding_dim = len(self.vectorizer.vocabulary_)
            print(f"-> Vectorizer dimuat dari {filepath}. Dimensi: {self.embedding_dim}")
            return True
        return False