"""
gui.py

Tkinter GUI for the quiz.

Uses validation.py for name validation and quiz.py for quiz questions + answers
"""

import tkinter as tk
from tkinter import messagebox 
from pathlib import Path 

from validation import validate_staff_name
from quiz import Quiz, build_questions

RESULTS_PATH = Path("data") / "results.csv" # Where the results will be saved


class App(tk.Tk):
    """
    GUI window:
    1) Start screen: enter staff name
    2) Question screen: answer multiple choice questions
    3) Results screen: view score and click Done to save + exit
    """

    def __init__(self):
        super().__init__()

        self.title("HATS NEPTS Operations Quiz") 
        self.geometry("900x600")
        self.configure(bg="#2f6f95")

        self.staff_name = "" # sets staff name to empty at the start
        self.quiz = Quiz(build_questions())  # creates a Quiz object using questions quiz.py

        self.container = tk.Frame(self, bg=self["bg"])
        self.container.pack(fill="both", expand=True)

        self.show_start()

    def clear(self):
        """Remove all widgets from the container frame, so widgets don't overlap."""
        for w in self.container.winfo_children():
            w.destroy()

    def show_start(self):
        """Display the start screen (name entry + start button)."""
        self.clear()

        tk.Label( # title label
            self.container,
            text="HATS NEPTS Operations Quiz", 
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self["bg"],
        ).pack(pady=60)

        tk.Label( # instructions label
            self.container,
            text="Enter your name",
            font=("Arial", 14),
            fg="white",
            bg=self["bg"],
        ).pack(pady=10)

        self.name_entry = tk.Entry(self.container, font=("Arial", 16), width=28, justify="center") # name input box
        self.name_entry.pack(pady=10)
        self.name_entry.focus_set() # puts the cursor in the box automatically

        tk.Button( # start button
            self.container,
            text="Start Quiz",
            font=("Arial", 14, "bold"),
            width=14,
            command=self.start_quiz,
        ).pack(pady=30)

    def start_quiz(self):
        """Validate the name entered and if valid start the quiz."""
        name = self.name_entry.get() # read the name entered

        if not validate_staff_name(name):  # validate using the pure function from validation.py
            messagebox.showerror(
                "Invalid Name",
                "Please enter a valid name.\n\nAllowed: letters, spaces, apostrophes (') and dashes (-).\nNo double spaces.",
            )
            return

        self.staff_name = name  # store the cleaned name
        self.show_question() # go to first question

    def show_question(self): 
        """Show the current quiz question and answer options."""
        self.clear()

        q = self.quiz.get_current_question()

        tk.Label(  # question counter label
            self.container,
            text=f"Question {self.quiz.current_index + 1} of {len(self.quiz.questions)}",
            font=("Arial", 18, "bold"),
            fg="white",
            bg=self["bg"],
        ).pack(pady=30)

        tk.Label( # question text
            self.container,
            text=q.prompt,
            font=("Arial", 16),
            fg="white",
            bg=self["bg"],
            wraplength=700,
            justify="center",
        ).pack(pady=20)

        self.selected = tk.IntVar(value=-1) # stores which option is selected. -1 means nothing selected

        for i, option in enumerate(q.options): # make a radio button for each option
            tk.Radiobutton(
                self.container,
                text=option,
                variable=self.selected,
                value=i,
                font=("Arial", 14),
                fg="white",
                bg=self["bg"],
                selectcolor=self["bg"],
                anchor="w",
                padx=20,
            ).pack(fill="x", padx=180, pady=6)

        btn_text = "Finish" if not self.quiz.has_next() else "Next" # "Finish" instead of "Next" on the last question
        tk.Button(
            self.container,
            text=btn_text,
            font=("Arial", 14, "bold"),
            width=14,
            command=self.next_clicked,
        ).pack(pady=40)

    def next_clicked(self):
        """Save the selected answer, then go to the next question or show results if this was the last question"""

        choice = self.selected.get()

        if choice == -1: # If user didn't select anything, show error and do not go to next question
            messagebox.showerror("No Answer", "Please select an answer.")
            return
        
        self.quiz.set_answer(choice) # record the chosen answer for the current question

        if self.quiz.has_next():  # if there are more questions, go to next question.
            self.quiz.next_question()
            self.show_question()
        else: # if no more questions, show results screen
            self.show_results()

    def show_results(self):
        """Display the results screen. Score is only saved after "Done" button is pressed, which also closes the window"""
        self.clear()

        self.final_score = self.quiz.calculate_score() # calculate and store final score
        self.total_questions = len(self.quiz.questions)

        tk.Label(
            self.container,
            text="Results",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self["bg"],
        ).pack(pady=60)

        tk.Label(
            self.container,
            text=f"{self.staff_name}'s score:",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=self["bg"],
        ).pack(pady=10)

        tk.Label(
            self.container,
            text=f"{self.final_score} / {self.total_questions}",
            font=("Arial", 44, "bold"),
            fg="white",
            bg=self["bg"],
        ).pack(pady=10)

        tk.Button(
            self.container,
            text="Done",
            font=("Arial", 14, "bold"),
            width=14,
            command=self.done_clicked,
        ).pack(pady=40)

    def done_clicked(self):
        """Save quiz results to CSV and close the application. If saving fails, show an error popup."""
        try:
            self.quiz.save_result(self.staff_name, RESULTS_PATH)
        except OSError:
            messagebox.showerror("Save Error", "Could not save results to CSV.")

        self.destroy()


if __name__ == "__main__":
    App().mainloop()