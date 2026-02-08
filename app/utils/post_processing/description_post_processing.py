import re
from typing import Optional

def post_process_description(description_value: str) -> Optional[str]:
    cleaned_value = description_value.strip()

    # Remove punctuation that comes after a space
    # Matches a space followed by one or more punctuation marks
    # \s matches a whitespace character
    cleaned_value = re.sub(r'\s[.,;:_\-\—*•]+', '', cleaned_value)

    # Remove extra spaces that may have been left behind
    cleaned_value = re.sub(r'\s+', ' ', cleaned_value).strip()

    return cleaned_value if cleaned_value else None