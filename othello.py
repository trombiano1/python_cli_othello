# Define constants.
OPEN = 0
FIRST = 1
SECOND = 2

DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1),
              (-1, 0), (-1, -1), (0, -1), (1, -1)]

INITIAL_BOARD = [[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, FIRST, SECOND, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, SECOND, FIRST, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN]]


def stone(turn):
    '''
    Util function to return the corresponding character for the stone.
    '''
    if turn == FIRST:
        return "○"
    elif turn == SECOND:
        return "●"
    elif turn == OPEN:
        return " "


def show_board(board, cells_to_place=[]):
    '''
    Util function to return the board representation as string.
    `cells_to_place` is a list of cells that the user can place the stone on,
    which is representated with '+'.
    '''
    s = ' : 0 1 2 3 4 5 6 7\n-------------------\n'
    for i in range(0, 8):
        s = s + str(i) + ': '
        for j in range(0, 8):
            if (i, j) in cells_to_place:
                s += '+'
            else:
                s += stone(board[i][j])
            s = s + ' '
        s = s + '\n'
    return s


def opponent(turn):
    '''
    Util function that returns the opponent of a turn.
    '''
    if turn == FIRST:
        return SECOND
    elif turn == SECOND:
        return FIRST
    else:
        raise ValueError("Unexpected turn")


def is_inside(i, j):
    '''
    Util function that returns whether (i, j) is
    a valid cell inside the board.
    '''
    if i < 0 or i >= 8:
        return False
    if j < 0 or j >= 8:
        return False
    return True


def get_cells_to_flip(board, turn, placed_i, placed_j):
    '''
    Returns a list of cells that should be flipped when a
    stone of `turn` is placed on (placed_i, placed_j).
    '''
    cells_to_flip = []

    # Test each of the 8 directions from the placed cell.
    for direction in DIRECTIONS:
        i = placed_i + direction[0]
        j = placed_j + direction[1]

        possible_flips = []
        while is_inside(i, j):
            if board[i][j] == opponent(turn):
                possible_flips.append((i, j))
            elif board[i][j] == turn:
                # `possible_flips` were valid.
                # This includes cases when it was empty.
                cells_to_flip.extend(possible_flips)
                break
            elif board[i][j] == OPEN:
                # `possible_flips` were invalid.
                break

            # Go to the next cell.
            i += direction[0]
            j += direction[1]

    return cells_to_flip


def place(board, i, j, turn):
    '''
    Returns an updated board with a stone of `turn` placed on (i, j).
    '''
    assert board[i][j] == OPEN
    board[i][j] = turn
    return board


def flip(board, cells):
    '''
    Returns an updated board with `cells` flipped.
    '''
    for (i, j) in cells:
        assert board[i][j] != OPEN
        board[i][j] = opponent(board[i][j])
    return board


def play():
    '''
    Main function that handles the gameplay.
    '''
    # Initialize variables.
    board = INITIAL_BOARD
    turn = FIRST
    pass_count = 0

    # The main game loop.
    while True:
        # A dictionary with placeable cells as key and the
        # corresponding list of cells to flip as its value.
        cells_to_place = {}

        # Iterate thorugh all cells and find which cells are able to
        # have a stone placed on them.
        for i in range(0, 8):
            for j in range(0, 8):
                if board[i][j] != OPEN:
                    continue
                cells_to_flip = get_cells_to_flip(board, turn, i, j)
                if len(cells_to_flip) > 0:
                    cells_to_place[(i, j)] = cells_to_flip

        # If no stone can be placed, we either pass or end the game
        # depending on the pass count.
        if len(cells_to_place.keys()) == 0:
            if pass_count == 1:
                break
            else:
                pass_count += 1
                turn = opponent(turn)
                continue

        # Show the board to the user.
        print(show_board(board, cells_to_place.keys()))
        print(f"{stone(turn)}'s turn!")

        # Try to get valid user input.
        while True:
            try:
                user_i = int(input("i: "))
                user_j = int(input("j: "))
            except ValueError:
                print("Invalid input. Please try again.")
                continue

            if not is_inside(user_i, user_j):
                print("Invalid input. Please try again.")
                continue

            if board[user_i][user_j] != OPEN:
                print("The cell is not open. Please try again.")
                continue

            if (user_i, user_j) not in cells_to_place.keys():
                print("The cell is not placeable. Please try again.")
                continue
            break

        # Update the board.
        board = place(board, user_i, user_j, turn)
        board = flip(board, cells_to_place[(user_i, user_j)])

        # Change the turn.
        turn = opponent(turn)

    # Handle gameover.
    print("---- GAME OVER ----")
    print(show_board(board))

    first_count = sum(cell == FIRST for row in board for cell in row)
    second_count = sum(cell == SECOND for row in board for cell in row)
    print(f"{stone(FIRST)}: {first_count}")
    print(f"{stone(SECOND)}: {second_count}")

    if first_count == second_count:
        print("It's a draw!")
    else:
        winner = FIRST if first_count > second_count else SECOND
        print(f"{stone(winner)} wins!")


if __name__ == "__main__":
    play()
