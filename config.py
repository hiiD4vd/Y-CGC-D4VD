
import os
from dotenv import load_dotenv

load_dotenv()

# --- Kunci API (Ganti dengan Kunci Anda) ---
# Penting: JANGAN upload API key ke repository publik!
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY") 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Jika menggunakan pytrends, tidak perlu kunci eksplisit
# Tesseract OCR path (sesuaikan dengan lokasi instalasi Anda)
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- Konstanta Proyek ---
SEARCH_REGION = 'ID' # Indonesia
MAX_TRENDING_KEYWORDS = 50 # Jumlah keyword yang diambil dari Trends
MAX_VIDEOS_PER_QUERY = 10  # Jumlah video kompetitor yang diambil per keyword