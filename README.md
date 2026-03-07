# Sonus: AI Co-Producer & Creative Partner

Sonus is a specialized AI assistant designed for music producers and developers. Acting as a collaborative partner, Sonus provides insights, feedback, and creative suggestions directly within your workflow.

## Features

### 1. Diskusi (Creative Discussion)
- **Lyric Analysis:** Evaluate emotional impact, rhyme schemes, and thematic consistency.
- **Melody Ideas:** Generate motifs based on mood or key.
- **Song Structure:** Suggest arrangements (Verse-Chorus-Bridge) tailored to genre.

### 2. Produksi (Production Engine)
- **Mixing Suggestions:** Frequency analysis to detect masking/mud via FFT.
- **Mastering Recommendations:** Dynamic range and loudness analysis.
- **Harmony Analysis:** Chord progression suggestions and music theory insights.
- **Sound Synthesis:** Basic waveform generation and envelope shaping ideas.

### 3. Teknis (Technical Integration)
- **DAW Integration:** Generates standard MIDI files (.mid) compatible with any DAW.
- **Audio Analysis:** BPM detection, Key detection using Librosa/Essentia.
- **VST Plugin Support:** (Planned) Analyzing plugin chains or suggesting settings.

## Architecture

- **Core:** Central logic and state management.
- **Analysis:** DSP algorithms (Librosa, NumPy).
- **Generation:** Algorithmic composition (Music21, Mido).
- **Interface:** Interactive CLI with rich text output.

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run Sonus
python main.py
```
