import numpy as np
import librosa
import aubio

class EmotionalDensity:
    def __init__(self, file_path):
        self.y, self.sr = librosa.load(file_path)

    def analyze_tension_release(self):
        """Map tension and release based on onset density and spectral brightness."""
        hop_length = 512
        
        # 1. Onset Density (Rhythmic Activity) - Normalized 0-1
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr, hop_length=hop_length)
        onset_norm = (onset_env - np.min(onset_env)) / (np.max(onset_env) - np.min(onset_env))
        
        # 2. Spectral Centroid (Brightness/Intensity) - Normalized 0-1
        centroid = librosa.feature.spectral_centroid(y=self.y, sr=self.sr, hop_length=hop_length)[0]
        centroid_norm = (centroid - np.min(centroid)) / (np.max(centroid) - np.min(centroid))
        
        # Combined Tension Index (Density)
        # Weighting: 60% Onset (Rhythm), 40% Centroid (Tone)
        tension_curve = (onset_norm * 0.6) + (centroid_norm * 0.4)
        
        # Analyze Sections (Simplified heuristics for Intro vs Drop)
        # Assume Drop is the loudest/densest part usually
        avg_tension = np.mean(tension_curve)
        peak_tension = np.max(tension_curve)
        
        # Find potential Drop (highest energy segment)
        # Using a rolling window would be better, but simplified for now
        window_size = int(len(tension_curve) / 10) # Divide song into 10 parts
        sections = [np.mean(tension_curve[i:i+window_size]) for i in range(0, len(tension_curve), window_size)]
        
        drop_index = np.argmax(sections)
        intro_tension = sections[0]
        drop_tension = sections[drop_index]
        
        report = []
        contrast = drop_tension - intro_tension
        
        if contrast < 0.2:
            report.append("DENSITY ISSUE: Kurang kontras antara Intro dan Drop. Drop lo kerasa 'datar' karena Intro terlalu padat.")
            report.append("ADVICE: Kurangi elemen di Intro/Build-up. Biarkan Drop jadi satu-satunya momen 'Full Gravity'.")
        else:
             report.append("GOOD CONTRAST: Dinamika lagu lo sehat. Drop terasa signifikan lebih berat dari Intro.")

        return {
            "intro_density": float(intro_tension),
            "drop_density": float(drop_tension),
            "contrast_ratio": float(contrast),
            "findings": report
        }
