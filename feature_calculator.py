import numpy as np

class FeatureCalculator:
    """
    Class yang menyimpan semua logika perhitungan ilmiah dan metrik strategis.
    REVISI: Ditambahkan pengaman matematika (Math Safety).
    """
    

    @staticmethod
    def calculate_wpi(views: int, likes: int, comments: int) -> float:
        """ Menghitung Weighted Performance Index (WPI) sebagai Proxy Kualitas. """
        # Pengaman agar tidak crash jika views 0
        if views == 0: return 0.0

        engagement = likes + comments
        # LANGKAH 2: Bagi dengan Views (Dapat rasio desimal, misal 0.05)
        
        ratio = engagement / views
        """ nah karena klo hasilnya kecil banget, misal 0.002, 
        jadi kita kali 1000 di langkah berikutnya biar angkanya lebih gede dan gampang dibaca """
        # LANGKAH 3 (PENTING): Kali 1000 sesuai Persamaan (3) di Jurnal
        wpi = ratio * 1000
        
        
        return wpi

    @staticmethod
    def calculate_strategic_gap_score(demand_index: float, supply_count: int, quality_score: float) -> float:
        """
        Menghitung Content Gap Score (CSG).
        Formula: (Demand Index * Quality Score) / (Log Supply)
        """
        # 1. Supply Count Log Smoothing
        # Menggunakan max(supply, 2) agar log10 minimal log10(2) = 0.3, pembagi tidak pernah 0.
        # Atau gunakan log10(supply + 10) untuk meredam supply kecil.

        #maksdnya itu pilih yg lebih besar antara supply_count atau 2, jadi klo supply_count < 2, dia bakal pake 2 karena kalau 0 nanti crash
        adjusted_supply = max(supply_count, 2)

        #ini logaritma basis 10 dari adjusted_supply, jadi misalnya adjusted_supply = 1000, maka log_supply = 3 agar angka pembagi tidk terlalu besar
        log_supply = np.log10(adjusted_supply)
        
        # 2. Hitung Gap Score
        # Demand (0-100) * Quality (0-0.1) -> Max 10. 
        # Dibagi log supply.
        raw_score = (demand_index * quality_score * 100) # Scaling factor agar angka terbaca
        gap_score = raw_score / log_supply
        
        # 3. Normalisasi ke skala 0-10
        return min(max(gap_score, 0.0), 10.0)


# ==============================================================================
# TAMBAHAN BARU: CustomMetrics (Untuk Evaluasi Model Manual Tanpa Library)
# ==============================================================================

class CustomMetrics:
    """
    Kelas ini berisi rumus matematika manual untuk menghitung evaluasi model.
    Sesuai permintaan dosen: TIDAK MENGGUNAKAN LIBRARY EVALUASI (sklearn.metrics).
    Murni menggunakan aritmatika dasar (Looping, Tambah, Bagi).
    """

    @staticmethod
    def calculate_tp_tn_fp_fn(y_true, y_pred):
        """Hitung komponen Confusion Matrix secara manual loop per baris."""
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        
        # Zip menyatukan kunci jawaban dan tebakan biar bisa dicek barengan
        for asli, tebakan in zip(y_true, y_pred):
            if asli == 1 and tebakan == 1:
                TP += 1
            elif asli == 0 and tebakan == 0:
                TN += 1
            elif asli == 0 and tebakan == 1:
                FP += 1  # Salah Tebak (PHP / False Positive)
            elif asli == 1 and tebakan == 0:
                FN += 1  # Kelewat (False Negative)
                
        return TP, TN, FP, FN

    @staticmethod
    def accuracy_score(y_true, y_pred):
        # Rumus: (Benar Viral + Benar Gagal) / Total Data
        TP, TN, FP, FN = CustomMetrics.calculate_tp_tn_fp_fn(y_true, y_pred)
        total = TP + TN + FP + FN
        if total == 0: return 0.0
        return (TP + TN) / total

    @staticmethod
    def precision_score(y_true, y_pred):
        # Rumus: Benar Viral / (Benar Viral + Salah Tebak Viral)
        TP, TN, FP, FN = CustomMetrics.calculate_tp_tn_fp_fn(y_true, y_pred)
        pembagi = TP + FP
        if pembagi == 0: return 0.0 
        return TP / pembagi

    @staticmethod
    def recall_score(y_true, y_pred):
        # Rumus: Benar Viral / (Total yang Aslinya Viral)
        TP, TN, FP, FN = CustomMetrics.calculate_tp_tn_fp_fn(y_true, y_pred)
        pembagi = TP + FN
        if pembagi == 0: return 0.0
        return TP / pembagi

    @staticmethod
    def f1_score(y_true, y_pred):
        # Rumus Harmonic Mean
        p = CustomMetrics.precision_score(y_true, y_pred)
        r = CustomMetrics.recall_score(y_true, y_pred)
        
        if (p + r) == 0: return 0.0
        return 2 * (p * r) / (p + r)

    @staticmethod
    def confusion_matrix(y_true, y_pred):
        # Outputkan format teks tabel manual biar rapi di print
        TP, TN, FP, FN = CustomMetrics.calculate_tp_tn_fp_fn(y_true, y_pred)
        
        return (
            f"[[TN={TN}  FP={FP}]\n"
            f" [FN={FN}  TP={TP}]]"
        )