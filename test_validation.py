"""
test_validation.py

Unit tests for validation.py.
Tests both valid and invalid staff names.
"""

from validation import validate_staff_name


def test_validate_staff_name():
    """Names that meet all validation rules should return True. Names that break them should return False"""
    assert validate_staff_name("Abdulaziz") is True
    assert validate_staff_name("Mary Jane") is True
    assert validate_staff_name("O'Connor") is True
    assert validate_staff_name("Jean-Paul") is True

    assert validate_staff_name("") is False
    assert validate_staff_name("A") is False
    assert validate_staff_name("Mary  Jane") is False
    assert validate_staff_name("John123") is False
    assert validate_staff_name("Sarah!") is False