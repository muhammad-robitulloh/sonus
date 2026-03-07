import numpy as np
import librosa
import aubio
import essentia.standard as es

class AdvancedDSPEngine:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_vibe_analysis(self):
        """Menganalisis suasana (mood), danceability, dan genre menggunakan Essentia."""
        loader = es.MonoLoader(filename=self.file_path)
        audio = loader()

        danceability = es.Danceability()(audio)[0]
        rhythm_extractor = es.RhythmExtractor2013()
        bpm, clicks, confidence, estimates, bpm_intervals = rhythm_extractor(audio)
        
        vibe = "Energetic" if danceability > 1.2 else "Chill/Atmospheric"
        
        return {
            "danceability": float(danceability),
            "vibe_estimate": vibe,
            "bpm_confidence": float(confidence),
            "tempo": float(bpm)
        }

    def get_pitch_trajectory(self):
        """Menganalisis pitch menggunakan Aubio (sangat akurat)."""
        win_s = 4096
        hop_s = 512
        samplerate = 44100
        
        s = aubio.source(self.file_path, samplerate, hop_s)
        samplerate = s.samplerate
        pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
        pitch_o.set_unit("Hz")
        pitch_o.set_tolerance(0.8)

        pitches = []
        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            if pitch_o.get_confidence() > 0.8:
                pitches.append(pitch)
            if read < hop_s: break
            
        return {
            "avg_pitch_hz": float(np.mean(pitches)) if pitches else 0,
            "max_pitch_hz": float(np.max(pitches)) if pitches else 0,
            "pitch_count": len(pitches)
        }

    def get_transient_analysis(self):
        """Menganalisis ketajaman transien (kick/snare) menggunakan Aubio."""
        hop_s = 512
        s = aubio.source(self.file_path, 0, hop_s)
        samplerate = s.samplerate
        o = aubio.onset("default", 2048, hop_s, samplerate)
        
        onsets = []
        while True:
            samples, read = s()
            if o(samples):
                onsets.append(o.get_last_s())
            if read < hop_s: break
            
        return {
            "onset_count": len(onsets),
            "onset_density": len(onsets) / (s.duration / samplerate) if s.duration > 0 else 0
        }