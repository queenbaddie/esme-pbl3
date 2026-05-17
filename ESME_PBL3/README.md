# **📦 [X/O Arena (Tictactoe)]**

**MVP Status:** v1.0-Production

**Group Members:** Sarah AVENAS, Chloé ALLAIRE, Nour JABER, Clara BISIAUX


## **🎯 Project Overview**

Provide a concise (2-3 sentence) description of what your application does and the specific problem it solves. Why did you build this?

The application is a TicTacToe game where the player can choose to play against another player or against an AI with different levels of difficulty. The goal of the project was to build an interactive graphical application in Python while learning how to structure a program into multiple modules and implement an artificial intelligence using the Minimax algorithm. We chose to develop the project using VSCode because it allows easy collaboration between team members and helps us improve our development workflow.


## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**  
   git clone [your-repo-link]  
   cd [project-folder]

2. **Setup Virtual Environment:**  
   python -m venv .venv  
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies:**  
   pip install -r requirements.txt

4. **Run Application:**  
   python main.py


## **🛠️ Technical Architecture**

Explain how your code is organized. An "Architect-level" README should describe the separation of concerns.

- **main.py**: Entry point of the application. It initializes the Tkinter window, displays the menus, manages the game flow and connects the interface with the game logic.

- **ai/**: Contains the artificial intelligence of the game. It implements the Minimax algorithm used to calculate the best possible move for the AI depending on the selected difficulty level.

- **board/**: Contains the Board class responsible for managing the game grid, checking available moves, detecting a winner, and resetting the board.

- **player/**: Contains the Player class which represents a player and stores the player's symbol (X or O).


## **🧪 Testing & Validation**

How can a user verify the code works?

- Run the application using `python main.py`.
- Choose a game mode (Player vs Player or Player vs AI or AI vs AI).
- Play by clicking on the grid.

Happy Path demonstration:

- The game starts with player **X**.
- Players alternate turns after each move.
- The game detects a win when three symbols are aligned.
- If the board is full with no winner, the game declares a draw.
- The user can return to the main menu after the game ends.


## **📦 Dependencies**

List the main third-party libraries used and why they were chosen:

- **tkinter**: Used to create the graphical user interface and manage user interactions such as buttons, menus, and the game grid.


## **🔮 Future Roadmap (v2.0)**

What features would you add if you had more time or a larger budget?

- Add a score tracking system between games
- Improve the graphical interface and design
- Add animations and sound effects
- Implement an online multiplayer mode
- Allow different board sizes (4x4, 5x5)
- Add player statistics and game history
