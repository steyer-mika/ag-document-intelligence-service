import re
from typing import Optional, Tuple

def parse_string_to_float(value: Optional[str]) -> Optional[Tuple[float, int]]:
    if not value:
        return None

    # 1. Keep only digits, space, comma, dot
    s = re.sub(r"[^0-9., ]", "", value).strip()
    if not s:
        return None

    # 2. Handle space as decimal separator (e.g. "149 50")
    if s.count(" ") == 1 and "." not in s and "," not in s:
        s = s.replace(" ", ".")
    else:
        s = s.replace(" ", "")

    # 3. Normalize comma → dot
    s = s.replace(",", ".")

    # 4. Remove leading and trailing dots
    s = s.strip(".")

    # 5. Reject multiple dots
    if s.count(".") > 1:
        return None

    # 6. Final validation
    if not re.fullmatch(r"\d+(\.\d+)?", s):
        return None

    try:
        f = float(s)
        # Count digits after decimal
        if "." in s:
            digits_after_dot = len(s.split(".")[1])
        else:
            digits_after_dot = 0
        return f, digits_after_dot
    except ValueError:
        return None
