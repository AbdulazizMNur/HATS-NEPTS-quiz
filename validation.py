"""Participant-name validation used by the quiz interface."""

import re


def validate_participant_name(name: str) -> bool:
    """Return whether a name meets the application's input rules."""
    cleaned = name.strip()
    if len(cleaned) < 2 or "  " in cleaned:
        return False
    return re.fullmatch(r"[A-Za-z\s'-]+", cleaned) is not None
