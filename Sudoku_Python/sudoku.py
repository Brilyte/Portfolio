
class SudokuGrid():

    # TODO create Cell class

    def __init__(self, size=9, empty=0):
        # Fill an empty grid with empty (0)
        self.grid = [[empty for x in range(size)] for y in range(size)]

        # Save this for future reference to what we consider 'empty' cells
        self.empty = empty
        self.size = size
        self.count = 0

    # Helper functions --------------------
    def pretty_print(self):
        for ent in range(self.size):
            print(self.grid[ent])

    def print_grid(self):
        grid = ''
        for i in range(self.size):
            # If at box bottom print divider

            if i > 0 and (i % (self.size / 3) == 0):
                grid += "---+---+---\n"

            # If at box side limit print divider
            for j in range(self.size):
                # grid += '|'
                if j > 0 and (j % (self.size / 3) == 0):
                    grid += ("|")
                grid += str(self.grid[i][j])
            grid += "\n"
        print(grid)

    # Cell functions ----------------------
    def get_cell(self, row, col):
        return self.grid[row][col]

    def fill_cell(self, row, col, val):
        # Fill cell with val at coordinates
        if (not str(val).isdigit()):
            self.grid[row - 1][col - 1] = 0
        else:
            self.grid[row - 1][col - 1] = int(val)

    def validate_cell(row, col, val):
        if not (
            (1 <= row <= 9) and \
            (1 <= col <= 9) and \
            (1 <= val <= 9)):
            raise ValueError('Row, col, and val must be between 1-9')
        return row-1, col-1

    def cell_is_empty(self, row, col):
        # Let's make this check non-CS row and col :P
        return self.grid[row-1][col-1] == self.empty

    def cell_is_valid(self, row, col, val):
        # Check if its valid to put value in row and col
        # I hate subtracting one all the time, convert in validate
        SudokuGrid.validate_cell(row, col, val)

        # Check Row
        for ent in range(self.size):
            # Check every value in row except ourselves
            if not(ent == col-1) and val == self.grid[row-1][ent]:
                # print('bad row selection', col, row, val)
                return False
            
        # Check Column
        for ent in range(self.size):
            # Only need to check every other value in column:
            # If we're NOT on chosen row (True) and value IS in that column (True)
            # this entry is NOT valid 
            if not(ent == row-1) and val == self.grid[ent][col-1]:
                # print('bad col selection')
                return False

        # Get coordinates of top corner of 3 x 3 box
        def get_coor(x):
            if 0 < col <= 2:
                coor = 0
            elif 3 < col <= 5:
                coor = 3
            elif 6 < col <= 8:
                coor = 6
            return coor

        def simplify_coor(x):
            boxsize = self.size / 3 # 3 * 3
            print(int(0 / boxsize) * 3) # 0
            print(int(1 / boxsize) * 3) # 0
            print(int(2 / boxsize) * 3) # 0
            print('')
            print(int(3 / boxsize) * 3) # 1
            print(int(4 / boxsize) * 3) # 1
            print(int(5 / boxsize) * 3) # 1
            print('')  
            print(int(6 / boxsize) * 3) # 2
            print(int(7 / boxsize) * 3) # 2
            print(int(8 / boxsize) * 3) # 2
            
            check = int(x / 3)

            if check == 0:
                coor = 0
            elif check == 1:
                coor = 3
            elif check == 2:
                coor = 6

            print(int(x / 3) * 3)

        # Check 3 x 3 box
        # Use integer math to get top corner of box, since rounds down to closest int
        boxsize = int(self.size / 3)
        corner_row = int((row-1) / 3) * 3
        corner_col = int((col-1) / 3) * 3
        for i in range(corner_row, corner_row + boxsize):
            for j in range(corner_col, corner_col + boxsize):
                # If we're NOT in selected cell, and cell HAS value: FAIL
                if (i != row-1 or j != col-1) and (val == self.grid[i][j]):
                    # print('bad box selection', i, j)
                    return False
        return True
        
    def clear_cell(self, row, col):
        # row, col = self.validate_cell(row, col)

        self.grid[row-1][col-1] = self.empty

    # Grid functions -----------------------
    def reset_grid(self):
        # Reset all cells to our emtpy value
        self.grid = [[self.empty for x in range(self.size)] for y in range(self.size)]

    def enter_puzzle(self, puzzle):
        
        def clean_puzzle(input_str):
            # Remove all extra characters so we can in puzzle properly
            new_puzzle = ''
            for ent in input_str:
                if ent in ['-', '+', '|', '\n']:
                    pass
                else:
                    new_puzzle += ent
            return new_puzzle

        def get_char(input_str):
            for ent in input_str:
                yield ent

        with open(puzzle, 'r' ,encoding='utf-8') as f:
            self.reset_grid()
            puzzle_str = f.read()
            if len(puzzle_str) not in [132, 133]:
                raise ValueError(
                    f'Bad format: {puzzle}. Wrong number of characters!')

            cleaned_puz = clean_puzzle(puzzle_str)
            if len(cleaned_puz) != 81:
                raise ValueError(
                    f'Bad format: {puzzle}. Wrong number of characters!')
            c = get_char(cleaned_puz)

            for row in range(self.size):
                for col in range(self.size):
                    entry = next(c)
                    if entry == '.':
                        val = 0
                    else:
                        val = int(entry)
                    self.fill_cell(row+1, col+1, val)

    def is_valid(self):
        # Check if grid is valid based on what's been filled in so far
        
        def line_has_duplicates(line):
            # Takes in list.
            # Returns True if duplicates other than 0 found
            used_digits = set()
            for cell_val in line:
                if cell_val == 0:
                    continue
                elif cell_val in used_digits:
                    return True
                else:
                    used_digits.add(cell_val)
            return False

        # Check row for duplicates
        for row in range(self.size):
            if line_has_duplicates(self.grid[row]):
                print('BAD ROW {}'.format(row + 1))
                return False

        # Check column for duplicates
        for col in range(self.size):
            column = []
            for row_cell in range(self.size):
                column.append(self.grid[row_cell][col])
            if line_has_duplicates(column):
                print('BAD COLUMN {}'.format(colum + 1))
                return False

        # Check 3 x 3 box
        # 0, 3, 6
        boxsize = int(self.size / 3)
        # Start at corner of each box:
        for row_corner in range(0, self.size, 3): # 0, 3, 9
            for col_corner in range(0, self.size, 3):
                #Fill list with box values (corner = row, col)
                box = []
                for row in range(row_corner, row_corner + boxsize):
                    for col in range(col_corner, col_corner + boxsize):
                        box.append(self.grid[row][col])
                if line_has_duplicates(box):
                    print('BAD BOX corner: {}:{}'.format(row_corner, col_corner))
                    return False

        return True

    def solve(self, row, col):
        # RECURSION Recursion recursion...
        # If we get past last row, it's a valid solution!
        if (row > self.size):
            return True

        if not self.cell_is_empty(row, col):
            if (col != self.size):
                return self.solve(row, col + 1)
            else:
                return self.solve(row + 1, 1)

        # If cell is empty we need to solve for it
        else:
            self.count += 1
            print(self.count)

            for value in range(1, self.size + 1):
                if self.cell_is_valid(row, col, value):
                    self.fill_cell(row, col, value)

                    if col < self.size:
                        if self.solve(row, col+1):
                            return True
                    else:
                        if self.solve(row+1, 1):
                            return True

            self.clear_cell(row, col)
            return False


def main():
    sudoku_grid = SudokuGrid(9, 0)

    print(sudoku_grid.enter_puzzle('puzzle.txt'))
    sudoku_grid.print_grid()
    # print('here', sudoku_grid.cell_is_valid(1, 1, 1))
    solved = sudoku_grid.solve(1, 1) # start at first corner
    if solved:
        assert(sudoku_grid.is_valid())
        print(f'Solution is valid: {sudoku_grid.is_valid()}')
        print(f'Solved in {sudoku_grid.count} iterations!')
    else:
        print('Puzzle in not solvable')
    
    print(sudoku_grid.print_grid())
    # sudoku_grid.pretty_print()

    # print(sudoku_grid.is_valid())

if __name__=="__main__":
    # call the main function
    main()
