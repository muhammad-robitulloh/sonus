import numpy as np
import librosa

class EmotionalDensity:
    def __init__(self, file_path):
        self.y, self.sr = librosa.load(file_path)

    def analyze_tension_release(self):
        """Map tension and release based on onset density and spectral brightness."""
        hop_length = 512
        
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr, hop_length=hop_length)
        onset_norm = (onset_env - np.min(onset_env)) / (np.max(onset_env) - np.min(onset_env) + 1e-9)
        
        centroid = librosa.feature.spectral_centroid(y=self.y, sr=self.sr, hop_length=hop_length)[0]
        centroid_norm = (centroid - np.min(centroid)) / (np.max(centroid) - np.min(centroid) + 1e-9)
        
        min_len = min(len(onset_norm), len(centroid_norm))
        tension_curve = (onset_norm[:min_len] * 0.6) + (centroid_norm[:min_len] * 0.4)
        
        avg_tension = np.mean(tension_curve)
        peak_tension = np.max(tension_curve)
        
        window_size = max(1, int(len(tension_curve) / 10))
        sections = [np.mean(tension_curve[i:i+window_size]) for i in range(0, len(tension_curve), window_size)]
        
        drop_index = np.argmax(sections)
        intro_tension = sections[0]
        drop_tension = sections[drop_index]
        
        report = []
        contrast = drop_tension - intro_tension
        
        if contrast < 0.2:
            report.append("DENSITY ISSUE: Low contrast between Intro and Drop. Drop feels flat because Intro is too dense.")
            report.append("ADVICE: Reduce elements in Intro/Build-up. Let the Drop be the only 'Full Gravity' moment.")
        else:
            report.append("GOOD CONTRAST: Song dynamics are healthy. Drop feels significantly heavier than the Intro.")

        return {
            "intro_density": float(intro_tension),
            "drop_density": float(drop_tension),
            "contrast_ratio": float(contrast),
            "findings": report
        }
