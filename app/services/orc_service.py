"""
Order Position Extraction Service

This service extracts order positions from PDF documents using OCR.
"""
from pathlib import Path
from typing import List, Dict, Any

import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path

from app.config.orc_config import DPI, GAUSSIAN_BLUR_KERNEL, LAYOUT, COLUMNS, OCR, ADAPTIVE_THRESHOLD
from app.dto import ExtractionResult, OrderPosition, FieldValue

class OrderPositionExtractionService:
    def extract_from_pdf(self, pdf_path: str) -> ExtractionResult:
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        pages = convert_from_path(
            str(pdf_path),
            dpi=DPI,
            fmt="png"
        )

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

        column_data = self._extract_columns(binary, start_y, page_h)

        return column_data

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
            ADAPTIVE_THRESHOLD["constant"]
        )

    def _extract_columns(
        self,
        binary: np.ndarray,
        start_y: int,
        page_h: int
    ) -> List[OrderPosition]:
        rows = []

        # loop through each row and extract column data
        y = start_y

        row_counter = 1
        stop_rows = False

        while y + LAYOUT["row_height"] < page_h:
            row_data = {
                "y": y,
                "fields": {},
                "row_number": row_counter
            }
            
            for column in COLUMNS:
                roi = binary[y:y + LAYOUT["row_height"], column["x"]:column["x"] + column["width"]]

                if roi.size == 0:
                    continue

                data = pytesseract.image_to_data(
                    roi,
                    lang=OCR["languages"],
                    config=column["tesseract_config"],
                    output_type=Output.DICT
                )

                texts = []
                confidences = []

                for i, conf in enumerate(data["conf"]):
                    if conf != -1:
                        txt = data["text"][i].strip()
                        if txt:
                            texts.append(txt)
                            confidences.append(float(conf))

                text = " ".join(texts)
                avg_confidence = (
                    sum(confidences) / len(confidences)
                    if confidences else 0.0
                )

                # Check if table has ended (e.g. empty article number column)
                if column["name"] == "article_number" and not text:
                    stop_rows = True
                    break

                row_data["fields"][column["name"]] = {
                    "text": text,
                    "confidence": round(avg_confidence, 2)
                }

            # Flag to detect if we are at the end of the table and should stop processing further rows
            if stop_rows:
                break

            rows.append(row_data)

            y += LAYOUT["row_height"]
            row_counter += 1

        return [self._map_to_order_position(row) for row in rows]
    
    def _map_to_order_position(self, row_data: Dict[str, Any]) -> OrderPosition:
        fields = row_data["fields"]

        return OrderPosition(
            article_number=FieldValue(
                value=fields.get("article_number", {}).get("text", ""),
                confidence=fields.get("article_number", {}).get("confidence", 0.0)
            ),
            description=FieldValue(
                value=fields.get("description", {}).get("text", ""),
                confidence=fields.get("description", {}).get("confidence", 0.0)
            ),
            kvk=FieldValue(
                value=fields.get("kvk", {}).get("text", ""),
                confidence=fields.get("kvk", {}).get("confidence", 0.0)
            ),
            wgp=FieldValue(
                value=fields.get("wgp", {}).get("text", ""),
                confidence=fields.get("wgp", {}).get("confidence", 0.0)
            ),
            quantity=FieldValue(
                value=fields.get("quantity", {}).get("text", ""),
                confidence=fields.get("quantity", {}).get("confidence", 0.0)
            ),
            price=FieldValue(
                value=fields.get("price", {}).get("text", ""),
                confidence=fields.get("price", {}).get("confidence", 0.0)
            ),
            total=FieldValue(
                value=fields.get("total", {}).get("text", ""),
                confidence=fields.get("total", {}).get("confidence", 0.0)
            )
        )
    



