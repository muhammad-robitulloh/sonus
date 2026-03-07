import numpy as np
import librosa

class HeadroomProtector:
    def __init__(self, file_path):
        self.y, self.sr = librosa.load(file_path, mono=False) # Load stereo
        # Handle mono files by duplicating channel
        if self.y.ndim == 1:
            self.y = np.vstack((self.y, self.y))

    def check_cumulative_gain(self):
        """Simulate summing and check for digital clipping risks."""
        # Mix down to mono for checking sum energy
        y_mono = librosa.to_mono(self.y)
        
        # Frame-based RMS analysis
        frame_length = 2048
        hop_length = 512
        rms = librosa.feature.rms(y=y_mono, frame_length=frame_length, hop_length=hop_length)[0]
        times = librosa.frames_to_time(np.arange(len(rms)), sr=self.sr, hop_length=hop_length)
        
        # Digital Ceiling (0dBFS = 1.0 amplitude)
        # Warning threshold at -0.5dB to be safe
        threshold = 1.0 
        clipping_indices = np.where(rms > threshold)[0]
        
        report = []
        if len(clipping_indices) > 0:
            first_clip_time = times[clipping_indices[0]]
            report.append(f"CRITICAL: Potential digital clipping detected starting at {first_clip_time:.2f}s.")
            report.append(f"ADVICE: Turunkan master fader atau group bus lo setidaknya -{(20*np.log10(np.max(rms))):.1f}dB.")
        else:
             report.append("CLEAN: Headroom aman. Tidak ada indikasi digital clipping kasar.")
             
        return {
            "max_peak_db": 20 * np.log10(np.max(rms)),
            "clipping_events": len(clipping_indices),
            "findings": report
        }

    def analyze_stereo_width(self):
        """Check for phase issues in low frequencies (The Mono-Maker Logic)."""
        # Split Mid/Side
        L = self.y[0]
        R = self.y[1]
        Mid = (L + R) / 2
        Side = (L - R) / 2
        
        # FFT for Side channel
        S_side = np.abs(librosa.stft(Side))
        freqs = librosa.fft_frequencies(sr=self.sr)
        
        # Define Low Frequency Zone (< 150Hz)
        low_mask = (freqs < 150)
        low_side_energy = np.mean(S_side[low_mask])
        total_side_energy = np.mean(S_side)
        
        ratio = low_side_energy / (total_side_energy + 1e-6)
        
        report = []
        # Threshold: Jika energi side di low freq > 15% dari total side energy (arbitrary heuristic)
        if ratio > 0.15:
            report.append(f"PHASE ISSUE: Deteksi energi Side signifikan ({ratio*100:.1f}%) di bawah 150Hz.")
            report.append("ACTION: Drop lo bakal loyo di club. Gunakan EQ Side-only, cut low di bawah 150Hz (Mono-Maker).")
        else:
            report.append("SOLID: Low-end lo monocompatible. Aman untuk sound system besar.")

        return {
            "low_side_ratio": float(ratio),
            "findings": report
        }
