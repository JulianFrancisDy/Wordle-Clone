# Wordle Clone

A fork of the popular word game Wordle built on Beeware, a Python framework.




### Prerequisites:

- Python 3.7 onward
  
  Download link:
  
  ```
  https://www.python.org/downloads/
  ```

- Briefcase 
  
  Run in terminal:
  
  ```console
  python -m pip install briefcase
  ```

### Operation:

- Start the  application with:
  
  ``` console
  briefcase dev
  ```

### Game Rules:

- A random word is chosen from a pool of words. The player has 6 attempts to guess the said word.

- Each guess must be of 6 characters and is in the list of allowed guesses.

- For each guess, a box is colored as:
  
  - Green -the letter is in the correct position.
  
  - Yellow - the letter is part of the answer but in the wrong position.
  
  - Grey - the letter is not part of the answer.

- Game restarts after:
  
  - Victory
  
  - 6 incorrect attempts
  
  - Restart button is pressed
