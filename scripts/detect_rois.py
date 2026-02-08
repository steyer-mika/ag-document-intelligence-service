# RUN WITH:
# docker compose exec ag-document-intelligence-service-api python /app/scripts/detect_rois.py

from pdf2image import convert_from_path
from pathlib import Path
import cv2
import numpy as np

PDF_PATH = "/app/scripts/20260129_154217.pdf"
OUT_DIR = Path("/app/scripts/debug")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DPI = 300

# =====================
# HARD-CODED LAYOUT
# =====================

# Y-start differs for first page vs others
START_Y_FIRST_PAGE = 580
START_Y_OTHER_PAGES = 515

ROW_X_START = 100
ROW_HEIGHT = 255
ROW_WIDTH = 2120

MIN_REQUIRED_BLACK_PIXELS_TO_PROCESS = 500
MAX_WHITE_PIXEL_RATIO_TO_PROCESS = 0.95

# Fields: (name, x row offset, width, y row offset, height)
FIELDS = [
    ("article_number", 1900, 310, 15, 50),
    ("description", 105, 720, 10, 50),
    ("kvk", 1150, 115, 10, 50),
    ("wgp", 1280, 140, 10, 50),
]

COLORS = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
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

def should_continue_processing(roi):
    white_pixels = np.sum(roi == 255)
    total_pixels = roi.size
    white_ratio = white_pixels / total_pixels

    print(f"White pixel ratio: {white_ratio:.2f}")

    if white_ratio > MAX_WHITE_PIXEL_RATIO_TO_PROCESS:
        return False
    
    black_pixels = np.sum(roi == 0)
    print(f"Black pixels: {black_pixels}, Minimum required: {MIN_REQUIRED_BLACK_PIXELS_TO_PROCESS}")

    if black_pixels < MIN_REQUIRED_BLACK_PIXELS_TO_PROCESS:
        return False
    
    return True

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

    y = start_y
    row_idx = 0
    
    # Loop through each row
    while y + ROW_HEIGHT < page_h:
        row_roi = binary[y:y + ROW_HEIGHT, ROW_X_START:ROW_X_START + ROW_WIDTH]
        
        if row_roi.size == 0:
            break

        empty_field_count = 0
        
        for field_idx, (name, rel_x, w, rel_y, h) in enumerate(FIELDS):
            abs_x = ROW_X_START + rel_x
            abs_y = y + rel_y
            
            # Extract field ROI from the binary image
            field_roi = binary[abs_y:abs_y + h, abs_x:abs_x + w]

            if field_roi.size == 0:
                continue

            should_continue = should_continue_processing(field_roi)

            if not should_continue:
                empty_field_count += 1
                continue

            # Draw rectangle on debug image
            color = COLORS[field_idx % len(COLORS)]
            cv2.rectangle(
                debug,
                (abs_x, abs_y),
                (abs_x + w, abs_y + h),
                color,
                2
            )

        # If most of the fields are empty, we can assume the table has ended
        # (why most and not all? Because its a scan and someone could have written something by hand)
        if empty_field_count >= len(FIELDS) - 1:
            break

        y += ROW_HEIGHT
        row_idx += 1

    out = OUT_DIR / f"page_{page_idx + 1}_rois.png"
    cv2.imwrite(str(out), debug)
    print(f"Saved {out}")