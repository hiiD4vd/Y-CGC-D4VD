# model_trainer.py - VERSI JUJUR (SPLIT 80:20)

import numpy as np
from sklearn.svm import SVC           
from sklearn.ensemble import RandomForestClassifier 
from sklearn.linear_model import LogisticRegression 
from sklearn.ensemble import StackingClassifier 
from sklearn.model_selection import train_test_split # <--- INI KUNCI KEJUJURAN

# Import Metrics
from feature_calculator import CustomMetrics 
from nlp_processor import NLPProcessor 
import pandas as pd
import joblib
import os

class ModelTrainer:
    """
    Class ModelTrainer (Versi Split Testing).
    Data akan dibagi: 80% Training, 20% Testing.
    """
    def __init__(self):
        self.base_estimators = [
            ('svm', SVC(probability=True, random_state=42)),
            ('rf', RandomForestClassifier(random_state=42, n_estimators=100))
        ]
        self.meta_learner = LogisticRegression()
        self.model = StackingClassifier(
            estimators=self.base_estimators,
            final_estimator=self.meta_learner,
            cv=3 
        )
        self.is_trained = False
        self.accuracy_report = None
        
        # Tempat menyimpan "Soal Ujian" (20% Data)
        self.X_test = None
        self.y_test = None

    def load_and_preprocess_data(self, dataset_path: str, nlp_processor: NLPProcessor):
        print(f"-> Memuat data dari: {dataset_path}")
        try:
            df = pd.read_csv(dataset_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"FATAL: File {dataset_path} tidak ditemukan.")

       
        simulated_titles = df['title'].astype(str) + " " + df['tags'].astype(str)
        simulated_y = df['is_success'].values 
        
      
        print("-> Melatih TF-IDF Vectorizer...")
        nlp_processor.train_vectorizer(simulated_titles.tolist()) 
        X_text_features = nlp_processor.vectorizer.transform(simulated_titles).toarray()
        

        print("-> Mengekstrak Fitur Proxy (Emotion & OCR)...")
        proxy_features_list = []
        for index, row in df.iterrows():
            emotion = nlp_processor.analyze_title_emotion(str(row['title']))
            density = row.get('ocr_text_density', 0.0)
            proxy_features_list.append([emotion, density])

        X_proxy = np.array(proxy_features_list)
        X_final = np.concatenate((X_text_features, X_proxy), axis=1)
        
        print(f"-> Total Data Siap: {X_final.shape[0]} sampel.")
        return X_final, simulated_y

    def train_ensemble_model(self, X, y):
        print("-> Membagi Data: 80% Latihan | 20% Ujian (Jujur)...")
        
        # INI PROSES PEMBAGIANNYA
        # X_train, y_train = Data buat belajar
        # X_test, y_test   = Data buat ujian (disimpan)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Simpan data ujian ke dalam class biar bisa dipanggil nanti
        self.X_test = X_test
        self.y_test = y_test

        print(f"-> Melatih model dengan {len(X_train)} data...")
        self.model.fit(X_train, y_train)
        
        self.is_trained = True
        print("✅ Pelatihan Selesai. Data Ujian (20%) telah disisihkan.")

    def evaluate_model(self, X=None, y=None):
        # Jika X dan y tidak dikirim manual, pakai data ujian yang disimpan tadi (self.X_test)
        if X is None or y is None:
            if self.X_test is None:
                raise RuntimeError("Belum ada data ujian. Latih model dulu!")
            print("-> Menggunakan Data Ujian (Testing Set) yang disimpan...")
            target_X = self.X_test
            target_y = self.y_test
        else:
            target_X = X
            target_y = y

        if not self.is_trained: raise RuntimeError("Model belum dilatih.")
        
        # Lakukan Ujian
        y_pred = self.model.predict(target_X)
        
        # Hitung Nilai
        accuracy = CustomMetrics.accuracy_score(target_y, y_pred)
        cm = CustomMetrics.confusion_matrix(target_y, y_pred)
        f1 = CustomMetrics.f1_score(target_y, y_pred)
        precision = CustomMetrics.precision_score(target_y, y_pred)
        recall = CustomMetrics.recall_score(target_y, y_pred)

        self.accuracy_report = (
            f"=== HASIL UJIAN (TESTING SET 20%) ===\n"
            f"Jumlah Data Uji: {len(target_y)} sampel\n"
            f"----------------------------------------\n"
            f"AKURASI MODEL : {accuracy:.4f} ({accuracy*100:.2f}%)\n"
            f"Precision     : {precision:.4f}\n"
            f"Recall        : {recall:.4f}\n"
            f"F1-Score      : {f1:.4f}\n"
            f"--- Confusion Matrix ---\n{cm}\n"
            f"Catatan: Ini adalah performa pada data BARU yang belum\n"
            f"pernah dilihat model saat latihan."
        )
        print("✅ Laporan Evaluasi Siap.")

    def save_model(self, filepath='ensemble_model.pkl'):
        if self.is_trained:
            joblib.dump(self.model, filepath)
            # Kita juga simpan data testnya buat jaga-jaga kalau app di-restart
            joblib.dump((self.X_test, self.y_test), 'test_data.pkl') 
            print(f"-> Model & Data Ujian disimpan ke {filepath}")

    def load_model(self, filepath='ensemble_model.pkl'):
        if os.path.exists(filepath):
            self.model = joblib.load(filepath)
            self.is_trained = True
            
            # Coba load data ujian lama juga
            if os.path.exists('test_data.pkl'):
                self.X_test, self.y_test = joblib.load('test_data.pkl')
                
            print(f"-> Model dimuat dari {filepath}")
            return True
        return False