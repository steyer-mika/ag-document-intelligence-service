from typing import Optional

from app.config.field_config import ARTICLE_NUMBER_LENGTH

def post_process_article_number(article_number_value: str) -> Optional[str]:
    # Step 1: Clean the string by removing unwanted characters
    cleaned_value = article_number_value.strip()

    # Step 2: Validate the length of the article number
    if len(cleaned_value) != ARTICLE_NUMBER_LENGTH:
        return None
    
    return cleaned_value if cleaned_value else None