"""
quiz.py

Quiz questions + answers, calculates score and saves to CSV
"""

import csv
from datetime import datetime, UTC
from pathlib import Path


class Question:
    """Multiple choice question."""

    def __init__(self, prompt: str, options: list[str], correct_index: int):
        self.prompt = prompt # question text
        self.options = options # list of answers
        self.correct_index = correct_index # index of the correct answer from the option list


class Quiz:
    """Tracks quiz progress, records answers, calculates score, saves results."""

    def __init__(self, questions: list[Question]):  
        """Initialise the quiz with a list of Question objects"""
       
        self.questions = questions
        self.current_index = 0 # tracks which question the user is on
        self.answers = [None] * len(questions) # stores the selected answers

    def get_current_question(self) -> Question: 
        """ Returns current question using current_index"""
        return self.questions[self.current_index]

    def set_answer(self, selected_index: int) -> None:
        """Save the selected answer for the current question."""
        q = self.get_current_question()
        self.answers[self.current_index] = selected_index

    def has_next(self) -> bool:
        """Return True if there is another question after the current one."""
        return self.current_index < len(self.questions) - 1

    def next_question(self) -> None:
        """Go to next question"""
        self.current_index += 1

    def calculate_score(self) -> int:
        """Count how many correct answers there are"""
        score = 0
        for q, a in zip(self.questions, self.answers): # compare each stored answer with the correct index
            if a is not None and a == q.correct_index:
                score += 1
        return score

    def save_result(self, staff_name: str, csv_path: Path) -> None:
        """Append the quiz result to a CSV file. If the file does not exist, headers are created first."""
        csv_path.parent.mkdir(parents=True, exist_ok=True) # checks that the data folder exists

        file_exists = csv_path.exists()
        score = self.calculate_score()
        total = len(self.questions)
        timestamp = datetime.now(UTC).isoformat()

        with csv_path.open("a", newline="", encoding="utf-8") as f: # open file to append/write
            writer = csv.writer(f)
            if not file_exists: # write headers if new
                writer.writerow(["staff_name", "score", "total", "completed_utc"])
            writer.writerow([staff_name, score, total, timestamp]) # write quiz result


def build_questions() -> list[Question]: 
    """Makes quiz questions (10 questions)."""
    return [
        # Q1
        Question(
            "How many crew members are required for an ST2 journey?",
            ["1", "2", "3", "It depends on mileage"],
            1,
        ),
        # Q2
        Question(
            "When should a journey be marked as Cancelled?",
            [
                "When the patient refuses travel on arrival",
                "When the patient does not answer the door",
                "When the booking is stopped before the vehicle is dispatched",
                "When traffic delays the crew",
            ],
            2,
        ),
        # Q3
        Question(
            "What should staff do if a patient is not ready at pickup time?",
            [
                "Leave immediately",
                "Wait indefinitely",
                "Follow waiting-time policy and update control",
                "Cancel the job",
            ],
            2,
        ),
        # Q4
        Question(
            "When should pickup time be recorded?",
            [
                "When the job is booked",
                "When the vehicle arrives on site",
                "When the patient gets into the vehicle",
                "When the journey finishes",
            ],
            2,
        ),
        # Q5
        Question(
            "If a patient appears unwell or unsafe to travel, what is the correct action?",
            [
                "Continue journey anyway",
                "Leave the patient",
                "Report to control immediately",
                "Mark as completed",
            ],
            2,
        ),
        # Q6
        Question(
            "Why are seatbelts and wheelchair restraints important?",
            [
                "For comfort",
                "For legal paperwork only",
                "To prevent injury during transit",
                "Only for long journeys",
            ],
            2,
        ),
        # Q7
        Question(
            "What should you do if you notice signs of neglect or abuse?",
            [
                "Ignore it",
                "Tell the patient only",
                "Report via the safeguarding process",
                "Post in a group chat",
            ],
            2,
        ),
        # Q8
        Question(
            "Is it acceptable to discuss patient details in public areas?",
            ["Yes", "Only with colleagues", "No", "If speaking quietly"],
            2,
        ),
        # Q9
        Question(
            "Why must mileage and journey times be recorded accurately?",
            [
                "For driver bonuses",
                "For invoicing and audit",
                "Only for statistics",
                "It is optional",
            ],
            1,
        ),
        # Q10
        Question(
            "What should you do if you make a data entry mistake?",
            [
                "Ignore it",
                "Delete the record",
                "Correct it and notify control/admin",
                "Start a new job",
            ],
            2,
        ),
    ]