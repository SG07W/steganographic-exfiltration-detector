from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import tempfile
import shutil
from pathlib import Path

try:
    from backend.lsb import LSBAnalyzer
    from backend.chi_square import ChiSquareAnalyzer
except ImportError:
    from lsb import LSBAnalyzer
    from chi_square import ChiSquareAnalyzer

app = FastAPI(title="Steganographic Exfiltration Detector")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
BACKEND_PORT = 8001

# CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Steganography Detector API Running"}


@app.post("/scan")
async def scan_image(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PNG and JPEG images are supported."
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name

    try:
        # LSB Analysis
        lsb = LSBAnalyzer(temp_path)

        lsb_result = {
            "bit_statistics": lsb.bit_statistics(),
            "entropy": lsb.entropy()
        }

        # Chi-Square Analysis
        chi = ChiSquareAnalyzer(temp_path)
        chi_result = chi.analyze()

        return JSONResponse(
            content={
                "status": "success",
                "filename": file.filename,
                "lsb": lsb_result,
                "chi_square": chi_result
            }
        )

    finally:
        Path(temp_path).unlink(missing_ok=True)