from turtle import clear, color
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import random

class labels():
    guess_label = toga.Label(
        'Guess: ',
        style=Pack(padding=(0, 5))
    )
    legend = toga.Label(
        'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
        style = Pack(
            text_align = CENTER,
            padding = 10
        )
    )

class game_button():
    def __init__(self, label) -> None:
        self.label = label
        self.button = toga.Button(
            self.label,
            style = Pack(padding = 10),
        )

class board():
    def __init__(self) -> None:
        self.grid = toga.Box(style=Pack(direction=COLUMN, padding=(0,240), alignment=CENTER))
        self.rows = []

    def fill_grid(self):
        self.rows.clear()
        for i in range(6): # 6 rows
            row = toga.Box() # container for buttons
            for j in range(5): # 5 columns
                letter = toga.Button("", style=Pack(width = 40, height = 40, padding = 3, background_color = "White"))
                row.add(letter)
            self.rows.append(row)
            self.grid.add(row)
        for i in range(6):
            self.grid.add(self.rows[i])

    def clear_grid(self): # remove nodes of grid from rows array
        for i in range(6):
            self.grid.remove(self.rows[i])

    def update_grid(self): # repopulate boxes from rows array
        for i in range(6):
            self.grid.add(self.rows[i])

    def reset(self): # method for resetting game after game is over
        print("RESETTING BOARD")
        self.clear_grid()
        self.fill_grid()

class wordleClone(toga.App):
    def startup(self):
        self.allowed_guesses = open("{}\\allowed_guesses.txt".format(self.paths.app)).readlines() # create list of allowed guesses from allowed_guesses.txt
        self.new_word() # select word from words.txt using new_word method
        self.attempts = 0 # initiate number of attempts to 0
        # toga main box
        main_box = toga.Box(
            style=Pack(direction=COLUMN)
        )

        # Guess input
        guess_label = labels().guess_label 
        self.guess_input = toga.TextInput(style=Pack(flex=1))
        guess_box = toga.Box(style=Pack(direction=ROW, padding=5))
        guess_box.add(guess_label)
        guess_box.add(self.guess_input)

        # Guess button
        guess_button = game_button('Guess').button
        guess_button.on_press=self.validate_guess

        # Legend
        legend = labels().legend

        # Letter Boxes
        self.board = board()
        self.board.fill_grid()

        #Restart button
        restart_button = game_button('Restart').button
        restart_button.on_press=self.restart

        main_box.add(guess_box)
        main_box.add(guess_button)
        main_box.add(legend)
        main_box.add(self.board.grid)
        main_box.add(restart_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def new_word(self): # select a word from words.txt
        words = open("{}\\words.txt".format(self.paths.app)).readlines()
        word_ind = random.randrange(len(words))
        self.answer = words[word_ind][:5]

    def restart(self, widget): # method for restart button
        print("RESTARTING") 
        self.new_word() # selects a new word
        self.guess_input.clear()
        self.board.reset()
        self.attempts = 0 # reset attempts to 0

    def reset(self):
        self.new_word()
        self.guess_input.clear()
        self.board.reset()
        self.attempts = 0

    def validate_guess(self, widget):
        guess_inp = str(self.guess_input.value)

        # error handling
        error_message = ""
        if len(guess_inp) != 5:
            error_message = "Guess must contain five letters"
        elif not(guess_inp.isalpha()):
            error_message = "Guess must contain only letters"
        elif ((guess_inp+"\n") not in self.allowed_guesses):
            error_message = "Guess is not a valid guess"

        if error_message != "": # there is an error, release prompt
            self.main_window.info_dialog(
                "Invalid Guess",
                error_message
            )
            self.guess_input.clear()
        else: # no error, proceed to game logic
            self.game_logic()

    def game_logic (self):

        self.attempts += 1 # increment attempts
        
        # for brevity
        answer = self.answer
        guess = self.guess_input.value

        # for testing purposes, prints ANSWER and  GUESS
        print("** FOR TESTING **\nAnswer is: {}\nGuess is: {}\n".format(self.answer, self.guess_input.value))

        # update grid, color current row
        new_row = toga.Box()
        
        self.board.clear_grid()

        # color current row
        for i in range(5):
            if guess[i] == answer[i]:
                letter = toga.Button("{}".format(guess[i]), style=Pack(width = 40, height = 40, padding = 3, background_color = "Green"))
                new_row.add(letter)
            elif guess[i] in answer:
                letter = toga.Button("{}".format(guess[i]), style=Pack(width = 40, height = 40, padding = 3, background_color = "Yellow"))
                new_row.add(letter)
            else:
                letter = toga.Button("{}".format(guess[i]), style=Pack(width = 40, height = 40, padding = 3, background_color = "Gray"))
                new_row.add(letter)

        # replace row of current attempt with colorized row
        self.board.rows.pop(self.attempts-1)
        self.board.rows.insert(self.attempts-1, new_row)

        # reflect changes
        self.board.update_grid()

        # game over scenarios
        if guess == answer: # correct guess
            self.main_window.info_dialog(
                "CORRECT GUESS!",
                "You correctly guessed {}".format(self.answer)
            )           
            self.reset()
        elif self.attempts == 6 and guess != answer:
            self.main_window.info_dialog(
                "GAME OVER",
                "The correct word is {}".format(self.answer)
            )         
            self.reset()

        self.guess_input.clear()

def main():
    return wordleClone()
