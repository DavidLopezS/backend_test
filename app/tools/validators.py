import re

def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_url(url: str) -> bool:
    pattern = r"^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?$"
    return re.match(pattern, url) is not None