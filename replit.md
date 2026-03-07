# Sonus - AI Co-Producer Dashboard

## Overview
Sonus is an AI Co-Producer and Creative Partner tool for music production (targeting VAREON). It provides deep audio analysis, production critique, vibe analysis, VST recipes, and creative suggestions.

## Architecture
- **Backend/Frontend**: FastAPI web app serving a Jinja2 HTML dashboard
- **Entry point**: `src/web/app.py` (serves on port 5000)
- **CLI entry point**: `main.py` (click-based CLI for terminal use)
- **Core logic**: `src/core/brain.py` (SonusBrain class)

## Project Structure
```
src/
  analysis/         - Audio analysis modules (DSP, psychoacoustics, harmonics, etc.)
  bridge/           - Creative context bridge (generative prompt building)
  core/brain.py     - Central SonusBrain orchestrator
  export/           - Label packager
  generation/       - Synth engine (pyo-based, with fallback)
  interface/        - Live audio monitor
  knowledge/        - label_standards.json, vst_recipes.json
  web/
    app.py          - FastAPI web app (port 5000)
    templates/      - index.html dashboard
```

## Dependencies
Core Python packages (in requirements.txt):
- numpy, librosa, scipy, soundfile, pyloudnorm
- essentia (audio analysis)
- mido, music21 (MIDI/notation)
- click, colorama (CLI)
- fastapi, uvicorn, jinja2, python-multipart (web)
- gunicorn (production server)

Note: `aubio` and `pyo` are in requirements.txt but cannot be compiled in this environment. The code has been updated with graceful fallbacks:
- aubio → replaced with librosa-based equivalents
- pyo → wrapped with try/except, degrades gracefully

## Workflow
- **Start application**: `PYTHONPATH=/home/runner/workspace/src python3 src/web/app.py` on port 5000

## Deployment
- Target: autoscale
- Run: gunicorn with uvicorn workers on port 5000
