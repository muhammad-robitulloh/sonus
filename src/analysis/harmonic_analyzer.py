import numpy as np
import librosa

class HarmonicAnalyzer:
    def __init__(self, file_path):
        self.y, self.sr = librosa.load(file_path)

    def analyze_harmonics(self):
        """Analyze odd vs even harmonics and suggest saturation strategies."""
        S = np.abs(librosa.stft(self.y))
        avg_S = np.mean(S, axis=1)
        freqs = librosa.fft_frequencies(sr=self.sr)
        
        # Find Fundamental Frequency (Peak in FFT)
        fundamental_idx = np.argmax(avg_S)
        fundamental_f = freqs[fundamental_idx]
        
        # Look for harmonics (multiples)
        harmonics = []
        for n in range(2, 6): # Check up to 5th harmonic
            target_f = fundamental_f * n
            if target_f >= self.sr / 2: break
            
            # Find closest index to target frequency
            idx = (np.abs(freqs - target_f)).argmin()
            harmonics.append({
                "n": n,
                "val": float(avg_S[idx]) / (avg_S[fundamental_idx] + 1e-6)
            })

        even_h = [h['val'] for h in harmonics if h['n'] % 2 == 0]
        odd_h = [h['val'] for h in harmonics if h['n'] % 2 != 0]
        
        avg_even = np.mean(even_h) if even_h else 0
        avg_odd = np.mean(odd_h) if odd_h else 0
        
        report = []
        if avg_even < 0.05 and avg_odd < 0.05:
            report.append("STERILE ALERT: Suara terlalu bersih/plastik (Massa tipis).")
            report.append("ADVICE: Tambahin 'Tape Saturation' untuk harmonisa ganjil (grit) atau 'Tube Drive' untuk harmonisa genap (warmth).")
        elif avg_odd > avg_even * 2:
            report.append("HARSH ALERT: Harmonisa ganjil terlalu dominan. Suara mungkin terlalu tajam/berisik.")
            
        return {
            "fundamental_hz": float(fundamental_f),
            "even_ratio": float(avg_even),
            "odd_ratio": float(avg_odd),
            "findings": report
        }
        
    def transient_check(self):
        """Check for aggressive transients that might stress the master limiter."""
        rms = librosa.feature.rms(y=self.y)[0]
        peak = np.max(np.abs(self.y))
        avg_rms = np.mean(rms)
        crest = 20 * np.log10(peak / (avg_rms + 1e-6))
        
        report = []
        if crest > 15: # Very sharp peaks
            report.append("LIMITER STRESS: Transien (Kick/Snare) terlalu tajam.")
            report.append("ADVICE: Lembutkan transien drum lo di FLM (soft clip atau manual volume automation) sebelum masuk master, biar limiter nggak 'pumping'.")
            
        return {
            "crest_factor": float(crest),
            "findings": report
        }
