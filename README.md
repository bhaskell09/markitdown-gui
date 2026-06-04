# MarkItDown GUI

A desktop frontend for Microsoft's [`markitdown`](https://github.com/microsoft/markitdown)
library, with optional NVIDIA NIM-powered OCR / image understanding.

Convert PDFs, Office documents, images, HTML, and more into clean Markdown — with a
drag-and-drop queue and a live, themed preview.

## Features
- Drag-and-drop file queue with per-file status (pending / converting / done / error)
- Optional OCR via NVIDIA NIM (Nemotron vision models)
- Live Markdown preview (rendered + raw) with copy / save
- Light / Dark / System themes
- Batch conversion that never halts on a single failed file

## Setup
```bash
pip install -r requirements.txt
```

Create your environment file and add your NVIDIA API key (only needed for OCR):
```bash
copy .env.example .env      # Windows
# cp .env.example .env       # macOS / Linux
```
Then edit `.env`:
```
NVIDIA_API_KEY=nvapi-your-key-here
```
Get a key at <https://build.nvidia.com> (free tier available). You can also paste the key
later via the gear (settings) dialog in the app.

## Run
```bash
python main.py
```

## Notes
- OCR is optional. Turn it **off** to convert documents that don't need image understanding
  (no API key required).
- Output `.md` files are written next to each source file by default, or to a folder you
  choose in the settings bar.
- Settings (theme, model, OCR, output folder) persist in `config.json`, created on first run.
