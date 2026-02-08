import numpy as np

from app.config.orc_config import ROW_PROCESSING

def should_continue_processing(roi: np.ndarray) -> bool:
    if roi.size == 0:
        return False
    
    white_pixels = np.sum(roi == 255) # 255 can be used because the scan is binary
    total_pixels = roi.size
    white_ratio = white_pixels / total_pixels

    # If ROI is mostly white (empty), skip processing
    if white_ratio > ROW_PROCESSING["max_white_pixel_ratio"]:
        return False
    
    black_pixels = np.sum(roi == 0) # 0 can be used because the scan is binary

    # If not enough black pixels, skip processing
    if black_pixels < ROW_PROCESSING["min_required_black_pixels"]:
        return False
    
    return True