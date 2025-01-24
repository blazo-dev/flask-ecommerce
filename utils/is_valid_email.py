import re


def is_valid_email(email: str):
    email_pattern = r"[\w.-]+@[\w-]+\.[a-z]{2,3}"
    match = re.search(email_pattern, email)

    return True if match else False
