import re
from typing import Optional, Union

def quantity_to_float(text: Union[str, None]) -> Optional[float]:
    """
    Parse a quantity string extracted by OCR to a float.
    
    Handles common OCR pitfalls:
    - Comma used as decimal separator (European format)
    - Spaces as thousand separators
    - 'O' or 'o' misread as '0'
    - 'l' or 'I' misread as '1'
    - 'S' or 's' misread as '5'
    - 'B' misread as '8'
    - 'Z' misread as '2'
    - Multiple decimal separators
    - Leading/trailing whitespace and special characters
    
    Args:
        text: The OCR-extracted string representing a quantity
        
    Returns:
        The parsed float value, or None if parsing fails
    """
    if text is None:
        return None
    
    if isinstance(text, (int, float)):
        return float(text)
    
    if not isinstance(text, str):
        return None
    
    # Strip whitespace and common unwanted characters
    cleaned = text.strip()
    
    if not cleaned:
        return None
    
    # Remove currency symbols and units that might be attached
    cleaned = re.sub(r'[$€£¥₹%]', '', cleaned)
    
    # Common OCR character substitutions
    ocr_fixes = {
        'O': '0',
        'o': '0',
        'l': '1',
        'I': '1',
        '|': '1',
        'S': '5',
        's': '5',
        'B': '8',
        'Z': '2',
        'z': '2',
        'g': '9',
        'q': '9',
    }
    
    # Only apply OCR fixes to characters that are surrounded by digits or at edges with digits
    result = []
    for i, char in enumerate(cleaned):
        if char in ocr_fixes:
            # Check if this character is likely meant to be a digit
            prev_is_digit = i > 0 and (cleaned[i-1].isdigit() or cleaned[i-1] in '.,')
            next_is_digit = i < len(cleaned) - 1 and (cleaned[i+1].isdigit() or cleaned[i+1] in '.,')
            
            if prev_is_digit or next_is_digit:
                result.append(ocr_fixes[char])
            else:
                result.append(char)
        else:
            result.append(char)
    
    cleaned = ''.join(result)
    
    # Remove spaces (thousand separators)
    cleaned = cleaned.replace(' ', '').replace('\u00a0', '')  # Regular and non-breaking space
    
    # Remove apostrophes used as thousand separators (Swiss format)
    cleaned = cleaned.replace("'", "")
    
    # Handle European format: determine if comma or dot is decimal separator
    dot_count = cleaned.count('.')
    comma_count = cleaned.count(',')
    
    if dot_count > 0 and comma_count > 0:
        # Both present: the last one is likely the decimal separator
        last_dot = cleaned.rfind('.')
        last_comma = cleaned.rfind(',')
        
        if last_comma > last_dot:
            # Comma is decimal separator (e.g., "1.234,56")
            cleaned = cleaned.replace('.', '').replace(',', '.')
        else:
            # Dot is decimal separator (e.g., "1,234.56")
            cleaned = cleaned.replace(',', '')
    elif comma_count == 1 and dot_count == 0:
        # Single comma, likely decimal separator (European format)
        # Check if it looks like a decimal (less than 3 digits after comma)
        parts = cleaned.split(',')
        if len(parts) == 2 and len(parts[1]) <= 3:
            cleaned = cleaned.replace(',', '.')
        else:
            # Likely a thousand separator
            cleaned = cleaned.replace(',', '')
    elif comma_count > 1:
        # Multiple commas = thousand separators
        cleaned = cleaned.replace(',', '')
    elif dot_count > 1:
        # Multiple dots = thousand separators, keep last as decimal
        parts = cleaned.rsplit('.', 1)
        cleaned = parts[0].replace('.', '') + '.' + parts[1]
    
    # Remove any remaining non-numeric characters except dot and minus
    cleaned = re.sub(r'[^\d.\-]', '', cleaned)
    
    # Handle multiple minus signs or misplaced minus
    if cleaned.count('-') > 1:
        cleaned = '-' + cleaned.replace('-', '')
    elif '-' in cleaned and not cleaned.startswith('-'):
        cleaned = '-' + cleaned.replace('-', '')
    
    # Handle multiple decimal points (keep first)
    if cleaned.count('.') > 1:
        parts = cleaned.split('.')
        cleaned = parts[0] + '.' + ''.join(parts[1:])
    
    try:
        return float(cleaned)
    except ValueError:
        return None