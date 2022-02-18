N = 9
A = []
for i in range(9):
    R = []
    for j in range(9):
        R.append(0)
    A.append(R)
ROW = []
COLUMN = []
BLOCK = []


def is_safe(sudoku, row, column, num):
    for m in range(9):
        if sudoku[row][m] == num and m != column:
            return False

    for n in range(9):
        if sudoku[n][column] == num and n != row:
            return False

    SR = row - row % 3
    SC = column - column % 3
    for m in range(3):
        for n in range(3):
            if sudoku[SR + m][SC + n] == num and ((SR + m) != row and (SC + n) != column):
                return False

    return True


def solve(sudoku, row, column):
    if row == N - 1 and column == N:
        return True
    if column == N:
        row += 1
        column = 0

    if sudoku[row][column] > 0:
        return solve(sudoku, row, column + 1)

    for num in range(1, N + 1):
        if is_safe(sudoku, row, column, num):
            sudoku[row][column] = num

            if solve(sudoku, row, column + 1):
                return True

        sudoku[row][column] = 0

    return False


def solver(sudoku):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] > 0:
                if not is_safe(sudoku, row, col, sudoku[row][col]):
                    return False

    if solve(sudoku, 0, 0):
        return sudoku
    else:
        return False


def main():
    V = solver(A)
    return V


if __name__ == "__main__":
    print(main())
