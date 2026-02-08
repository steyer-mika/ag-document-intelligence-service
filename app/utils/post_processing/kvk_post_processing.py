from typing import Optional
from app.utils.parse_string_to_float import parse_string_to_float

from app.config.field_config import KVK_DIGESTS_AFTER_DECIMAL

def post_process_kvk(kvk_value: str) -> Optional[float]:
    result = parse_string_to_float(kvk_value)

    if result is None:
        return None

    value, digits_after_decimal = result

    if digits_after_decimal == 0:
        # If there are no digits, assume orc misinterpreted the decimal point and divide by 10**KVK_DIGESTS_AFTER_DECIMAL
        return value / (10 ** KVK_DIGESTS_AFTER_DECIMAL)

    # Value parsed correctly
    return value
