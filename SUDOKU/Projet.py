from collections import defaultdict
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


class Sudoku:
    def __init__(board):
        board.grille = board.create_board()

    def create_board(board):
        newboard = [['.' for _ in range(9)] for _ in range(9)]
        board.Remplir(newboard)
        board.supprimer_valeurs(newboard)
        return newboard

    def Remplir(board, grille):
        nombres = list(range(1, 10))
        random.shuffle(nombres)

        for l in range(9):
            for c in range(9):
                if grille[l][c] == '.':
                    random.shuffle(nombres)

                    for num in nombres:
                        if board.is_valid(grille, l, c, str(num)):
                            grille[l][c] = str(num)

                            if board.Remplir(grille):
                                return True

                            grille[l][c] = '.'

                    return False

        return True

    def supprimer_valeurs(board, grille):
        nbrcellsupp = random.randint(50, 60)

        while nbrcellsupp > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if grille[row][col] != '.':
                t = grille[row][col]
                grille[row][col] = '.'

                if not board.solution_unique(grille):
                    grille[row][col] = t
                else:
                    nbrcellsupp -= 1

    @staticmethod
    def is_valid(grille, row, col, num):#s'assure qu'un nombre peut etre placee dans position
        for i in range(9):
            if grille[row][i] == num or grille[i][col] == num:
                return False

        rows = (row // 3) * 3
        cols = (col // 3) * 3
        for i in range(rows, rows + 3):
            for j in range(cols, cols + 3):
                if grille[i][j] == num:
                    return False

        return True

    @staticmethod
    def solution_unique(grille):
        count = [0]
        Sudoku.sudoku_resolu(grille, count)
        return count[0] == 1

    @staticmethod
    def sudoku_resolu(grille, count):# une approche de résolution récursive pour remplir les cellules vides de la grille avec des nombres valides
        for row in range(9):
            for col in range(9):
                if grille[row][col] == '.':
                    for num in range(1, 10):
                        if Sudoku.is_valid(grille, row, col, str(num)):
                            grille[row][col] = str(num)

                            if Sudoku.est_Resolu(grille):
                                count[0] += 1#en vérifiant à chaque étape si une solution unique a été trouvée.
                                if count[0] > 1:
                                    return

                            Sudoku.sudoku_resolu(grille, count)
                            grille[row][col] = '.'

                    return

    @staticmethod
    def est_Resolu(grille):
        for row in range(9):
            for col in range(9):
                if grille[row][col] == '.':
                    return False

        return True

    def introduction(board):
        print('------SUDOKU------')
        print()

    def print_grille(board):
        grid_str = ''
        for i in range(len(board.grille)):
            if i % 3 == 0 and i != 0:
                grid_str += "- - - - - - - - - - - - -\n"

            for j in range(len(board.grille[i])):
                if j % 3 == 0 and j != 0:
                    grid_str += "| "

                if j == 8:
                    grid_str += board.grille[i][j] + "\n"
                else:
                    grid_str += str(board.grille[i][j]) + " "

        return grid_str

    def check_game(board):#si la sudoku est completement valide 
        check = defaultdict(int)
        for i in range(len(board.grille)):
            for j in range(len(board.grille[i])):
                val = board.grille[i][j]
                if val != '.':
                    check[str(val) + ' dans la ligne ' + str(i)] += 1
                    check[str(val) + ' dans la colonne ' + str(j)] += 1
                    check[str(val) + ' dans la box ' + str(i // 3) + ' ' + str(j // 3)] += 1
                    if check[str(val) + ' dans la ligne ' + str(i)] > 1 or \
                            check[str(val) + ' dans la colonne ' + str(j)] > 1 or \
                            check[str(val) + ' dans la box ' + str(i // 3) + ' ' + str(j // 3)] > 1:
                        return False
        return True


class SudokuGUI(QMainWindow):
    def __init__(board):
        super().__init__()#appel du constructeur pour initialiser la fenetre
        board.setWindowTitle("Sudoku")
        board.setGeometry(100, 100, 400, 400)

        board.sudoku = Sudoku()
        board.create_widgets()

    def create_widgets(board):
        board.intro_label = QLabel(board)#classe qui affiche un texte ou une image
        board.intro_label.setText("------SUDOKU------")
        board.intro_label.setFont(QFont("Arial", 16))
        board.intro_label.setAlignment(Qt.AlignCenter)
        board.intro_label.setGeometry(10, 10, 380, 40)

        board.grid_label = QLabel(board)
        board.grid_label.setText(board.sudoku.print_grille())
        board.grid_label.setFont(QFont("Courier New", 12))
        board.grid_label.setAlignment(Qt.AlignCenter)
        board.grid_label.setGeometry(10, 60, 380, 260)

        board.quit_button = QPushButton(board)
        board.quit_button.setText("Quitter")
        board.quit_button.setGeometry(200, 330, 80, 30)
        board.quit_button.clicked.connect(board.close)

        board.input_label = QLabel(board)
        board.input_label.setText("Veuillez entrer un nombre :")
        board.input_label.setFont(QFont("Arial", 12))
        board.input_label.setGeometry(10, 300, 380, 20)

        board.number_input = QLineEdit(board)
        board.number_input.setGeometry(140, 330, 50, 30)

        board.row_input = QLineEdit(board)
        board.row_input.setPlaceholderText("Ligne (1-9)")
        board.row_input.setGeometry(20, 360, 80, 30)

        board.col_input = QLineEdit(board)#rectangle
        board.col_input.setPlaceholderText("Colonne (1-9)")
        board.col_input.setGeometry(120, 360, 100, 30)

        board.submit_button = QPushButton(board)
        board.submit_button.setText("Valider")
        board.submit_button.setGeometry(240, 360, 80, 30)
        board.submit_button.clicked.connect(board.submit_answer)

    def submit_answer(board):
        ans = board.number_input.text()
        row = int(board.row_input.text()) - 1
        col = int(board.col_input.text()) - 1

        if board.sudoku.grille[row][col] != '.':
            board.number_input.setText("")
        else:
            board.sudoku.grille[row][col] = ans
            if not board.sudoku.check_game():
                board.sudoku.grille[row][col] = '.'
            else:
                if board.sudoku.est_Resolu(board.sudoku.grille):
                    board.show_message_box("Félicitations !", "Vous avez terminé le Sudoku !")
                else:
                    board.grid_label.setText(board.sudoku.print_grille())
                    board.number_input.setText("")
                    board.row_input.setText("")
                    board.col_input.setText("")

                    if board.sudoku.check_game() and board.sudoku.est_Resolu(board.sudoku.grille):
                        board.show_message_box("Félicitations !", "Vous avez terminé le Sudoku !")



    def show_message_box(board, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


def main():
    app = QApplication([])
    sudoku_gui = SudokuGUI()# une implémentation personnalisée d'une interface graphique de jeu Sudoku
    sudoku_gui.show()#méthode rend la fenêtre visible à l'utilisateur
    app.exec_()


if __name__ == "__main__":
    main()
