# RUN WITH: docker compose exec ag-document-intelligence-service-api python /app/scripts/extract_pdf.py

from pdf2image import convert_from_path
from pathlib import Path
import cv2
import numpy as np

PDF_PATH = "/app/scripts/scan_default.pdf"
OUT_DIR = Path("/app/scripts/pages")
OUT_DIR.mkdir(parents=True, exist_ok=True)

pages = convert_from_path(
    PDF_PATH,
    dpi=300,
    fmt="png"
)

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold (VERY important for bad scans)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    return thresh

for i, page in enumerate(pages):
    out = OUT_DIR / f"page_{i+1}.png"

    # Convert PIL image to OpenCV format
    img = np.array(page)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Preprocess the image for better OCR results
    processed_img = preprocess_image(img)

    cv2.imwrite(str(out), processed_img)
    print(f"Saved {out}")

