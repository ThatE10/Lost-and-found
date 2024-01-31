import re

def validate_phone(phone):
    pattern = r'^\d{10}$'
    if not re.match(pattern, phone):
        return False
    return True

def validate_email(email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(pattern, email):
        return False
    return True