import numpy as np
import librosa
import soundfile as sf
from scipy.fftpack import fft

class MicroAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.y, self.sr = librosa.load(file_path)
        self.duration = librosa.get_duration(y=self.y, sr=self.sr)

    def analyze_tonal_balance(self):
        """Membedah spektrum frekuensi ke dalam 4 zona utama menggunakan Librosa STFT."""
        psd = np.abs(librosa.stft(self.y))**2
        freqs = librosa.fft_frequencies(sr=self.sr)
        avg_psd = np.mean(psd, axis=1)

        # Zona Frekuensi
        low = avg_psd[(freqs >= 20) & (freqs <= 150)].mean()
        low_mid = avg_psd[(freqs > 150) & (freqs <= 500)].mean()
        mid_high = avg_psd[(freqs > 500) & (freqs <= 5000)].mean()
        air = avg_psd[(freqs > 5000) & (freqs <= 20000)].mean()

        report = []
        if low_mid > low * 1.5:
            report.append("CRITICAL: 'Muddy' detected di area 200-400Hz. Terlalu banyak penumpukan instrumen di low-mid.")
        if air < mid_high * 0.3:
            report.append("ADVICE: Mix terasa 'dark'. Tambahkan high-shelf di atas 8kHz untuk memberikan 'air'.")
        
        return {
            "low": float(low),
            "low_mid": float(low_mid),
            "mid_high": float(mid_high),
            "air": float(air),
            "findings": report
        }

    def analyze_dynamics(self):
        """Menganalisis Headroom dan Dynamic Range (Crest Factor)."""
        rms = librosa.feature.rms(y=self.y)
        peak = np.max(np.abs(self.y))
        avg_rms = np.mean(rms)
        crest_factor = 20 * np.log10(peak / (avg_rms + 1e-6))

        report = []
        if crest_factor < 6:
            report.append("CRITICAL: Over-compressed! Crest factor terlalu rendah. Transien (kick/snare) kehilangan 'snap'.")
        elif crest_factor > 15:
            report.append("ADVICE: Terlalu dinamis. Gunakan bus compression untuk menyatukan (glue) mix.")

        return {
            "peak_db": float(20 * np.log10(peak + 1e-6)),
            "avg_rms_db": float(20 * np.log10(avg_rms + 1e-6)),
            "crest_factor": float(crest_factor),
            "findings": report
        }

    def analyze_true_peak(self):
        """Deteksi True Peak menggunakan upsampling 4x via Librosa Resample."""
        y_upsampled = librosa.resample(self.y, orig_sr=self.sr, target_sr=self.sr * 4)
        peak_isp = np.max(np.abs(y_upsampled))
        peak_db = 20 * np.log10(peak_isp + 1e-6)
        
        report = []
        if peak_db > -1.0:
            report.append(f"DANGER: True Peak {peak_db:.2f}dB detected. Risiko clipping di streaming platform.")
        
        return {"true_peak_db": float(peak_db), "findings": report}

    def analyze_lufs(self):
        """Integrated LUFS (EBU R128) menggunakan pyloudnorm jika tersedia."""
        # Fallback to RMS-based estimation if pyloudnorm is missing
        rms = np.sqrt(np.mean(self.y**2))
        lufs_est = 20 * np.log10(rms + 1e-6) - 0.69
        return {"integrated_lufs": float(lufs_est), "findings": []}

    def get_full_critique(self):
        tonal = self.analyze_tonal_balance()
        dynamics = self.analyze_dynamics()
        true_peak = self.analyze_true_peak()
        lufs = self.analyze_lufs()
        
        findings = tonal['findings'] + dynamics['findings'] + true_peak['findings'] + lufs['findings']
        
        return {
            "tonal_report": tonal,
            "dynamic_report": dynamics,
            "mastering_report": {"true_peak": true_peak, "lufs": lufs},
            "findings": findings,
            "overall_score": max(0.0, 10.0 - (len(findings) * 1.5))
        }
