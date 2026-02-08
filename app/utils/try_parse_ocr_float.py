import re
from typing import Optional

def try_parse_ocr_float(text: str) -> Optional[float]:
    if not text:
        return None

    # 1. Keep only digits, space, comma, dot
    s = re.sub(r"[^0-9., ]", "", text).strip()
    if not s:
        return None

    # 2. Handle space as decimal separator (e.g. "149 50")
    if s.count(" ") == 1 and "." not in s and "," not in s:
        s = s.replace(" ", ".")
    else:
        s = s.replace(" ", "")

    # 3. Normalize comma → dot
    s = s.replace(",", ".")

    # 4. Reject multiple dots
    if s.count(".") > 1:
        return None

    # 5. Reject leading or trailing dot
    if s.startswith(".") or s.endswith("."):
        return None

    # 6. Final validation
    if not re.fullmatch(r"\d+(\.\d+)?", s):
        return None

    try:
        return float(s)
    except ValueError:
        return None
