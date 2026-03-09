import numpy as np
import librosa
try:
    import aubio
    AUBIO_AVAILABLE = True
except ImportError:
    AUBIO_AVAILABLE = False
import essentia.standard as es
import os
import subprocess
import tempfile

class AdvancedDSPEngine:
    def __init__(self, file_path):
        self.file_path = file_path
        self._temp_wav = None
        self._working_path = self.file_path

    def _ensure_aubio_compatible(self):
        """Aubio often fails on MP3s in Termux. Convert to WAV if needed."""
        if self.file_path.lower().endswith('.mp3'):
            self._temp_wav = os.path.join(tempfile.gettempdir(), f"sonus_temp_{os.getpid()}.wav")
            # Convert to mono wav 44.1k for best aubio results
            cmd = ["ffmpeg", "-i", self.file_path, "-ar", "44100", "-ac", "1", self._temp_wav, "-y", "-loglevel", "quiet"]
            try:
                subprocess.run(cmd, check=True)
                self._working_path = self._temp_wav
            except Exception as e:
                print(f"⚠️ Failed to convert for Aubio: {e}")
                self._working_path = self.file_path

    def __del__(self):
        if self._temp_wav and os.path.exists(self._temp_wav):
            try:
                os.remove(self._temp_wav)
            except:
                pass

    def get_vibe_analysis(self):
        """Analyzes mood, danceability, and genre using Essentia."""
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
        """Analyzes pitch using aubio if available, otherwise librosa."""
        if AUBIO_AVAILABLE:
            self._ensure_aubio_compatible()
            win_s = 4096
            hop_s = 512
            samplerate = 44100
            
            s = aubio.source(self._working_path, samplerate, hop_s)
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
        else:
            y, sr = librosa.load(self.file_path)
            f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
            pitches = f0[voiced_flag] if voiced_flag is not None else []
            pitches = [p for p in pitches if p > 0]
            return {
                "avg_pitch_hz": float(np.mean(pitches)) if len(pitches) > 0 else 0,
                "max_pitch_hz": float(np.max(pitches)) if len(pitches) > 0 else 0,
                "pitch_count": len(pitches)
            }

    def get_transient_analysis(self):
        """Analyzes transient sharpness using aubio if available, otherwise librosa."""
        if AUBIO_AVAILABLE:
            self._ensure_aubio_compatible()
            hop_s = 512
            s = aubio.source(self._working_path, 0, hop_s)
            samplerate = s.samplerate
            o = aubio.onset("default", 2048, hop_s, samplerate)
            
            onsets = []
            while True:
                samples, read = s()
                if o(samples):
                    onsets.append(o.get_last_s())
                if read < hop_s: break
            
            duration = s.duration / samplerate if samplerate > 0 else 0
            
            return {
                "onset_count": len(onsets),
                "onset_density": len(onsets) / duration if duration > 0 else 0
            }
        else:
            y, sr = librosa.load(self.file_path)
            onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
            onset_times = librosa.frames_to_time(onset_frames, sr=sr)
            duration = librosa.get_duration(y=y, sr=sr)
            
            return {
                "onset_count": len(onset_times),
                "onset_density": len(onset_times) / duration if duration > 0 else 0
            }