# 🎥 Y-CGC (YouTube Content Gap Creator) V3.3

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?logo=qt)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Ensemble%20Model-orange)
![NLP & OCR](https://img.shields.io/badge/NLP%20%26%20OCR-EasyOCR-yellow)

**Y-CGC (YouTube Content Gap Creator)** is an advanced desktop application designed to help YouTube creators analyze market trends, identify content gaps, and generate high-potential video ideas for YouTube Shorts. 

By leveraging **Machine Learning**, **Natural Language Processing (NLP)**, and **Optical Character Recognition (OCR)**, Y-CGC provides data-driven insights to maximize your content's reach and engagement.

---

## ✨ Key Features

- 🔍 **YouTube Data Extraction:** Fetches real-time YouTube Shorts metadata using the official YouTube Data API v3.
- 👁️ **OCR Video Analysis:** Extracts on-screen text and captions from video frames using `EasyOCR`.
- 🧠 **Smart NLP Processing:** Analyzes video titles, tags, and extracted text to understand context and sentiment using TF-IDF.
- 📈 **Predictive ML Model:** Utilizes a pre-trained Ensemble Machine Learning model to predict content performance and identify unsaturated niches (content gaps).
- 💡 **AI Content Advisor:** Generates actionable, AI-driven content recommendations based on gap analysis.
- 🖥️ **Modern Clean GUI:** A sleek, user-friendly desktop interface built with PyQt5, featuring a responsive sidebar layout.

---

## 🏗️ Project Structure

```text
📁 Y-CGC-D4VD
├── 🖥️ gui.py                 # Main application entry point (PyQt5 GUI)
├── 🤖 model_trainer.py       # Machine learning model training script
├── 📊 feature_calculator.py  # Calculates metrics (engagement rate, etc.)
├── 📝 nlp_processor.py       # Text preprocessing & TF-IDF vectorization
├── 👁️ ocr_processor.py       # Optical Character Recognition logic
├── 📥 data_fetcher.py        # YouTube API data collection
├── 💡 ai_advisor.py          # AI recommendation generator
├── 📦 dist/                  # Compiled executable build
└── 📄 requirements.txt       # Project dependencies
```

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/hiiD4vd/Y-CGC-D4VD.git
cd Y-CGC-D4VD
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 5. Run the Application
```bash
python gui.py
```

---

## 🛠️ Built With

* [PyQt5](https://riverbankcomputing.com/software/pyqt/) - The GUI framework
* [EasyOCR](https://github.com/JaidedAI/EasyOCR) - Optical Character Recognition
* [Scikit-Learn](https://scikit-learn.org/) - Machine Learning models
* [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) - Data manipulation
* [YouTube Data API v3](https://developers.google.com/youtube/v3) - Data fetching

---

## 👨‍💻 Author

**Daud (hiiD4vd)**
- GitHub: [@hiiD4vd](https://github.com/hiiD4vd)

---
*Note: This project was developed as a Final Year Project (Tugas Akhir - SPK).*
