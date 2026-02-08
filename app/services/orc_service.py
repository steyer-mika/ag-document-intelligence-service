from pathlib import Path
from typing import List, Dict, Any

import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path

from app.config.orc_config import (
    DPI,
    GAUSSIAN_BLUR_KERNEL,
    LAYOUT,
    FIELDS,
    OCR,
    ADAPTIVE_THRESHOLD,
)
from app.dto import ExtractionResult, OrderPosition, FieldValue
from app.utils.orc_should_continue_processing import should_continue_processing

class OrderPositionExtractionService:
    def __init__(self):
        self.row_count = 1

    def extract_from_pdf(self, pdf_path: str) -> ExtractionResult:
        self.row_count = 1 # Reset row count for each new PDF

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        pages = convert_from_path(str(pdf_path), dpi=DPI, fmt="png")

        all_positions = []

        for page_index, page in enumerate(pages):
            positions = self._process_page(page, page_index)
            all_positions.extend(positions)

        return ExtractionResult(
            positions=all_positions,
            total_pages=len(pages),
        )

    def _process_page(self, page, page_index: int) -> List[OrderPosition]:
        img = np.array(page)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        binary = self._preprocess_image(img)

        start_y = (
            LAYOUT["start_y_first_page"]
            if page_index == 0
            else LAYOUT["start_y_other_pages"]
        )

        page_h, page_w = binary.shape

        rows = self._extract_rows(binary, start_y, page_h, page_index)

        return [self._map_to_order_position(row) for row in rows]

    def _preprocess_image(self, img: np.ndarray) -> np.ndarray:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        gray = cv2.GaussianBlur(gray, GAUSSIAN_BLUR_KERNEL, 0)

        # Apply adaptive thresholding to get binary image
        return cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            ADAPTIVE_THRESHOLD["block_size"],
            ADAPTIVE_THRESHOLD["constant"],
        )

    def _extract_rows(
        self, binary: np.ndarray, start_y: int, page_h: int, page_index: int
    ) -> List[Dict[str, Any]]:
        rows = []
        y = start_y

        while y + LAYOUT["row_height"] < page_h:
            row_data = {
                "y": y,
                "page": page_index + 1,
                "fields": {},
                "row_number": self.row_count,
            }

            empty_field_count = 0

            # Process each field in the row
            for field in FIELDS:
                # Calculate absolute coordinates
                abs_x = LAYOUT["row_x_start"] + field["x_row_offset"]
                abs_y = y + field["y_row_offset"]

                # Extract field ROI from the binary image
                field_roi = binary[
                    abs_y : abs_y + field["height"],
                    abs_x : abs_x + field["width"],
                ]

                if field_roi.size == 0:
                    continue

                # Check if field should be processed
                if not should_continue_processing(field_roi):
                    empty_field_count += 1
                    row_data["fields"][field["name"]] = {
                        "text": "",
                        "confidence": 0.0,
                    }
                    continue

                # Run OCR on the field
                try:
                    data = pytesseract.image_to_data(
                        field_roi,
                        lang=OCR["languages"],
                        config=field["tesseract_config"],
                        output_type=Output.DICT,
                    )

                    # Extract text and calculate confidence
                    texts = []
                    confidences = []

                    for i, conf in enumerate(data["conf"]):
                        if conf != -1:  # -1 means no detection
                            txt = data["text"][i].strip()
                            if txt:
                                texts.append(txt)
                                confidences.append(float(conf))

                    text = " ".join(texts)
                    avg_confidence = (
                        sum(confidences) / len(confidences) if confidences else 0.0
                    )

                    row_data["fields"][field["name"]] = {
                        "text": text,
                        "confidence": round(avg_confidence, 2),
                    }

                except Exception as e:
                    print(
                        f"Error processing field '{field['name']}' on page {page_index + 1}, row {self.row_count}: {e}"
                    )
                    row_data["fields"][field["name"]] = {
                        "text": "",
                        "confidence": 0.0,
                        "error": str(e),
                    }

            # If most of the fields are empty, we can assume the table has ended
            # (why most and not all? Because it's a scan and someone could have written something by hand)
            if empty_field_count >= len(FIELDS) - 1:
                break

            rows.append(row_data)

            y += LAYOUT["row_height"]
            self.row_count += 1

        return rows

    def _map_to_order_position(self, row_data: Dict[str, Any]) -> OrderPosition:
        fields = row_data["fields"]

        return OrderPosition(
            position_number=row_data["row_number"],
            article_number=FieldValue(
                value=fields.get("article_number", {}).get("text", ""),
                confidence=fields.get("article_number", {}).get("confidence", 0.0),
            ),
            description=FieldValue(
                value=fields.get("description", {}).get("text", ""),
                confidence=fields.get("description", {}).get("confidence", 0.0),
            ),
            kvk=FieldValue(
                value=fields.get("kvk", {}).get("text", ""),
                confidence=fields.get("kvk", {}).get("confidence", 0.0),
            ),
            wgp=FieldValue(
                value=fields.get("wgp", {}).get("text", ""),
                confidence=fields.get("wgp", {}).get("confidence", 0.0),
            ),
        )