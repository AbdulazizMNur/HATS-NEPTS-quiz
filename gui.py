"""Tkinter interface for the transport operations training quiz."""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from quiz import Quiz, build_questions
from validation import validate_participant_name

RESULTS_PATH = Path("data") / "results.csv"
BACKGROUND = "#18324a"
ACCENT = "#28a6a8"


class App(tk.Tk):
    """Display the start, question and results screens."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Transport Operations Training Quiz")
        self.geometry("900x600")
        self.configure(bg=BACKGROUND)

        self.participant_name = ""
        self.quiz = Quiz(build_questions())
        self.container = tk.Frame(self, bg=BACKGROUND)
        self.container.pack(fill="both", expand=True)
        self.show_start()

    def clear(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()

    def heading(self, text: str, size: int = 24) -> None:
        tk.Label(
            self.container,
            text=text,
            font=("Arial", size, "bold"),
            fg="white",
            bg=BACKGROUND,
        ).pack(pady=30)

    def show_start(self) -> None:
        self.clear()
        self.heading("Transport Operations Training Quiz")
        tk.Label(
            self.container,
            text="Illustrative portfolio demo — not operational guidance",
            font=("Arial", 11),
            fg="#c8d6e5",
            bg=BACKGROUND,
        ).pack(pady=5)
        tk.Label(
            self.container,
            text="Enter participant name",
            font=("Arial", 14),
            fg="white",
            bg=BACKGROUND,
        ).pack(pady=25)

        self.name_entry = tk.Entry(
            self.container, font=("Arial", 16), width=28, justify="center"
        )
        self.name_entry.pack(pady=10)
        self.name_entry.focus_set()
        tk.Button(
            self.container,
            text="Start Quiz",
            font=("Arial", 14, "bold"),
            bg=ACCENT,
            fg="white",
            width=14,
            command=self.start_quiz,
        ).pack(pady=30)

    def start_quiz(self) -> None:
        name = self.name_entry.get().strip()
        if not validate_participant_name(name):
            messagebox.showerror(
                "Invalid Name",
                "Use letters, spaces, apostrophes or dashes, with no double spaces.",
            )
            return
        self.participant_name = name
        self.show_question()

    def show_question(self) -> None:
        self.clear()
        question = self.quiz.get_current_question()
        self.heading(
            f"Question {self.quiz.current_index + 1} of {len(self.quiz.questions)}",
            18,
        )
        tk.Label(
            self.container,
            text=question.prompt,
            font=("Arial", 16),
            fg="white",
            bg=BACKGROUND,
            wraplength=700,
            justify="center",
        ).pack(pady=20)

        self.selected = tk.IntVar(value=-1)
        for index, option in enumerate(question.options):
            tk.Radiobutton(
                self.container,
                text=option,
                variable=self.selected,
                value=index,
                font=("Arial", 14),
                fg="white",
                bg=BACKGROUND,
                selectcolor=BACKGROUND,
                anchor="w",
                padx=20,
            ).pack(fill="x", padx=150, pady=6)

        tk.Button(
            self.container,
            text="Next" if self.quiz.has_next() else "Finish",
            font=("Arial", 14, "bold"),
            bg=ACCENT,
            fg="white",
            width=14,
            command=self.next_clicked,
        ).pack(pady=35)

    def next_clicked(self) -> None:
        choice = self.selected.get()
        if choice == -1:
            messagebox.showerror("No Answer", "Please select an answer.")
            return
        self.quiz.set_answer(choice)
        if self.quiz.has_next():
            self.quiz.next_question()
            self.show_question()
        else:
            self.show_results()

    def show_results(self) -> None:
        self.clear()
        self.heading("Results")
        tk.Label(
            self.container,
            text=f"{self.participant_name}'s score",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=BACKGROUND,
        ).pack(pady=10)
        tk.Label(
            self.container,
            text=f"{self.quiz.calculate_score()} / {len(self.quiz.questions)}",
            font=("Arial", 44, "bold"),
            fg="white",
            bg=BACKGROUND,
        ).pack(pady=10)
        tk.Button(
            self.container,
            text="Save and Exit",
            font=("Arial", 14, "bold"),
            bg=ACCENT,
            fg="white",
            width=14,
            command=self.done_clicked,
        ).pack(pady=40)

    def done_clicked(self) -> None:
        try:
            self.quiz.save_result(self.participant_name, RESULTS_PATH)
        except OSError:
            messagebox.showerror("Save Error", "The result could not be saved.")
            return
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
