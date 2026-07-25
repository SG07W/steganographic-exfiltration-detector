# Steganographic Exfiltration Detector

A simple full-stack project for analyzing images for signs of steganographic hiding techniques.

## Overview

This project combines:
- a FastAPI backend for image analysis
- a React + Vite frontend for uploading and viewing results

## Features

- Upload PNG or JPEG images
- Run LSB analysis
- Run Chi-Square analysis
- View analysis results in the browser

## Project Structure

- backend/ - FastAPI server and analysis modules
- frontend/ - React frontend application
- requirements.txt - Python dependencies

## Setup

### Backend

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the backend:
   ```bash
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```

### Frontend

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Notes

- The frontend is expected to connect to the backend at http://127.0.0.1:8000
- Only PNG and JPEG files are currently supported
