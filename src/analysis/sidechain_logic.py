import numpy as np
import librosa
import aubio

class SidechainLogic:
    def __init__(self, file_path):
        self.file_path = file_path
        self.y, self.sr = librosa.load(file_path)

    def detect_kick_vs_sub(self):
        """Deteksi masking antara transien (kick) dan sub-bass."""
        # 1. Onset Detection (Kick)
        o = librosa.onset.onset_detect(y=self.y, sr=self.sr)
        onsets_sec = librosa.frames_to_time(o, sr=self.sr)

        # 2. Sub-Bass Energy (20-80Hz)
        # Filter band-pass sederhana (DSP approach)
        S = np.abs(librosa.stft(self.y))
        freqs = librosa.fft_frequencies(sr=self.sr)
        sub_mask = (freqs >= 20) & (freqs <= 80)
        sub_energy = np.mean(S[sub_mask, :], axis=0)
        
        masking_events = []
        for onset in o:
            # Cek energi sub pada saat onset (frame onset)
            energy_at_onset = sub_energy[onset]
            # Jika energi sub masih tinggi saat kick berbunyi (> threshold)
            if energy_at_onset > np.mean(sub_energy) * 1.5:
                time_sec = librosa.frames_to_time(onset, sr=self.sr)
                masking_events.append(f"{time_sec:.2f}s")

        report = []
        if len(masking_events) > 5:
            report.append(f"CRITICAL MASKING: {len(masking_events)} Kick vs Sub collisions detected. Cek sidechain/ducking lo.")
        
        return {
            "masking_count": len(masking_events),
            "timestamps": masking_events[:10], # 10 pertama
            "findings": report
        }
