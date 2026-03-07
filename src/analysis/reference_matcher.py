import numpy as np
import librosa
import os

class ReferenceMatcher:
    def __init__(self, target_path, reference_path):
        self.target_path = target_path
        self.reference_path = reference_path
        
    def compare_spectrum(self):
        """Compare the spectral balance of target vs reference track."""
        # Load both tracks (limit duration for speed)
        y_tgt, sr_tgt = librosa.load(self.target_path, duration=60)
        y_ref, sr_ref = librosa.load(self.reference_path, duration=60)
        
        # Calculate Power Spectral Density (PSD)
        S_tgt = np.abs(librosa.stft(y_tgt))
        S_ref = np.abs(librosa.stft(y_ref))
        
        # Normalize energy
        S_tgt = S_tgt / np.max(S_tgt)
        S_ref = S_ref / np.max(S_ref)
        
        freqs = librosa.fft_frequencies(sr=sr_tgt)
        avg_tgt = np.mean(S_tgt, axis=1)
        avg_ref = np.mean(S_ref, axis=1)
        
        # Define Frequency Bands
        bands = {
            "Sub (20-60Hz)": (20, 60),
            "Bass (60-250Hz)": (60, 250),
            "Low Mids (250-500Hz)": (250, 500),
            "Mids (500-2kHz)": (500, 2000),
            "High Mids (2k-4kHz)": (2000, 4000),
            "Presence (4k-6kHz)": (4000, 6000),
            "Brilliance (6k-20kHz)": (6000, 20000)
        }
        
        report = []
        comparison_data = {}
        
        for name, (low, high) in bands.items():
            mask = (freqs >= low) & (freqs <= high)
            
            # Calculate average energy in band
            band_tgt = np.mean(avg_tgt[mask])
            band_ref = np.mean(avg_ref[mask])
            
            # Calculate difference in dB (approx)
            # Add epsilon to avoid log(0)
            diff_db = 10 * np.log10(band_tgt + 1e-6) - 10 * np.log10(band_ref + 1e-6)
            comparison_data[name] = diff_db
            
            if diff_db < -3.0:
                report.append(f"LACKING: {name} is too quiet ({diff_db:.1f}dB) vs reference.")
            elif diff_db > 3.0:
                report.append(f"EXCESS: {name} is too loud (+{diff_db:.1f}dB) vs reference.")
                
        return {
            "band_comparison": comparison_data,
            "findings": report
        }
