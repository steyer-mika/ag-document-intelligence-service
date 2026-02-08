# RUN WITH:
# docker compose exec ag-document-intelligence-service-api python /app/scripts/detect_rois.py

from pdf2image import convert_from_path
from pathlib import Path
import cv2
import numpy as np

PDF_PATH = "/app/scripts/scan_default.pdf"
OUT_DIR = Path("/app/scripts/debug")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DPI = 300

# =====================
# HARD-CODED LAYOUT
# =====================

# Y-start differs for first page vs others
START_Y_FIRST_PAGE = 1905
START_Y_OTHER_PAGES = 345

ROW_HEIGHT = 83
WHITE_THRESHOLD = 0.95  # % of white pixels to stop

# Columns: (x, width)
COLUMNS = [
    ("article_number", 165, 260),
    ("description", 425, 830),
    ("kvk", 1255, 140),
    ("wgp", 1395, 140),
]

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]

# =====================
# HELPERS
# =====================

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    return cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

# =====================
# MAIN
# =====================

pages = convert_from_path(PDF_PATH, dpi=DPI, fmt="png")

for page_idx, page in enumerate(pages):
    print(f"Processing page {page_idx + 1}")

    img = np.array(page)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    binary = preprocess_image(img)

    debug = img.copy()

    start_y = (
        START_Y_FIRST_PAGE
        if page_idx == 0
        else START_Y_OTHER_PAGES
    )

    page_h, page_w = binary.shape

    for col_idx, (name, x, w) in enumerate(COLUMNS):
        color = COLORS[col_idx % len(COLORS)]
        y = start_y

        while y + ROW_HEIGHT < page_h:
            roi = binary[y:y + ROW_HEIGHT, x:x + w]

            if roi.size == 0:
                break

            # Draw rectangle
            cv2.rectangle(
                debug,
                (x, y),
                (x + w, y + ROW_HEIGHT),
                color,
                2
            )

            y += ROW_HEIGHT

    out = OUT_DIR / f"page_{page_idx + 1}_rois.png"
    cv2.imwrite(str(out), debug)
    print(f"Saved {out}")
