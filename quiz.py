"""Core domain logic for the transport operations training quiz."""

import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class Question:
    """A multiple-choice question and the index of its correct option."""

    prompt: str
    options: tuple[str, ...]
    correct_index: int

    def __post_init__(self) -> None:
        if len(self.options) < 2:
            raise ValueError("A question must have at least two options.")
        if not 0 <= self.correct_index < len(self.options):
            raise ValueError("The correct answer index is outside the option list.")


class Quiz:
    """Track progress, record answers, calculate scores and save results."""

    def __init__(self, questions: list[Question]):
        if not questions:
            raise ValueError("A quiz must contain at least one question.")
        self.questions = questions
        self.current_index = 0
        self.answers: list[int | None] = [None] * len(questions)

    def get_current_question(self) -> Question:
        return self.questions[self.current_index]

    def set_answer(self, selected_index: int) -> None:
        question = self.get_current_question()
        if not 0 <= selected_index < len(question.options):
            raise ValueError("The selected answer is outside the option list.")
        self.answers[self.current_index] = selected_index

    def has_next(self) -> bool:
        return self.current_index < len(self.questions) - 1

    def next_question(self) -> None:
        if not self.has_next():
            raise IndexError("The quiz is already on its final question.")
        self.current_index += 1

    def calculate_score(self) -> int:
        return sum(
            answer == question.correct_index
            for question, answer in zip(self.questions, self.answers)
            if answer is not None
        )

    def save_result(self, participant_name: str, csv_path: Path) -> None:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        file_exists = csv_path.exists()

        with csv_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    ["participant_name", "score", "total", "completed_utc"]
                )
            writer.writerow(
                [
                    participant_name,
                    self.calculate_score(),
                    len(self.questions),
                    datetime.now(UTC).isoformat(),
                ]
            )


def build_questions() -> list[Question]:
    """Return illustrative, organisation-neutral transport scenarios."""
    return [
        Question(
            "What should be completed before a vehicle begins service?",
            (
                "A documented safety check",
                "Only a mileage estimate",
                "A customer survey",
                "No checks are required",
            ),
            0,
        ),
        Question(
            "What is the best response when a schedule changes?",
            (
                "Keep the original record",
                "Update the approved system promptly",
                "Wait until the end of the month",
                "Record it in a personal notebook only",
            ),
            1,
        ),
        Question(
            "What should you do when asked to provide assistance beyond your training?",
            (
                "Attempt it without support",
                "Ignore the request",
                "Pause and escalate using the approved procedure",
                "Ask another passenger to help",
            ),
            2,
        ),
        Question(
            "Why should operational timestamps be recorded accurately?",
            (
                "For decoration in reports",
                "To support performance monitoring, audit and billing",
                "Only to track staff breaks",
                "They do not affect reporting",
            ),
            1,
        ),
        Question(
            "What is the best first step when two data sources disagree?",
            (
                "Choose the higher value",
                "Delete both records",
                "Verify the source evidence and follow the escalation process",
                "Leave the discrepancy unresolved",
            ),
            2,
        ),
        Question(
            "How should sensitive passenger information be handled?",
            (
                "Share it in public areas",
                "Use approved systems and share only with authorised people",
                "Save it to a personal device",
                "Include it in informal group chats",
            ),
            1,
        ),
        Question(
            "What should happen before safety equipment is used?",
            (
                "It should be checked and used according to training",
                "It should be used only on long journeys",
                "Checks should be skipped when busy",
                "Passengers should inspect it themselves",
            ),
            0,
        ),
        Question(
            "What is an appropriate response to a safeguarding concern?",
            (
                "Discuss it publicly",
                "Record factual information and use the approved reporting route",
                "Investigate it personally",
                "Wait to see whether it happens again",
            ),
            1,
        ),
        Question(
            "What information supports a clear cancellation record?",
            (
                "A reason and accurate timestamp",
                "Only the passenger's name",
                "An informal message",
                "No supporting information",
            ),
            0,
        ),
        Question(
            "How should an operational data-entry mistake be corrected?",
            (
                "Hide the original error",
                "Create an unrelated replacement record",
                "Use the approved correction process and preserve the audit trail",
                "Ignore it if a report has already run",
            ),
            2,
        ),
    ]
