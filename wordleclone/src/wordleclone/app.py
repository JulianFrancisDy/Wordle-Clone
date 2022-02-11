from turtle import clear, color
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

class wordleClone(toga.App):

    def startup(self):

        self.answer = "czari"

        self.attempts = 0

        main_box = toga.Box(
            style=Pack(direction=COLUMN)
        )

        # Guess input
        guess_label = toga.Label(
            'Guess: ',
            style=Pack(padding=(0, 5))
        )
        self.guess_input = toga.TextInput(style=Pack(flex=1))

        guess_box = toga.Box(style=Pack(direction=ROW, padding=5))
        guess_box.add(guess_label)
        guess_box.add(self.guess_input)

        # Guess button
        guess_button = toga.Button(
            'Guess',
            style = Pack(padding = 10),
            on_press=self.validate_guess,
        )

        # Legend
        legend = toga.Label(
            'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
            style = Pack(
                text_align = CENTER,
                padding = 10
            )
        )

        # Letter Boxes
        # initiate grid as box
        self.grid = toga.Box(style=Pack(direction=COLUMN, padding=(0,240), alignment=CENTER))
        
        self.rows = [] # container for all rows, for easier manipulation

        self.fill_grid()

        # Restart button
        restart_button = toga.Button(
            'Restart',
            style = Pack(padding = 10),
            on_press=self.reset
        )

        main_box.add(guess_box)
        main_box.add(guess_button)
        main_box.add(legend)
        main_box.add(self.grid)
        main_box.add(restart_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def reset(self, widget):
        print("RESETTING")
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
        error_message = ""

        if (len(guess_inp) != 5):
            error_message = "Guess must contain five characters"
        elif not(guess_inp.isalpha()):
            error_message = "Guess must contain only letters"
        
        if error_message != "":
            self.main_window.info_dialog(
                "Invalid Guess",
                error_message
                self.guess_inp.clear
            )
        else:
            self.game_logic()

    def game_logic (self):

        print(self.attempts)

        self.attempts += 1

        answer = self.answer
        guess = self.guess_input.value

        print("** FOR TESTING **\nAnswer is: {}\nGuess is: {}\n".format(self.answer, self.guess_input.value))

        new_row = toga.Box()

        self.clear_grid()

        for i in range(5):
            if guess[i] == answer[i]:
                letter = toga.Button("", style=Pack(width = 40, height = 40, padding = 3, background_color = "Green"))
                new_row.add(letter)
            elif guess[i] in answer:
                letter = toga.Button("", style=Pack(width = 40, height = 40, padding = 3, background_color = "Yellow"))
                new_row.add(letter)
            else:
                letter = toga.Button("", style=Pack(width = 40, height = 40, padding = 3, background_color = "Gray"))
                new_row.add(letter)

        self.rows.pop(self.attempts-1)
        self.rows.insert(self.attempts-1, new_row)

        self.update_grid()

def main():
    return wordleClone()
