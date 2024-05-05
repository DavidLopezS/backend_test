import re

def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_url(url: str) -> bool:
    pattern = r"^https://www\.linkedin\.com/in/[-\w]+/$"
    return re.match(pattern, url) is not None