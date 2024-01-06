# Define constants.
OPEN = 0
FIRST = 1
SECOND = 2

DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1),
              (-1, 0), (-1, -1), (0, -1), (1, -1)]

INITIAL_BOARD = [[OPEN, OPEN, OPEN, OPEN,   OPEN,   OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN,   OPEN,   OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN,   OPEN,   OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, FIRST,  SECOND, OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, SECOND, FIRST,  OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN,   OPEN,   OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN,   OPEN,   OPEN, OPEN, OPEN],
                 [OPEN, OPEN, OPEN, OPEN,   OPEN,   OPEN, OPEN, OPEN]]


def stone(turn):
    """Get the string representation of the stone.

    Args:
        turn (int): OPEN, FIRST, or SECOND.

    Returns:
        str: The string of the turn (' ', '○' or '●').
    """
    if turn == FIRST:
        return "○"
    elif turn == SECOND:
        return "●"
    elif turn == OPEN:
        return " "
    else:
        raise ValueError("Unexpected turn value.")


def opponent(turn):
    """Get the opponent turn.

    Args:
        turn (int): FIRST or SECOND (and not OPEN).

    Returns:
        int: The opponent of the turn.
    """
    if turn == FIRST:
        return SECOND
    elif turn == SECOND:
        return FIRST
    else:
        raise ValueError("Unexpected turn value.")


def is_inside(i, j):
    """Check if (i, j) is inside the board.

    Args:
        i (int): The row.
        j (int): The column.

    Returns:
        bool: Whether the cell (i, j) is inside the board.
    """
    if i < 0 or i >= 8:
        return False
    if j < 0 or j >= 8:
        return False
    return True


def show_board(board, cells_to_place=[]):
    """Get the string representation of the board.

    Args:
        board (list[list[int]]): The board.
        cells_to_place (list[tuple[int, int]], optional):
            The cells that can be placed on. Defaults to [].

    Returns:
        str: The board as string.
    """
    board_str = " : 0 1 2 3 4 5 6 7\n-------------------\n"
    for i in range(0, 8):
        board_str += f"{i}: "
        for j in range(0, 8):
            if (i, j) in cells_to_place:
                board_str += "+"
            else:
                board_str += stone(board[i][j])
            board_str += " "
        board_str += "\n"
    return board_str


def get_cells_to_flip(board, turn, placed_i, placed_j):
    """Get the list of cells that should be flipped if a stone is
       placed on (placed_i, placed_j).

    Args:
        board (list[list[int]]): The board.
        turn (int): The turn of the placed stone.
                    FIRST or SECOND (and not OPEN).
        placed_i (int): Row of the stone to be placed on.
        placed_j (int): Column of the stone to be placed on.

    Returns:
        list[tuple[int, int]]: List of cells that should be flipped.
    """
    # Check arguments.
    assert turn != OPEN
    assert is_inside(placed_i, placed_j)

    # Create the result list.
    cells_to_flip = []

    # Test each of the 8 directions from the placed cell.
    for (direction_i, direction_j) in DIRECTIONS:
        i = placed_i + direction_i
        j = placed_j + direction_j

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
            i += direction_i
            j += direction_j

    return cells_to_flip


def place(board, turn, i, j):
    """Place a stone of type `turn` on (i, j).

    Args:
        board (list[list[int]]): The board.
        i (int): Row of the cell to place the stone on.
        j (int): Column of the cell to place the stone on.
        turn (int): The turn of the stone. FIRST or SECOND (and not OPEN).

    Returns:
        list[list[int]]: The updated board.
    """
    assert board[i][j] == OPEN
    board[i][j] = turn
    return board


def flip(board, cells):
    """Flip stones on `cells`.

    Args:
        board (list[list[int]]): The board.
        cells (list[tuple[int, int]]): The cells that should be flipped.

    Returns:
        list[list[int]]: The updated board.
    """
    for (i, j) in cells:
        assert board[i][j] != OPEN
        board[i][j] = opponent(board[i][j])
    return board


def play(give_hint=False):
    """Main function that handles the gameplay.

    Args:
        give_hint (bool, optional): Whether hint (+) should be given.
                                    Defaults to False.
    """
    # Initialize variables.
    board = INITIAL_BOARD
    turn = FIRST
    pass_count = 0

    # The main game loop.
    while True:
        # A dictionary with placeable cells and corresponding flips.
        # (dict[tuple[int, int], list[tuple[int, int]]])
        # ex.
        # {
        #   (2, 5): [(2, 4), (2, 3)],
        #   (3, 6): [(4, 6), (3, 6), (2, 6)],
        #   (1, 1): [(2, 2)]
        # }
        # This means that if a stone of `turn` is placed on (2, 5) then
        # cells (2, 4) and (2, 3) should be flipped.
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
        if give_hint:
            print(show_board(board, cells_to_place.keys()))
        else:
            print(show_board(board))
        print(f"{stone(turn)}'s turn!")

        # Try to get valid user input.
        while True:
            try:
                user_i = int(input("i: "))
                user_j = int(input("j: "))
            except ValueError:
                # The input cannot be parsed as `int`.
                print("Invalid input. Please try again.")
                continue

            if not is_inside(user_i, user_j):
                print("This cell not inside the board. Please try again.")
                continue

            if board[user_i][user_j] != OPEN:
                print("This cell is not open. Please try again.")
                continue

            if (user_i, user_j) not in cells_to_place.keys():
                print("That doesn't flip any of the stones. Please try again.")
                continue

            break

        # Update the board.
        board = place(board, turn, user_i, user_j)
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
    give_hint = input("Do you want hints(+)? (y/n): ")
    if give_hint == "y":
        play(True)
    else:
        play()
