#! Note this was written by ChatGPT

import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO
import os

INPUT_PDF = "input.pdf"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)


def degrade_scan(
    img,
    dpi=200,
    blur=1.0,
    noise=5,
    skew=0.5,
    contrast=1.2,
    brightness=-10,
    jpeg_quality=50,
    threshold=False
):
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # DPI reduction
    scale = dpi / 300
    h, w = gray.shape
    gray = cv2.resize(gray, (int(w * scale), int(h * scale)))

    # Blur (FIXED)
    if blur > 0:
        k = int(round(blur * 2))
        # Ensure k is at least 1 and odd
        k = max(1, k)
        if k % 2 == 0:
            k += 1
        gray = cv2.GaussianBlur(gray, (k, k), 0)

    # Noise
    if noise > 0:
        n = np.random.normal(0, noise, gray.shape)
        gray = np.clip(gray + n, 0, 255).astype(np.uint8)

    # Skew
    angle = np.random.uniform(-skew, skew)
    M = cv2.getRotationMatrix2D(
        (gray.shape[1] // 2, gray.shape[0] // 2),
        angle,
        1
    )
    gray = cv2.warpAffine(
        gray,
        M,
        (gray.shape[1], gray.shape[0]),
        borderValue=255
    )

    # Contrast / brightness
    gray = cv2.convertScaleAbs(gray, alpha=contrast, beta=brightness)

    # Fax threshold
    if threshold:
        _, gray = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)

    out = Image.fromarray(gray)

    # JPEG artifacts
    buf = BytesIO()
    out.save(buf, format="JPEG", quality=jpeg_quality)
    buf.seek(0)

    return Image.open(buf)


def process_pdf(name, settings):
    pages = convert_from_path(INPUT_PDF, dpi=300)
    scanned = [degrade_scan(p, **settings) for p in pages]

    scanned[0].save(
        os.path.join(OUT_DIR, f"{name}.pdf"),
        save_all=True,
        append_images=scanned[1:],
        resolution=settings.get("dpi", 150)
    )


if __name__ == "__main__":
    # Very light degradation - barely noticeable
    process_pdf("scan_good", dict(
        dpi=280, blur=0.3, noise=2, skew=0.1,
        contrast=1.05, brightness=-3, jpeg_quality=85
    ))

    # Moderate degradation - looks like a decent office scan
    process_pdf("scan_average", dict(
        dpi=150, blur=0.8, noise=8, skew=0.4,
        contrast=1.15, brightness=-6, jpeg_quality=40
    ))

    # Heavier degradation - noticeably lower quality but still readable
    # (removed threshold to keep it more natural)
    process_pdf("scan_terrible", dict(
        dpi=150, blur=1.5, noise=12, skew=1.2,
        contrast=1.35, brightness=-7, jpeg_quality=35
    ))

    print("Done.")