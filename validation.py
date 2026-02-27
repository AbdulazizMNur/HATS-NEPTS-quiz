"""
validation.py

Name validation for the quiz.
Only allows letters, spaces, apostrophes, and dashes.
No double spaces allowed.
"""

import re


def validate_staff_name(name: str) -> bool:
    """
    Validate a staff member's name
    Returns True if valid, False if it is not
    """

    cleaned = name.strip()  # remove spaces at the start and end

    if len(cleaned) < 2:
        return False

    if "  " in cleaned:
        return False

    return re.fullmatch(r"[A-Za-z\s'-]+", cleaned) is not None # makes sure only allowed characters are used