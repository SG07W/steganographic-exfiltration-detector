# Steganographic Exfiltration Detector

A full-stack image analysis tool that detects potential steganographic embedding by running lightweight statistical checks on uploaded images.

## What it does

The project combines:
- a FastAPI backend for image scanning and analysis
- a React + Vite frontend for upload and result viewing

It currently performs:
- LSB bit-plane analysis
- Chi-square histogram analysis
- risk scoring and verdict generation

## Project structure

- backend/ - FastAPI app and analysis modules
- frontend/ - React/Vite client
- requirements.txt - Python dependencies

## Requirements

- Python 3.10+
- Node.js 18+

## Setup

### 1. Backend

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/scan

### 2. Frontend

Install frontend dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

- http://127.0.0.1:5173/

## Notes

- The frontend expects the backend at http://127.0.0.1:8000
- Supported image formats are PNG and JPEG
- For a quick test, upload an image and click Analyze Image
