import re
from typing import Optional, Union

def amount_to_float(text: Union[str, None]) -> Optional[float]:
    """
    Convert an OCR-extracted amount string to a float.
    
    Handles common OCR pitfalls such as:
    - Currency symbols (€, $, £, etc.)
    - Comma as decimal separator (European format: "18,90")
    - Period as thousands separator (European format: "1.234,56")
    - Comma as thousands separator (US format: "1,234.56")
    - Mixed or confused separators
    - Whitespace and extra characters
    - 'O' or 'o' interpreted as '0'
    - 'l' or 'I' interpreted as '1'
    - 'S' or 's' interpreted as '5'
    - 'B' interpreted as '8'
    
    Args:
        text: The OCR-extracted string containing an amount
        
    Returns:
        The parsed float value, or None if parsing fails
    """
    if text is None or not isinstance(text, str):
        return None
    
    # Strip whitespace and normalize
    text = text.strip()
    
    if not text:
        return None
    
    # Remove currency symbols and common noise
    currency_symbols = r'[€$£¥₹₽¢₩₪₴₦₲₵₡₢₤₥₧₨₭₮₯₰₱₳₻₼₾₿]'
    text = re.sub(currency_symbols, '', text)
    
    # Remove common text like "EUR", "USD", etc.
    text = re.sub(r'\b(EUR|USD|GBP|CHF|JPY|CNY)\b', '', text, flags=re.IGNORECASE)
    
    # Remove spaces, non-breaking spaces, and other whitespace
    text = re.sub(r'\s+', '', text)
    
    # Fix common OCR character misreadings
    ocr_fixes = {
        'O': '0',
        'o': '0',
        'l': '1',
        'I': '1',
        'S': '5',
        's': '5',
        'B': '8',
        'g': '9',
        'q': '9',
    }
    
    # Only apply OCR fixes to characters that are clearly in numeric context
    result = []
    for i, char in enumerate(text):
        if char in ocr_fixes:
            # Check if surrounded by digits or decimal separators
            prev_is_numeric = i > 0 and (text[i-1].isdigit() or text[i-1] in '.,')
            next_is_numeric = i < len(text) - 1 and (text[i+1].isdigit() or text[i+1] in '.,')
            if prev_is_numeric or next_is_numeric:
                result.append(ocr_fixes[char])
            else:
                result.append(char)
        else:
            result.append(char)
    text = ''.join(result)
    
    # Remove any remaining non-numeric characters except . and , and -
    text = re.sub(r'[^\d.,-]', '', text)
    
    # Handle negative sign
    is_negative = text.startswith('-')
    text = text.lstrip('-')
    
    if not text:
        return None
    
    # Count occurrences of . and ,
    comma_count = text.count(',')
    period_count = text.count('.')
    
    try:
        # Determine the decimal separator
        if comma_count == 0 and period_count == 0:
            # No separators, just a plain number
            value = float(text)
        elif comma_count == 0 and period_count == 1:
            # US format with decimal point (e.g., "18.90")
            value = float(text)
        elif comma_count == 1 and period_count == 0:
            # European format with comma as decimal (e.g., "18,90")
            value = float(text.replace(',', '.'))
        elif comma_count > 1 and period_count == 0:
            # Commas as thousands separators (e.g., "1,234,567")
            value = float(text.replace(',', ''))
        elif period_count > 1 and comma_count == 0:
            # Periods as thousands separators (e.g., "1.234.567")
            value = float(text.replace('.', ''))
        elif comma_count >= 1 and period_count >= 1:
            # Mixed format - determine which is the decimal separator
            last_comma = text.rfind(',')
            last_period = text.rfind('.')
            
            if last_comma > last_period:
                # European format: "1.234,56" - comma is decimal separator
                value = float(text.replace('.', '').replace(',', '.'))
            else:
                # US format: "1,234.56" - period is decimal separator
                value = float(text.replace(',', ''))
        else:
            value = float(text.replace(',', '.'))
        
        return -value if is_negative else value
        
    except ValueError:
        return None