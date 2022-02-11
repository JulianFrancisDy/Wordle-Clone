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

class boxes():
    guess_box = toga.Box(style=Pack(direction=ROW, padding=5))
    grid = toga.Box(style=Pack(direction=COLUMN, padding=(0,240), alignment=CENTER))

class wordleClone(toga.App):

    def startup(self):
        self.allowed_guesses = open("{}\\allowed_guesses.txt".format(self.paths.app)).readlines()

        self.new_word()

        self.attempts = 0

        main_box = toga.Box(
            style=Pack(direction=COLUMN)
        )

        # Guess input
        guess_label = labels().guess_label
        self.guess_input = toga.TextInput(style=Pack(flex=1))
        guess_box = boxes().guess_box

        guess_box.add(guess_label)
        guess_box.add(self.guess_input)

        # Guess button
        guess_button = toga.Button(
            'Guess',
            style = Pack(padding = 10),
            on_press=self.validate_guess,
        )

        # Legend
        legend = labels().legend

        # Letter Boxes
        self.grid = boxes().grid

        self.rows = [] # container for all rows, for easier manipulation

        self.fill_grid()

        # Restart button
        restart_button = toga.Button(
            'Restart',
            style = Pack(padding = 10),
            on_press=self.restart
        )

        main_box.add(guess_box)
        main_box.add(guess_button)
        main_box.add(legend)
        main_box.add(self.grid)
        main_box.add(restart_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def new_word(self):
        words = open("{}\\words.txt".format(self.paths.app)).readlines()
        word_ind = random.randrange(len(words))
        self.answer = words[word_ind][:5]

    def restart(self, widget):
        print("RESTARTING")
        self.new_word()
        self.clear_grid()
        self.fill_grid()
        self.attempts = 0

    def reset(self):
        print("RESETTING")
        self.new_word()
        self.clear_grid()
        self.fill_grid()
        self.attempts = 0

    def fill_grid(self):
        self.rows.clear()
        for i in range(6):
            row = toga.Box()
            for j in range(5):
                letter = toga.Button("", style=Pack(width = 40, height = 40, padding = 3, background_color = "White"))
                row.add(letter)
            self.rows.append(row)
            self.grid.add(row)
        for i in range(6):
            self.grid.add(self.rows[i])

    def clear_grid(self):
        for i in range(6):
            self.grid.remove(self.rows[i])

    def update_grid(self):
        for i in range(6):
            self.grid.add(self.rows[i])

    def validate_guess(self, widget):
        guess_inp = str(self.guess_input.value)

        print((guess_inp+"\n") in self.allowed_guesses)

        error_message = ""

        if len(guess_inp) != 5:
            error_message = "Guess must contain five letters"
        elif not(guess_inp.isalpha()):
            error_message = "Guess must contain only letters"
        elif ((guess_inp+"\n") not in self.allowed_guesses):
            error_message = "Guess is not a valid guess"

        if error_message != "":
            self.main_window.info_dialog(
                "Invalid Guess",
                error_message
            )
            self.guess_input.clear()
        else:
            self.game_logic()

    def game_logic (self):
        self.attempts += 1

        answer = self.answer
        guess = self.guess_input.value

        print("** FOR TESTING **\nAnswer is: {}\nGuess is: {}\n".format(self.answer, self.guess_input.value))

        new_row = toga.Box()

        self.clear_grid()

        # 0: GRAY 1: GREEN 2: YELLOW
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

        self.rows.pop(self.attempts-1)
        self.rows.insert(self.attempts-1, new_row)

        self.update_grid()

        if guess == answer:
            self.main_window.info_dialog(
                "CORRECT GUESS!",
                "You correctly guessed {}".format(self.answer)
            )           
            self.reset()

        if self.attempts == 6 and guess != answer:
            self.main_window.info_dialog(
                "GAME OVER",
                "The correct word is {}".format(self.answer)
            )           
            self.reset()

        self.guess_input.clear()

def main():
    return wordleClone()
