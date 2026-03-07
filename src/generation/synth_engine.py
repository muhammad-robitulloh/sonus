from pyo import *
import numpy as np

class PyoSynthEngine:
    def __init__(self):
        # Server pyo (audio processing)
        self.s = Server(duplex=0).boot()
        self.s.start()

    def generate_sine_preview(self, freq=440, dur=1.0):
        """Menghasilkan nada sine sederhana untuk preview melodi."""
        env = Adsr(attack=0.01, decay=0.1, sustain=0.5, release=0.2, dur=dur, mul=0.3)
        osc = Sine(freq=freq, mul=env).out()
        env.play()
        # In actual usage, we'd record this to a file or play it
        return "Sine preview generated at {} Hz".format(freq)

    def suggest_fm_params(self, carrier=100, ratio=1.5, index=5):
        """Memberikan saran parameter FM Synthesis (Frequency Modulation)."""
        # Suggesting params for a 'Growl' or 'Pluck' sound
        if index > 10:
            return "Saran: Index tinggi (>10) menghasilkan tekstur harmonik yang kompleks/noisy, cocok untuk bass EDM."
        else:
            return "Saran: Ratio 1.5 - 2.0 memberikan karakter suara yang harmonis dan 'clean'."

    def stop(self):
        self.s.stop()
        self.s.shutdown()
