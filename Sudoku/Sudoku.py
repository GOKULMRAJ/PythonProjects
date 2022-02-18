from tkinter import *
from Logic import solver

root = Tk()
root.title = 'Sudoku Solver'
root.geometry("360x400")

label = Label(root, text='Fill the numbers and click solve').grid(row=0, column=1, columnspan=10)
err_label = Label(root, text='', fg='red')
err_label.grid(row=15, column=1, columnspan=10, pady=5)
solved_label = Label(root, text='', fg='green')
solved_label.grid(row=15, column=1, columnspan=10, pady=5)

cells = {}


def Validate(x):
    out = (x.isdigit() or x == '') and (len(x) == 1)
    return out


reg = root.register(Validate)


def Form_3x3_Grid(row, column, bg_color):
    for i in range(3):
        for j in range(3):
            e = Entry(root, width=5, bg=bg_color, justify="center", validate="key", validatecommand=('reg', "%P"))
            e.grid(row=row + i + 1, column=column + j + 1, sticky="nsew", padx=1, pady=1, ipady=2)
            cells[(row + i + 1, column + j + 1)] = e


def Form_9x9_Grid():
    color = "#D0faff"
    for _row in range(1, 10, 3):
        for _col in range(0, 9, 3):
            Form_3x3_Grid(_row, _col, color)
            if color == "#D0faff":
                color = "#ffffd0"
            else:
                color = "#D0faff"


def clear_values():
    solved_label.config(text="")
    solved_label.config(text="")
    for _row in range(2, 11):
        for _col in range(1, 10):
            cell = cells[(_row, _col)]
            cell.delete(0, "end")


def get_values():
    board = []

    for _row in range(2, 11):
        rows = []
        for _col in range(1, 10):
            val = cells[(_row, _col)].get()
            if val == "":
                rows.append(0)
            else:
                rows.append(int(val))

        board.append(rows)
    Update(board)


btn = Button(root, command=get_values, text="Solve", width=10)
btn.grid(row=20, column=1, columnspan=5, pady=20)

btn = Button(root, command=clear_values, text="Clear", width=10)
btn.grid(row=20, column=5, columnspan=5, pady=20)


def Update(s):
    sol = solver(s)
    if sol:
        for row in range(2, 11):
            for col in range(1, 10):
                cells[(row, col)].delete(0, "end")
                cells[(row, col)].insert(0, sol[row - 2][col - 1])
        solved_label.config(text="SUDOKU SOLVED!")
    else:
        solved_label.config(text="NO SOLUTION EXISTS!!")


Form_9x9_Grid()
root.mainloop()
