import numpy as np
import librosa

class SidechainLogic:
    def __init__(self, file_path):
        self.file_path = file_path
        self.y, self.sr = librosa.load(file_path)

    def detect_kick_vs_sub(self):
        """Detect masking between transients (kick) and sub-bass."""
        o = librosa.onset.onset_detect(y=self.y, sr=self.sr)
        onsets_sec = librosa.frames_to_time(o, sr=self.sr)

        S = np.abs(librosa.stft(self.y))
        freqs = librosa.fft_frequencies(sr=self.sr)
        sub_mask = (freqs >= 20) & (freqs <= 80)
        sub_energy = np.mean(S[sub_mask, :], axis=0)
        
        masking_events = []
        for onset in o:
            if onset < len(sub_energy):
                energy_at_onset = sub_energy[onset]
                if energy_at_onset > np.mean(sub_energy) * 1.5:
                    time_sec = librosa.frames_to_time(onset, sr=self.sr)
                    masking_events.append(f"{time_sec:.2f}s")

        report = []
        if len(masking_events) > 5:
            report.append(f"CRITICAL MASKING: {len(masking_events)} Kick vs Sub collisions detected. Check sidechain/ducking.")
        
        return {
            "masking_count": len(masking_events),
            "timestamps": masking_events[:10],
            "findings": report
        }
