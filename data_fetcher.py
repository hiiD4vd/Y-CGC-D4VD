# data_fetcher.py - UPDATED FOR V3.0

from googleapiclient.discovery import build
from pytrends.request import TrendReq
from youtube_transcript_api import YouTubeTranscriptApi # <--- LIBRARY BARU
from youtube_transcript_api.formatters import TextFormatter
import config
from core.video_case import VideoCase
import time
import random

class DataFetcher:
    def __init__(self):
        # Gunakan API Key dari Config
        self.youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)
        self.trends_connector = TrendReq(hl='id-ID', tz=420, retries=2, backoff_factor=0.1)

    # --- FITUR 1: DATA MINING (Video Biasa) ---
    def search_youtube_videos(self, query: str, max_results=config.MAX_VIDEOS_PER_QUERY) -> list:
        print(f"-> Searching YouTube for: {query}")
        try:
            request = self.youtube.search().list(
                q=query, part='snippet', type='video',
                maxResults=max_results, regionCode=config.SEARCH_REGION,
                videoDuration='short' # Fokus Shorts
            )
            response = request.execute()
            video_ids = [item['id']['videoId'] for item in response.get('items', [])]
            
            if video_ids:
                return self._get_video_details(video_ids)
            return []
        except Exception as e:
            print(f"Error searching videos: {e}")
            return []

    def _get_video_details(self, video_ids: list) -> list:
        video_cases = []
        video_ids_str = ','.join(video_ids)
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics', id=video_ids_str
            )
            response = request.execute()
            
            for item in response.get('items', []):
                new_case = VideoCase(
                    video_id=item['id'],
                    title=item['snippet']['title'],
                    raw_tags=item['snippet'].get('tags'),
                )
                stats = item.get('statistics', {})
                new_case.raw_views = int(stats.get('viewCount', 0))
                new_case.raw_likes = int(stats.get('likeCount', 0))
                new_case.raw_comments = int(stats.get('commentCount', 0))
                new_case.thumbnail_url = item['snippet']['thumbnails']['high']['url']
                video_cases.append(new_case)
            return video_cases
        except Exception as e:
            print(f"Error detail: {e}")
            return []

    # --- FITUR 2: CHANNEL INTELLIGENCE (Baru) ---
    def get_channel_id(self, channel_name: str):
        """Mencari ID Channel berdasarkan nama."""
        try:
            req = self.youtube.search().list(
                q=channel_name, type='channel', part='id,snippet', maxResults=1
            )
            res = req.execute()
            if res['items']:
                return res['items'][0]['id']['channelId'], res['items'][0]['snippet']['title']
            return None, None
        except Exception as e:
            return None, None

    def get_channel_top_videos(self, channel_id: str, max_results=5):
        """Mengambil video terpopuler dari channel."""
        try:
            # Langkah 1: Ambil Playlist 'Uploads' dari Channel ini
            # (Ini cara lebih hemat kuota daripada search)
            ch_req = self.youtube.channels().list(id=channel_id, part='contentDetails').execute()
            uploads_playlist_id = ch_req['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Langkah 2: Ambil video dari playlist tersebut
            # Note: API Playlist tidak bisa sort by ViewCount secara langsung,
            # Jadi kita pakai Search endpoint khusus channel ini agar bisa sort by viewCount (Viral)
            req = self.youtube.search().list(
                channelId=channel_id, part='id,snippet',
                order='viewCount', maxResults=max_results, type='video'
            )
            res = req.execute()
            vid_ids = [item['id']['videoId'] for item in res.get('items', [])]
            
            if vid_ids:
                return self._get_video_details(vid_ids)
            return []
        except Exception as e:
            print(f"Error fetch channel: {e}")
            return []

    # --- FITUR 3: TRANSCRIPT MINING (Baru & Penting) ---
    def get_video_transcript(self, video_id: str):
        """
        Versi Final: Mengembalikan (Judul Video, Isi Transkrip)
        """
        print(f"-> Mining Data untuk Video ID: {video_id}")
        
        video_title = "Topik Tidak Diketahui"
        final_transcript = ""

        # LANGKAH 1: Ambil Judul Video dulu (Wajib)
        try:
            req = self.youtube.videos().list(part='snippet', id=video_id)
            res = req.execute()
            if res['items']:
                video_title = res['items'][0]['snippet']['title']
        except Exception as e:
            print(f"   ⚠️ Gagal ambil judul: {e}")

        # LANGKAH 2: Coba Ambil Subtitle (CC)
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            target = transcript_list.find_transcript(['id', 'en', 'id-ID', 'en-US'])
            transcript_data = target.fetch()
            
            formatter = TextFormatter()
            text_formatted = formatter.format_transcript(transcript_data)
            final_transcript = text_formatted.replace("\n", " ")
            print("   ✅ Berhasil mengambil Transkrip (CC).")
            
            # RETURN DUA DATA: JUDUL DAN TEKS
            return video_title, final_transcript
            
        except Exception as e:
            print(f"   ⚠️ Transkrip CC tidak tersedia ({e}).")

        # LANGKAH 3: Fallback ke Deskripsi (Plan B)
        try:
            # Kita pakai data dari Langkah 1 tadi
            if res['items']:
                description = res['items'][0]['snippet']['description']
                final_transcript = (
                    f"[CATATAN: Ini bukan transkrip, tapi Deskripsi Video]\n"
                    f"{description}"
                )
                print("   ✅ Menggunakan Deskripsi sebagai pengganti.")
                return video_title, final_transcript
                
        except Exception as e:
            print(f"   ❌ Gagal Total: {e}")

        return video_title, ""

    # --- FITUR 4: GOOGLE TRENDS ---
    def fetch_trending_keywords(self, niche_keyword: str) -> list:
        """
        Mencari 'Anak' Keyword (Related Queries) dari Google Trends.
        Contoh: Input 'Mesin' -> Output ['Mesin Diesel', 'Mesin CNC', 'Mesin Bubut']
        """
        print(f"-> Expanding Keyword: {niche_keyword}")
        try:
            # Menggunakan timeframe 30 hari terakhir agar trennya segar
            self.trends_connector.build_payload(kw_list=[niche_keyword], timeframe='today 1-m', geo=config.SEARCH_REGION)
            related_queries = self.trends_connector.related_queries()
            
            top_keywords = []
            
            # Ambil 'top' queries (pencarian terbanyak)
            if related_queries.get(niche_keyword) and related_queries[niche_keyword]['top'] is not None:
                # Ambil 4 keyword teratas saja biar tidak kebanyakan
                df = related_queries[niche_keyword]['top']
                top_keywords = df['query'].head(4).tolist()
            
            # Jika kosong, kembalikan keyword asli saja
            if not top_keywords:
                print("   ⚠️ Tidak ada keyword turunan, menggunakan keyword asli.")
                return [niche_keyword]
                
            # Tambahkan keyword asli ke dalam list agar ikut dianalisis
            if niche_keyword not in top_keywords:
                top_keywords.insert(0, niche_keyword)
                
            print(f"   ✅ Expanded: {top_keywords}")
            return top_keywords

        except Exception as e:
            print(f"   ❌ Gagal Expand Keyword: {e}")
            # Fallback: Kembalikan keyword asli
            return [niche_keyword]
            
    # --- FITUR 5: DEMAND SCORE ---
    def get_demand_score(self, keyword: str) -> float:
        # (Kode lama Anda tetap dipakai di sini)
        try:
            self.trends_connector.build_payload(kw_list=[keyword], timeframe='today 12-m', geo=config.SEARCH_REGION)
            data = self.trends_connector.interest_over_time()
            if not data.empty:
                return data[keyword].mean()
            return 5.0
        except:
            return 0.0