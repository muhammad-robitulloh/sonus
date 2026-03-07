import numpy as np
import librosa

class PsychoMaskingEngine:
    def __init__(self, file_path):
        self.y, self.sr = librosa.load(file_path)

    def analyze_masking(self):
        """Analyze masking using simplified ERB (Equivalent Rectangular Bandwidth) logic."""
        S = np.abs(librosa.stft(self.y))
        freqs = librosa.fft_frequencies(sr=self.sr)
        avg_S = np.mean(S, axis=1)

        # Simplified ERB model: Bandwidth increases with frequency
        # ERB(f) = 24.7 * (4.37 * f/1000 + 1)
        def get_erb(f):
            return 24.7 * (4.37 * f / 1000 + 1)

        masking_issues = []
        # Focus on Critical Mid-High range (1kHz - 5kHz) where human hearing is most sensitive
        critical_range = (freqs >= 1000) & (freqs <= 5000)
        crit_freqs = freqs[critical_range]
        crit_vals = avg_S[critical_range]

        for i in range(1, len(crit_freqs) - 1):
            erb = get_erb(crit_freqs[i])
            # Check if a neighboring frequency is significantly louder within the ERB
            if crit_vals[i] < crit_vals[i-1] * 0.4: # Arbitrary threshold for "being masked"
                 masking_issues.append({
                     "freq": float(crit_freqs[i]),
                     "severity": "High" if crit_vals[i] < crit_vals[i-1] * 0.2 else "Medium"
                 })

        report = []
        if len(masking_issues) > 10:
            report.append("PSYCHOACOUSTIC ALERT: Deteksi masking berat di area 1k-5kHz.")
            report.append("ADVICE: Jangan cuma naikin EQ instrumen yang 'hilang'. Coba 'scoop' instrumen dominan di area frekuensi tersebut.")
        
        return {
            "masking_points_count": len(masking_issues),
            "findings": report
        }
