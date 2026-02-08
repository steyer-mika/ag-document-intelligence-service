################################################################################
#                               Image Processing                               #
################################################################################

# Rescaled Image DPI for better OCR accuracy
DPI = 300

# Gaussian blur kernel size for noise reduction before thresholding
GAUSSIAN_BLUR_KERNEL = (5, 5)

# Adaptive thresholding parameters for binarization
ADAPTIVE_THRESHOLD = {
    "block_size": 31,
    "constant": 15,
}

################################################################################
#                            Row Processing Thresholds                         #
################################################################################

# Configs for determining when to consider the table row to be ended
ROW_PROCESSING = {
    "min_required_black_pixels": 500,
    "max_white_pixel_ratio": 0.95,
}

################################################################################
#                               Layout Detection                               #
################################################################################

LAYOUT = {
    "start_y_first_page": 580,
    "start_y_other_pages": 515,
    "row_x_start": 100,
    "row_height": 255,
    "row_width": 2120,
}


################################################################################
#                             Field Definitions                                #
################################################################################

# Fields: (name, x_row_offset, width, y_row_offset, height)
FIELDS = [
    {
        "name": "article_number",
        "x_row_offset": 1900,
        "width": 310,
        "y_row_offset": 15,
        "height": 50,
        "tesseract_config": "--psm 8 -c tessedit_char_whitelist=0123456789 -c classify_bln_numeric_mode=1",
    },
    {
        "name": "description",
        "x_row_offset": 105,
        "width": 720,
        "y_row_offset": 10,
        "height": 50,
        "tesseract_config": "--psm 7",
    },
    {
        "name": "kvk",
        "x_row_offset": 1150,
        "width": 115,
        "y_row_offset": 10,
        "height": 50,
        "tesseract_config": "--psm 8 -c tessedit_char_whitelist=0123456789.,",
    },
    {
        "name": "wgp",
        "x_row_offset": 1280,
        "width": 140,
        "y_row_offset": 10,
        "height": 50,
        "tesseract_config": "--psm 8 -c tessedit_char_whitelist=0123456789.,",
    },
]


################################################################################
#                                 OCR Settings                                 #
################################################################################

OCR = {
    "languages": "deu+eng",
    "min_confidence": 0.0,
}
