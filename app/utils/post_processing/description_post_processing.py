from typing import Optional

def post_process_description(description_value: str) -> Optional[str]:
    cleaned_value = description_value.strip()
    
    return cleaned_value if cleaned_value else None