import pytest

from validation import validate_participant_name


@pytest.mark.parametrize(
    "name",
    ["Abdulaziz", "Mary Jane", "O'Connor", "Jean-Paul"],
)
def test_valid_names(name: str) -> None:
    assert validate_participant_name(name)


@pytest.mark.parametrize(
    "name",
    ["", "A", "Mary  Jane", "John123", "Sarah!"],
)
def test_invalid_names(name: str) -> None:
    assert not validate_participant_name(name)
