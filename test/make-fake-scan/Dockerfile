FROM python:3.11-slim

# Install system deps (Poppler + OpenCV deps)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --no-cache-dir \
    pdf2image \
    pillow \
    numpy \
    opencv-python-headless

WORKDIR /app

COPY fake_scan_pdf.py .
COPY input.pdf .

CMD ["python", "fake_scan_pdf.py"]
