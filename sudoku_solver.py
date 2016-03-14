"""Sudoku Solver"""

###############################################################################
## (1) Logic

# First, we want to set all the legal values to every cell
### If a cell has an assigned value (from the puzzle), give it that value
### Else, set the possible values from 1 - 9

# Second, check all cells that only have a single value and eliminate that
# from all of its peers.

# Third, if a group of cells only has one possible place for a value, set that
# spot to the value.


###############################################################################
## (2) Setting up the grid

# A1 A2 A3 | A4 A5 A6 | A7 A8 A9
# B1 B2 B3 | B4 B5 B6 | B7 B8 B9
# C1 C2 C3 | C4 C5 C6 | C7 C8 C9
# _________+__________+_________
# D1 D2 D3 | D4 D5 D6 | D7 D8 D9
# E1 E2 E3 | E4 E5 E6 | E7 E8 E9
# F1 F2 F3 | F4 F5 F6 | F7 F8 F9
# _________+__________+_________
# G1 G2 G3 | G4 G5 G6 | G7 G8 G9
# H1 H2 H3 | H4 H5 H6 | H7 H8 H9
# I1 I2 I3 | I4 I5 I6 | I7 I8 I9

# Each element has 20 other related elements: 8 horizontal, 8 vertical,
# and 8 in the same square
# For example, A1 has the following related elements:

# A1 A2 A3 | A4 A5 A6 | A7 A8 A9
# B1 B2 B3 |          |
# C1 C2 C3 |          |
# _________+__________+_________
# D1       |          |
# E1       |          |
# F1       |          |
# _________+__________+_________
# G1       |          |
# H1       |          |
# I1       |          |


###############################################################################
## (3) Helper Functions

def set_grid(puzzle):
    """Takes a puzzle as a list and assigns it a grid unit in a dict.

    Puzzles are input as a list and empty squares are set as 0.
    e.g. puzzle = [7, 9, 0, 0, 0, 0, 3, 0, 0,
                   0, 0, 0, 0, 0, 6, 9, 0, 0,
                   8, 0, 0, 0, 3, 0, 0, 7, 6,
                   0, 0, 0, 0, 0, 5, 0, 0, 2,
                   0, 0, 5, 4, 1, 8, 7, 0, 0,
                   4, 0, 0, 7, 0, 0, 0, 0, 0,
                   6, 1, 0, 0, 9, 0, 0, 0, 8,
                   0, 0, 2, 3, 0, 0, 0, 0, 0,
                   0, 0, 9, 0, 0, 0, 0, 5, 4]

        would represent the puzzle:
            7 9 . | . . . | 3 . .
            . . . | . . 6 | 9 . .
            8 . . | . 3 . | . 7 6
            ______+_______+______
            . . . | . . 5 | . . 2
            . . 5 | 4 1 8 | 7 . .
            4 . . | 7 . . | . . .
            ______+_______+______
            6 1 . | . 9 . | . . 8
            . . 2 | 3 . . | . . .
            . . 9 | . . . | . 5 4
    """

    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    all_digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    # First generate a list of all grid elements
    grid_elements = [r + c for r in rows for c in cols]

    # Set empty Python dictionary for grid elements and values
    elements_values = dict()

    # Loop through the puzzle and set the grid elements and values to dict
    for i in xrange(puzzle):
        if puzzle[i] == 0:
            elements_values[grid_elements[i]] = all_digits
        else:
            elements_values[grid_elements[i]] = [puzzle[i]]

    return elements_values


def get_all_related(element):
    """Given the position of an element, find a set of all related elements.

    e.g. for element 'A1', it would return the following list:

        set(A2, A3, A4, A5, A6, A7, A8, A9, B1, B2,
         B3, C1, C2, C3, D1, E1, F1, G1, H1, I1)

        A1 A2 A3 | A4 A5 A6 | A7 A8 A9
        B1 B2 B3 |          |
        C1 C2 C3 |          |
        _________+__________+_________
        D1       |          |
        E1       |          |
        F1       |          |
        _________+__________+_________
        G1       |          |
        H1       |          |
        I1       |          |
    """

    # Parse element row (letter) and digit (col)
    row = element[0]
    digit = element[1]

    # All rows and column possibilities
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Initiate an empty list to hold all elements
    related_elements = set()

    # Add all elements in the same column
    for r in rows:
        related_elements.add(r + digit)

    # Add all elements in the same row
    for c in cols:
        related_elements.add(row + c)

    # Add all the elements in the same 'square' as the given element
    if row in ['A', 'B', 'C']:
        if digit in ['1', '2', '3']:
            for elem in [r + c for r in ['A', 'B', 'C'] for c in ['1', '2', '3']]:
                related_elements.add(elem)
        elif digit in ['4', '5', '6']:
            for elem in [r + c for r in ['A', 'B', 'C'] for c in ['4', '5', '6']]:
                related_elements.add(elem)
        elif digit in ['7', '8', '9']:
            for elem in [r + c for r in ['A', 'B', 'C'] for c in ['7', '8', '9']]:
                related_elements.add(elem)
    elif row in ['D', 'E', 'F']:
        if digit in ['1', '2', '3']:
            for elem in [r + c for r in ['D', 'E', 'F'] for c in ['1', '2', '3']]:
                related_elements.add(elem)
        elif digit in ['4', '5', '6']:
            for elem in [r + c for r in ['D', 'E', 'F'] for c in ['4', '5', '6']]:
                related_elements.add(elem)
        elif digit in ['7', '8', '9']:
            for elem in [r + c for r in ['D', 'E', 'F'] for c in ['7', '8', '9']]:
                related_elements.add(elem)
    elif row in ['G', 'H', 'I']:
        if digit in ['1', '2', '3']:
            for elem in [r + c for r in ['G', 'H', 'I'] for c in ['1', '2', '3']]:
                related_elements.add(elem)
        elif digit in ['4', '5', '6']:
            for elem in [r + c for r in ['G', 'H', 'I'] for c in ['4', '5', '6']]:
                related_elements.add(elem)
        elif digit in ['7', '8', '9']:
            for elem in [r + c for r in ['G', 'H', 'I'] for c in ['7', '8', '9']]:
                related_elements.add(elem)

    # Pop the element itself -- we only want the related elements to compare
    related_elements.remove(element)

    return related_elements

###############################################################################
## (4) Solving the Sudoku

def solve_sudoku(puzzle):
    """Solving the sudoku."""

    # Get dictionary based on current sudoku puzzle
    elements_values = set_grid(puzzle)
