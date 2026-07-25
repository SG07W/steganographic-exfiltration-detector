from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import shutil
import tempfile
from pathlib import Path

try:
    from backend.lsb import LSBAnalyzer
    from backend.chi_square import ChiSquareAnalyzer
    from backend.risk_engine import RiskEngine
except ImportError:
    from lsb import LSBAnalyzer
    from chi_square import ChiSquareAnalyzer
    from risk_engine import RiskEngine

app = FastAPI(title="Steganographic Exfiltration Detector")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
BACKEND_PORT = 8000

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
    if file.filename is None:
        raise HTTPException(status_code=400, detail="A filename is required.")

    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PNG and JPEG images are supported.",
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name

    try:
        lsb = LSBAnalyzer(temp_path)
        lsb_result = {
            "bit_statistics": lsb.bit_statistics(),
            "entropy": lsb.entropy(),
        }

        chi = ChiSquareAnalyzer(temp_path)
        chi_result = chi.analyze()
        risk = RiskEngine(lsb_result, chi_result)
        risk_result = risk.calculate()

        return JSONResponse(
            content={
                "status": "success",
                "filename": file.filename,
                "verdict": risk_result["verdict"],
                "risk_score": risk_result["risk_score"],
                "lsb_risk": risk_result["lsb_risk"],
                "lsb_message": risk_result["lsb_message"],
                "chi_risk": risk_result["chi_risk"],
                "chi_message": risk_result["chi_message"],
                "entropy_risk": risk_result["entropy_risk"],
                "entropy_message": risk_result["entropy_message"],
                "lsb": lsb_result,
                "chi_square": chi_result,
            }
        )
    finally:
        Path(temp_path).unlink(missing_ok=True)