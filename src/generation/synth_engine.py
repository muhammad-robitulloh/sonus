import numpy as np

try:
    from pyo import *
    PYO_AVAILABLE = True
except ImportError:
    PYO_AVAILABLE = False

class PyoSynthEngine:
    def __init__(self):
        if PYO_AVAILABLE:
            self.s = Server(duplex=0).boot()
            self.s.start()
        else:
            self.s = None

    def generate_sine_preview(self, freq=440, dur=1.0):
        """Generate a simple sine tone for melody preview."""
        if PYO_AVAILABLE and self.s:
            env = Adsr(attack=0.01, decay=0.1, sustain=0.5, release=0.2, dur=dur, mul=0.3)
            osc = Sine(freq=freq, mul=env).out()
            env.play()
            return "Sine preview generated at {} Hz".format(freq)
        else:
            return f"Sine preview at {freq} Hz (audio playback unavailable in this environment)"

    def suggest_fm_params(self, carrier=100, ratio=1.5, index=5):
        """Provide FM Synthesis parameter suggestions."""
        if index > 10:
            return "Suggestion: High index (>10) produces complex/noisy harmonic texture, great for EDM bass."
        else:
            return "Suggestion: Ratio 1.5-2.0 gives a harmonic and 'clean' sound character."

    def stop(self):
        if PYO_AVAILABLE and self.s:
            self.s.stop()
            self.s.shutdown()
