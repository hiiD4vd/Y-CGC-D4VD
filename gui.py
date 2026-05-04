# gui.py - Y-CGC V3.3 (SIDEBAR LAYOUT - CLEAN THEME)
# VERSI FINAL - FIX TOMBOL STATUS MODEL

import sys
import numpy as np
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QStackedWidget, QGridLayout, QTextEdit, QMessageBox,
    QGroupBox, QListWidget, QListWidgetItem, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor

# --- IMPORT MODUL INTI (TETAP SAMA) ---
from feature_calculator import FeatureCalculator
from model_trainer import ModelTrainer
from nlp_processor import NLPProcessor
from ocr_processor import OCRProcessor
from data_fetcher import DataFetcher
from ai_advisor import AIAdvisor

class ContentGapApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Youtube Content Gap Creator") 
        self.setGeometry(100, 100, 1200, 800) 

        try:
            # Terapkan Tema Clean (Putih/Abu)
            self.apply_clean_theme()
            
            # Inisialisasi Backend
            self.trainer = ModelTrainer()
            self.nlp_processor = NLPProcessor()
            self.ocr_processor = OCRProcessor()
            self.fetcher = DataFetcher()
            self.ai_advisor = AIAdvisor()
            
            self.is_ready = False
            self.init_ui()
            
            
        except Exception as e:
             QMessageBox.critical(self, "ERROR FATAL", f"Gagal Inisialisasi: {e}")

    def apply_clean_theme(self):
        """Style Sheet untuk meniru desain gambar referensi"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QListWidget {
                background-color: #1e1e1e;
                color: #aaaaaa;
                border: none;
                font-size: 15px;
                outline: 0;
            }
            QListWidget::item {
                padding: 15px 20px;
                border-left: 4px solid transparent;
            }
            QListWidget::item:selected {
                background-color: #2d2d2d;
                color: #ffffff;
                border-left: 4px solid #4fc3f7;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #252525;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4fc3f7;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
            QGroupBox {
                border: none;
                margin-top: 10px;
                font-weight: bold;
                font-size: 16px;
                color: #000000;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 0px;
                padding: 0 0px 10px 0px;
            }
        """)

    def init_ui(self):
        # Layout Utama: Horizontal (Kiri: Menu, Kanan: Konten)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 1. SIDEBAR MENU (KIRI) ---
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(250) 
        
        item1 = QListWidgetItem("  🧠 Market Intelligence")
        item2 = QListWidgetItem("  🎯 Validasi Viralitas")
        item3 = QListWidgetItem("  📊 Status Model")
        
        item1.setSizeHint(QSize(0, 60))
        item2.setSizeHint(QSize(0, 60))
        item3.setSizeHint(QSize(0, 60))
        
        self.sidebar.addItem(item1)
        self.sidebar.addItem(item2)
        self.sidebar.addItem(item3)
        
        self.sidebar.currentRowChanged.connect(self.switch_page)

        # --- 2. MAIN CONTENT AREA (KANAN) ---
        self.pages = QStackedWidget()
        self.pages.setContentsMargins(20, 20, 20, 20)

        self.page_ideation = QWidget()
        self.setup_intelligence_page()
        self.pages.addWidget(self.page_ideation)

        self.page_prediction = QWidget()
        self.setup_validation_page()
        self.pages.addWidget(self.page_prediction)

        self.page_status = QWidget()
        self.setup_status_page() # INI YANG KITA MODIFIKASI
        self.pages.addWidget(self.page_status)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)
        
        self.setLayout(main_layout)
        self.sidebar.setCurrentRow(0)

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)

    # =========================================================================
    # HALAMAN 1 & 2 (TETAP SAMA PERSIS SEPERTI KODE ABANG)
    # =========================================================================
    def setup_intelligence_page(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        lbl_title = QLabel("Tahap 1: Analisis Struktur Pasar")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #000; margin-bottom: 10px;")
        layout.addWidget(lbl_title)
        
        top_bar = QHBoxLayout()
        lbl_niche = QLabel("Niche / Topik Utama:")
        lbl_niche.setStyleSheet("font-weight: bold;")
        self.niche_input = QLineEdit()
        self.niche_input.setPlaceholderText("Contoh: Mesin, Masak, Coding")
        
        self.btn_dominator = QPushButton("🚀 JALANKAN MARKET DOMINATOR (AI)")
        self.btn_dominator.setCursor(Qt.PointingHandCursor)
        self.btn_dominator.setStyleSheet("""
            QPushButton { background-color: #6a1b21; color: white; border-radius: 6px; padding: 12px 20px; font-weight: bold; }
            QPushButton:hover { background-color: #8e242c; }
        """)
        self.btn_dominator.clicked.connect(self.run_market_dominator)
        
        top_bar.addWidget(lbl_niche)
        top_bar.addWidget(self.niche_input)
        top_bar.addWidget(self.btn_dominator)
        layout.addLayout(top_bar)

        self.intel_result_area = QTextEdit()
        self.intel_result_area.setReadOnly(True)
        self.intel_result_area.setPlaceholderText("Hasil analisis AI akan muncul di sini...")
        self.intel_result_area.setStyleSheet("QTextEdit { border: 1px solid #ddd; background: #fff; border-radius: 8px; }")
        layout.addWidget(self.intel_result_area)

        self.btn_transfer = QPushButton("➡️ Gunakan Teks Terblokir (Highlight) sebagai Judul Validasi")
        self.btn_transfer.setCursor(Qt.PointingHandCursor)
        self.btn_transfer.setStyleSheet("""
            QPushButton { background-color: #0d47a1; color: white; border-radius: 6px; padding: 12px; font-weight: bold; }
            QPushButton:hover { background-color: #1565c0; }
        """)
        self.btn_transfer.clicked.connect(self.transfer_idea_to_validation)
        layout.addWidget(self.btn_transfer)

        lbl_mining = QLabel("Tahap 2: Bedah Konten")
        lbl_mining.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 15px;")
        layout.addWidget(lbl_mining)
        
        bot_bar = QHBoxLayout()
        lbl_vid = QLabel("ID Video Referensi:")
        self.video_id_input = QLineEdit()
        self.video_id_input.setPlaceholderText("Paste ID Video Viral di sini...")
        
        self.btn_mining = QPushButton("⛏️ TAMBANG OUTLINE")
        self.btn_mining.setCursor(Qt.PointingHandCursor)
        self.btn_mining.setStyleSheet("""
            QPushButton { background-color: #424242; color: white; border-radius: 6px; padding: 12px 20px; font-weight: bold; }
            QPushButton:hover { background-color: #616161; }
        """)
        self.btn_mining.clicked.connect(self.run_content_mining)
        
        bot_bar.addWidget(lbl_vid)
        bot_bar.addWidget(self.video_id_input)
        bot_bar.addWidget(self.btn_mining)
        layout.addLayout(bot_bar)
        
        self.page_ideation.setLayout(layout)

    def setup_validation_page(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Tahap 3: Validasi Keputusan (Classification)")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #000; margin-bottom: 20px;")
        layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setSpacing(10)
        
        lbl_j = QLabel("Judul Final:")
        lbl_j.setStyleSheet("font-weight: bold;")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Judul video yang akan diupload...")
        
        lbl_t = QLabel("Tags Kunci:")
        lbl_t.setStyleSheet("font-weight: bold;")
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Pisahkan dengan koma...")
        
        form_layout.addWidget(lbl_j, 0, 0)
        form_layout.addWidget(self.title_input, 0, 1)
        form_layout.addWidget(lbl_t, 1, 0)
        form_layout.addWidget(self.tags_input, 1, 1)
        
        layout.addLayout(form_layout)

        self.btn_validate = QPushButton("PREDIKSI POTENSI VIRAL")
        self.btn_validate.setCursor(Qt.PointingHandCursor)
        self.btn_validate.setStyleSheet("""
            QPushButton { background-color: #2e7d32; color: white; border-radius: 6px; padding: 15px; font-size: 16px; font-weight: bold; margin-top: 10px; }
            QPushButton:hover { background-color: #388e3c; }
        """)
        self.btn_validate.clicked.connect(self.run_analysis)
        layout.addWidget(self.btn_validate)

        self.output_text_area = QTextEdit()
        self.output_text_area.setReadOnly(True)
        self.output_text_area.setPlaceholderText("Hasil prediksi akan muncul di sini...")
        layout.addWidget(self.output_text_area)
        
        self.page_prediction.setLayout(layout)

    # =========================================================================
    # HALAMAN 3: STATUS (SAYA HANYA UBAH BAGIAN INI)
    # =========================================================================
    def setup_status_page(self):
        layout = QVBoxLayout()
        title = QLabel("Status Sistem & Model")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # --- [BARU] TOMBOL KONTROL ---
        btn_layout = QHBoxLayout()
        
        # Tombol Train
        self.btn_train_manual = QPushButton("🔄 LATIH ULANG MODEL (Train)")
        self.btn_train_manual.setCursor(Qt.PointingHandCursor)
        self.btn_train_manual.setStyleSheet("""
            QPushButton { background-color: #00897b; color: white; font-weight: bold; padding: 10px; border-radius: 5px; }
            QPushButton:hover { background-color: #00695c; }
        """)
        self.btn_train_manual.clicked.connect(self.run_manual_training) # Aksi baru
        
        # Tombol Evaluasi
        self.btn_eval_manual = QPushButton("📊 LIHAT RAPOR EVALUASI")
        self.btn_eval_manual.setCursor(Qt.PointingHandCursor)
        self.btn_eval_manual.setStyleSheet("""
            QPushButton { background-color: #fb8c00; color: white; font-weight: bold; padding: 10px; border-radius: 5px; }
            QPushButton:hover { background-color: #ef6c00; }
        """)
        self.btn_eval_manual.clicked.connect(self.run_manual_evaluation) # Aksi baru
        
        btn_layout.addWidget(self.btn_train_manual)
        btn_layout.addWidget(self.btn_eval_manual)
        layout.addLayout(btn_layout)
        # -----------------------------
        
        self.metrics_display = QTextEdit()
        self.metrics_display.setReadOnly(True)
        self.metrics_display.setStyleSheet("""
            background-color: #222; color: #00e676; font-family: Consolas; font-size: 13px; margin-top: 10px;
        """)
        self.metrics_display.setText("✅ System Ready.\nKlik tombol di atas untuk memulai.")
        
        layout.addWidget(self.metrics_display)
        self.page_status.setLayout(layout)

    # =========================================================================
    # LOGIKA BARU UNTUK TOMBOL (Supaya tombolnya jalan)
    # =========================================================================
    def run_manual_training(self):
        self.metrics_display.setText("⏳ Sedang melatih model... Mohon tunggu.")
        QApplication.processEvents()
        
        data_file = "shorts_training_data.csv" # Pastikan file ini ada
        model_file = "ensemble_model.pkl"
        vectorizer_file = "tfidf_vectorizer.pkl"
        
        try:
            # 1. Load & Preprocess
            X_train, y_train = self.trainer.load_and_preprocess_data(data_file, self.nlp_processor)
            
            # 2. Train Model
            self.trainer.train_ensemble_model(X_train, y_train)
            
            # 3. Simpan
            self.trainer.save_model(model_file)
            self.nlp_processor.save_vectorizer(vectorizer_file)
            
            self.is_ready = True
            self.metrics_display.append("\n✅ PELATIHAN SELESAI!\nModel dan Vectorizer telah diperbarui.")
            
        except Exception as e:
            self.metrics_display.append(f"\n❌ Error Training: {e}")

    def run_manual_evaluation(self):
        self.metrics_display.append("\n⏳ Menghitung metrik evaluasi (Testing Set)...")
        QApplication.processEvents()
        
        try:
            if not self.is_ready:
                 # Coba load model & data test kalau ada
                 if os.path.exists("ensemble_model.pkl"):
                     self.trainer.load_model("ensemble_model.pkl")
                     self.nlp_processor.load_vectorizer("tfidf_vectorizer.pkl")
                     self.is_ready = True
                 else:
                    self.metrics_display.append("⚠️ Model belum siap. Latih dulu!")
                    return

            # PERUBAHAN PENTING DI SINI:
            # Kita TIDAK mengirim X dan y. Biarkan trainer pakai X_test miliknya sendiri.
            self.trainer.evaluate_model() # Kosongkan kurungnya!
            
            # Tampilkan Laporan
            report = self.trainer.accuracy_report
            self.metrics_display.setText("") # Bersihkan layar dulu
            self.metrics_display.append(report)
            
        except Exception as e:
            self.metrics_display.append(f"\n❌ Error Evaluasi: {e}")

    # =========================================================================
    # LOGIKA BACKEND LAINNYA (TETAP SAMA)
    # =========================================================================
    def transfer_idea_to_validation(self):
        cursor = self.intel_result_area.textCursor()
        selected_text = cursor.selectedText().strip()
        if not selected_text:
            QMessageBox.warning(self, "Pilih Judul", "Blok/Highlight dulu judul saran AI.")
            return
        self.title_input.setText(selected_text)
        niche = self.niche_input.text()
        if niche: self.tags_input.setText(niche)
        self.sidebar.setCurrentRow(1) 
        QMessageBox.information(self, "Sukses", "Data ditransfer ke halaman Validasi.")

    def run_market_dominator(self):
        niche = self.niche_input.text().strip()
        if not niche: 
            QMessageBox.warning(self, "Input", "Masukkan Niche dulu!")
            return
        self.intel_result_area.setText(f"📡 Radar Aktif: Mencari turunan topik dari '{niche}'...")
        QApplication.processEvents()
        try:
            expanded_keywords = self.fetcher.fetch_trending_keywords(niche)
            report_text = f"✅ Menemukan {len(expanded_keywords)} Sub-Niche Potensial:\n"
            for k in expanded_keywords:
                report_text += f"   - {k}\n"
            self.intel_result_area.setText(report_text + "\n🚀 Memulai Deep Scanning untuk setiap Sub-Niche...")
            QApplication.processEvents()
            bulk_data = []
            for sub_kw in expanded_keywords:
                videos = self.fetcher.search_youtube_videos(sub_kw, max_results=5)
                for v in videos:
                    bulk_data.append({'title': v.title, 'views': v.raw_views, 'keyword_source': sub_kw})
            if not bulk_data:
                self.intel_result_area.setText("❌ Tidak ditemukan video yang relevan.")
                return
            self.intel_result_area.append(f"\n📦 Total Data Terkumpul: {len(bulk_data)} Video.")
            self.intel_result_area.append("🤖 Mengirim data ke Gemini AI untuk Analisis Blue Ocean...")
            QApplication.processEvents()
            ai_analysis = self.ai_advisor.analyze_market_clusters(bulk_data)
            html = f"<h2>🌊 Laporan Blue Ocean Strategy: '{niche}'</h2>"
            html += f"<p><b>Sub-Niche yang Dianalisis:</b> {', '.join(expanded_keywords)}</p><hr>"
            html += ai_analysis
            self.intel_result_area.setText(html)
        except Exception as e:
            self.intel_result_area.setText(f"Error Blue Ocean: {str(e)}")

    def run_content_mining(self):
        vid_id = self.video_id_input.text().strip()
        if not vid_id: return
        self.intel_result_area.append("\n\n🔄 Mengambil Data Video...")
        QApplication.processEvents()
        real_title, transcript = self.fetcher.get_video_transcript(vid_id)
        if not transcript:
            self.intel_result_area.append("❌ Gagal ambil data.")
            return
        self.intel_result_area.append(f"🤖 Mining: '{real_title}'...")
        QApplication.processEvents()
        outline = self.ai_advisor.generate_content_outline(real_title, transcript)
        current = self.intel_result_area.toHtml()
        self.intel_result_area.setHtml(current + "<hr>" + outline)

    #klasifikasi
    def run_analysis(self):
        if not self.is_ready: return
        title = self.title_input.text()
        tags_str = self.tags_input.text()
        if not title: return
        tags = [t.strip() for t in tags_str.split(',') if t.strip()]
        main_kw = tags[0] if tags else title
        self.output_text_area.setText("🚀 Menganalisis...")
        QApplication.processEvents()
        try:
            
            demand = self.fetcher.get_demand_score(main_kw)
            comps = self.fetcher.search_youtube_videos(main_kw, max_results=20)
            supply = len(comps) * 50 if comps else 10
            q_score = 0.01
            if comps:
                total_cqs = sum([self.nlp_processor.calculate_proxy_cqs(v.raw_views, v.raw_likes, v.raw_comments) for v in comps])
                q_score = total_cqs / len(comps)

            text_vec = self.nlp_processor.get_semantic_embedding(title + " " + tags_str)
            emotion = self.nlp_processor.analyze_title_emotion(title)
            density = 0.0 
            proxy = np.array([emotion, density])

            inp = np.concatenate((text_vec, proxy)).astype(np.float32).reshape(1, -1)
            exp_dim = self.trainer.model.n_features_in_

            if inp.shape[1] < exp_dim:
                inp = np.concatenate((inp, np.zeros((1, exp_dim - inp.shape[1]))), axis=1)
            elif inp.shape[1] > exp_dim: inp = inp[:, :exp_dim]
            
            probs = self.trainer.model.predict_proba(inp)[0]
            success_probability = probs[1]
            threshold = 0.35 

            #decision & gap score making
            if success_probability > threshold:
                label = "SUCCESS"
                gap_score = FeatureCalculator.calculate_strategic_gap_score(demand, supply, q_score) * 1.5
            else:
                label = "FAILURE"
                gap_score = FeatureCalculator.calculate_strategic_gap_score(demand, supply, q_score)
            gap_score = min(gap_score, 10.0)
            
            color = "#2e7d32" if label == "SUCCESS" else "#c62828"
            self.output_text_area.setText(
                f"<div style='text-align:center; margin-top:10px;'>"
                f"<h1 style='color:{color}; font-size: 24pt;'>{label}</h1>"
                f"<h2>Gap Score: {gap_score:.1f} / 10.0</h2><hr>"
                f"<p>Confidence: {success_probability*100:.1f}% | Demand: {demand:.0f}</p></div>"
            )
        except Exception as e:
            self.output_text_area.setText(f"Error: {e}")

    def train_and_evaluate_on_startup(self):
        # Method ini saya biarkan ada tapi tidak dipanggil di init_ui
        # karena fungsinya sudah digantikan tombol manual
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ContentGapApp()
    w.show()
    sys.exit(app.exec_())