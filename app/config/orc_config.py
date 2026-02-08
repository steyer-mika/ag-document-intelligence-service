################################################################################
#                               Image Processing                               #
################################################################################

DPI = 300

GAUSSIAN_BLUR_KERNEL = (5, 5)

ADAPTIVE_THRESHOLD = {
    "block_size": 31,
    "constant": 15,
}

################################################################################
#                               Layout Detection                               #
################################################################################

LAYOUT = {
    "start_y_first_page": 1905,
    "start_y_other_pages": 345,
    "row_height": 83,
}


################################################################################
#                             Column Definitions                               #
################################################################################

COLUMNS = [
    {
        "name": "article_number",
        "x": 165,
        "width": 260,
        "tesseract_config": "--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-",
    },
    {
        "name": "description",
        "x": 425,
        "width": 830,
        "tesseract_config": "--psm 6 -c preserve_interword_spaces=1",
    },
    {
        "name": "kvk",
        "x": 1255,
        "width": 140,
        "tesseract_config": "--psm 8 -c classify_bln_numeric_mode=1",
    },
    {
        "name": "wgp",
        "x": 1395,
        "width": 140,
        "tesseract_config": "--psm 8 -c classify_bln_numeric_mode=1",
    },
]


################################################################################
#                                 OCR Settings                                 #
################################################################################

OCR = {
    "languages": "deu+eng",
    "min_confidence": 0.0,
}
