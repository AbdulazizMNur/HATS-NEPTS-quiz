# **HATS NEPTS Operations Quiz**


## **Introduction**

HATS Group provides Non-Emergency Patient Transport Services (NEPTS). Staff working in this service must follow clear procedures related to safety, safeguarding, data protection, and daily operational tasks. Because the service operates in a healthcare environment, it is important that staff understand these procedures and apply them correctly. This helps protect patients, maintain service quality, and ensure compliance with company and regulatory standards.

This MVP is a desktop quiz application built using Python and Tkinter. Its purpose is to provide a simple way to check staff understanding of important NEPTS topics. The quiz includes questions about crew requirements, safeguarding actions, cancellation processes, recording pickup times, and correct documentation. The goal is to create a consistent and structured way to assess knowledge.

The application includes a graphical user interface (GUI) where staff enter their name and complete a multiple-choice quiz. The system checks that the name entered is valid, records selected answers, and calculates the final score automatically. Results are saved to a CSV file so there is a record of completion. Automated unit tests were written using pytest to confirm that key parts of the logic work correctly. Continuous Integration was set up using GitHub Actions so tests run automatically whenever changes are made to the code.

Overall, this project shows how a simple digital tool can support internal training and provide a clearer way to assess staff knowledge within the the company.

The application includes:

- A graphical user interface (GUI),   
- Multiple-choice questions,  
- Name validation,    
- Automatic score calculation,    
- Saving results to a CSV file,   
- Unit testing using pytest,  
- Continuous Integration using GitHub Actions


## **Design**

**1) GUI Design (Figma Prototype)**

Before coding, the screens were designed in Figma to plan the layout and user journey.

***Start Screen***

![Start Screen](<Screen 1 - Start.png>)

This screen includes:

- Application title,  
- Name input field,   
- Start button,   
- Clear layout and colour theme (company colours)

***Question Screen***

![Quiz Screen](<Screen 2 - Quiz.png>)

This screen includes:

- Question number display,    
- Question text,  
- Four answer options (radio buttons),    
- Next button (Finish was put into the last question screen), 
- Validation to prevent skipping questions

***Results Screen***

![Results Screen](<Screen 3 - Results.png>)

This screen includes:

- Results heading,    
- Staff member’s name,    
- Large score display,    
- Done button (saves results and exits)

**2) Functional Requirements**

The application must:

- Accept a name,    
- Validate the name that was entered,    
- Display 10 multiple-choice questions,   
- Store selected answers, 
- Prevent moving forward without selecting an answer,     
- Calculate the final score,  
- Save results to a CSV file, 
- Display the final score,    
- Close safely after saving,  

**3) Non-Functional Requirements**

The application should:

- Be simple and easy to use,  
- Run locally without internet,   
- Respond quickly,    
- Have clear, readable code,  
- Be testable,    
- Use a consistent visual design, 

**4) Technology Stack**

This project was built using Python 3.11. The GUI was created with Tkinter, which allowed the application to run as a simple desktop program. The quiz logic was written using object-oriented programming, separating the GUI from the core quiz code. Testing was done using pytest to check that key features, such as score calculation and name validation, work correctly. Continuous Integration was set up using GitHub Actions so tests run automatically whenever changes are pushed to the repository. Quiz results are saved in a CSV file, which is an easy method of storing data without needing a database. 

**5) Code Design**

***Application Flow***

![Flow diagram](<flow_diagram (1).png>)

The user journey follows this order:

Start application

1. Enter name

2. Load First Question

3. Select Answer

4. Load Next Question

5. Calculate score

6. Display results

7. Save results

8. Exit

This simple flow keeps the application easy to understand.

***Class Structure***

![Arcitercure Diagram](<Architecture Diagram (1).png>)

The application follows a simple structure. The App (GUI) class, later names just App during development, handles all user interaction, including the screens, any input, and navigating between questions. It calls the validate_staff_name() function in validation.py to check name that was inputted before starting the quiz.

The Quiz class contains the logic for the quiz. It stores the list of questions, records selected answers, calculates the final score, and saves results to a CSV file. The Quiz class uses the Question class as a data structure to represent each multiple-choice question.

Quiz results are saved in a CSV file called results.csv. The save_result() method in the Quiz class writes the staff name, score, total number of questions, and completion time to this file.

The separate user interface, quiz logic and data storage. This makes the code easier to understand and manage.

## **Development**

The project is divided into three main files:

- validation.py

- quiz.py

- gui.py

And 2 additional files are used for testing:

- test_validation.py

- test_quiz.py  

***1) Name Validation***

The validation function checks that:

The name is at least two characters, there are no double spaces and only letters, spaces, apostrophes, or dashes are used. It also trims the name of any extra spaces either side.

```
def validate_staff_name(name: str) -> bool:
    cleaned = name.strip()

    if len(cleaned) < 2:
        return False

    if "  " in cleaned:
        return False

    return re.fullmatch(r"[A-Za-z\s'-]+", cleaned) is not None
```
This function is a pure function, meaning it always returns the same result for the same input. This makes it easy to test.

***2) Question Class***
```
class Question:
    def __init__(self, prompt: str, options: list[str], correct_index: int):
        self.prompt = prompt
        self.options = options
        self.correct_index = correct_index
```
Each question object stores its own data, including the question text (prompt), the list of possible answers (options), and the index of the correct answer (correct_index).

Instead of storing questions as plain text or separate variables, grouping the data inside a class keeps it organised and easier to manage. The Quiz class then uses a list of Question objects to run the quiz.


***3) Quiz Class***

It keeps track of the list of questions, the current question index, and the answers selected by the user. It also handles score calculation and saving results to a file.

This method works by counting how many answers are correct. It goes through each question and the user’s selected answer at the same time using zip(). If the selected answer matches the correct answer for that question, the score increases by one. After checking all questions, the total score is returned:

```
def calculate_score(self) -> int:
    score = 0
    for q, a in zip(self.questions, self.answers):
        if a is not None and a == q.correct_index:
            score += 1
    return score
```

The save_result() method stroes the results in a csv by ensuring that the directory exists using mkdir(), then it checks whether the CSV file already exists. The score is calculated using the calculate_score() method and stored along with the user's name and a timestamp. The file is opened in append mode ("a"), meaning new results are added to the end of the file without deleting existing data:

```
def save_result(self, staff_name: str, csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = csv_path.exists()

    score = self.calculate_score()
    total = len(self.questions)
    timestamp = datetime.now(UTC).isoformat()

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["staff_name", "score", "total", "completed_utc"])
        writer.writerow([staff_name, score, total, timestamp])
```
This ensures results are stored safely and headers are added if needed.

***4) GUI***

The GUI controls screen transitions and user interaction including error messages if the user tries to move on without selecting an answer:

```
if choice == -1:
    messagebox.showerror("No Answer", "Please select an answer.")
    return
```
This prevents users from skipping questions.

***5) How the components work together***

When the application starts, the App class creates an instance of the Quiz class using a list of Question objects. The GUI controls what the user sees on screen and handles button clicks and screen changes. Before the quiz begins, the GUI calls the validate_staff_name() function to check that the name entered is valid.

As the user answers each question, the selected answer is passed to the Quiz class and stored in its answers list. The GUI then moves to the next question. When all questions have been completed, the calculate_score() method is called to determine the final score. After the results are displayed, the save_result() method writes the staff name, score, and timestamp to the CSV file.

```
self.quiz = Quiz(build_questions())
```

## **Testing**
***1) Testing Approach***

Two types of testing were used:

- Manual testing of the interface
- Automated testing using pytest

This ensures both the user experience and logic work correctly.

***2) Unit Testing***

Pytest was used to test the main parts of the application, including score calculation, name validation, and saving results. 

Here is an example of automated unit testing:

```
def test_score_all_correct():
    """If the user answers every question correctly, the score should equal the number of questions."""
    quiz = Quiz([ 
        Question("Q1", ["a", "b"], 0), 
        Question("Q2", ["a", "b"], 1),
    ])
```

When the tests were run, pytest showed 3 tests passed, confirming that the core functions work correctly:

![Pytest screenshot](<Screenshot 2026-02-27 065824.png>)

***3) Manual Testing***

Manual testing was carried out to check that the application works correctly from the user's end. Different features were tested through the GUI, including name validation, question progression, score calculation, result saving, and application exit. Different valid and invalid inputs were used to confirm that error messages appeared when expected and that the system behaved correctly in all scenarios:

![Manual Testing Table](<Screenshot 2026-02-27 070911.png>)

Continuous Integration through GitHub Actions makes sure that tests are automatically run whenever changes are made.

## **Documentation**

***1) User Guide***

To run the application:

- python gui.py

Steps:

1. Enter name
2. Click Start Quiz
3. Answer questions
4. View results
5. Click Done

If an invalid name is entered, an error message will appear. If no answer is selected, the user cannot move to the next question.

Results are saved in:

data/results.csv

***2) Technical Guide***

To run tests:

1. pip install pytest
2. pytest

Project structure:

- gui.py
- quiz.py
- validation.py
- test_quiz.py
- test_validation.py

Continuous Integration runs automatically through GitHub Actions.

## **Evaluation**


Overall, the project went well and I was able to build a working quiz application that meets the main requirements. One part I found challenging was making sure that each answer matched the correct question when calculating the score. Since the questions and answers were stored separately, I had to make sure they were compared in the right order. Using the zip() function helped solve this, but I had to test it carefully to make sure the score was accurate. This improved my understanding of how lists and indexing work in Python. If I continued developing the project, I would improve it by adding features such as randomising the questions or using a database instead of a CSV file. Overall, the project helped me better understand how different parts of an application connect and work together.
