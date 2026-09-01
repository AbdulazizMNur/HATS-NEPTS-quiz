import csv
from pathlib import Path

import pytest

from quiz import Question, Quiz, build_questions


def test_score_all_correct() -> None:
    quiz = Quiz(
        [Question("Q1", ("a", "b"), 0), Question("Q2", ("a", "b"), 1)]
    )
    quiz.set_answer(0)
    quiz.next_question()
    quiz.set_answer(1)
    assert quiz.calculate_score() == 2


def test_score_partial_completion() -> None:
    quiz = Quiz(
        [Question("Q1", ("a", "b"), 0), Question("Q2", ("a", "b"), 1)]
    )
    quiz.set_answer(0)
    assert quiz.calculate_score() == 1


def test_invalid_answer_is_rejected() -> None:
    quiz = Quiz([Question("Q1", ("a", "b"), 0)])
    with pytest.raises(ValueError):
        quiz.set_answer(2)


def test_save_result_creates_expected_csv(tmp_path: Path) -> None:
    quiz = Quiz([Question("Q1", ("a", "b"), 0)])
    quiz.set_answer(0)
    output = tmp_path / "results.csv"
    quiz.save_result("Test User", output)

    with output.open(newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    assert rows[0] == ["participant_name", "score", "total", "completed_utc"]
    assert rows[1][:3] == ["Test User", "1", "1"]


def test_question_bank_contains_ten_questions() -> None:
    assert len(build_questions()) == 10
