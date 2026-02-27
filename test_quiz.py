"""
test_quiz.py

Unit tests for quiz.py using pytest.

"""
from pathlib import Path
from quiz import Quiz, Question


def test_score_all_correct():
    """If the user answers every question correctly, the score should equal the number of questions."""
    quiz = Quiz([ # creates a test quiz with 2 questions
        Question("Q1", ["a", "b"], 0), # correct answer is option 0
        Question("Q2", ["a", "b"], 1),# correct answer is option 1
    ])
    quiz.set_answer(0)
    quiz.next_question()
    quiz.set_answer(1)
    assert quiz.calculate_score() == 2   # score should be 2 out of 2

def test_save_result_creates_file(tmp_path: Path):
    """Saving results should create a CSV file and write content into it"""
    quiz = Quiz([Question("Q1", ["a", "b"], 0)])
    quiz.set_answer(0)
    out = tmp_path / "results.csv" # create a path to a CSV file with pytest's temp folder
    quiz.save_result("Test User", out)

    assert out.exists() # confirm the file now exists
    text = out.read_text() 
    assert "staff_name" in text # check for the header
    assert "Test User" in text  # check for the user's name