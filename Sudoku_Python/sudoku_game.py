import pygame
import copy
from pygame.locals import Color, Rect
from pygame.constants import (MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE, QUIT)
from sudoku import SudokuGrid

SCREENRECT = Rect(0, 0, 640, 640)
COLOR_INACTIVE = Color(223, 97, 97)
COLOR_ACTIVE = Color(0, 0, 255)
COLOR_LOCKED = Color(0, 0, 0)

pygame.font.init()
font_path = pygame.font.match_font('dejavusansextralight')
player_font = pygame.font.Font(font_path, 20)
player_font.set_bold(True)
locked_font = pygame.font.Font(font_path, 20)
locked_font.set_bold(True)
cell_font = pygame.font.Font(font_path, 20)


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, row, col, text='', locked=False):
        
        self.rect = pygame.Rect(x, y, w, h)
        self.cell_height = h
        self.cell_width = w
        self.text = text
        self.color = COLOR_LOCKED
        self.txt_surface = cell_font.render(text, True, self.color)
        self.active = False
        self.row = row
        self.col = col
        self.width = 1

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the rect.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            self.color = COLOR_INACTIVE if self.active else COLOR_LOCKED
            self.width = 4 if self.active else 1

        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key in range(49, 58):
                    # Only allow keys from 1-9
                    self.text += event.unicode

                if len(self.text) > 1:
                    # Only allow one entry at a time
                    self.text = self.text[:1]

                # Re-render the text.
                sudoku_grid.fill_cell(self.row + 1, self.col + 1, self.text)
                self.txt_surface = cell_font.render(
                    self.text, True, self.color)

    def draw(self, screen):
        # Blit the text. Use x and y variance to center text!
        text_x = (self.cell_width - self.txt_surface.get_width()) / 2
        text_y = (self.cell_height - cell_font.get_linesize()) / 2
        screen.blit(self.txt_surface, (self.rect.x + text_x, self.rect.y + text_y))

        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, self.width)


class LockedCell(Cell):
    def __init__(self, x, y, w, h, row, col, text):
        super().__init__(x, y, w, h, row, col, text=text)
        self.color = COLOR_LOCKED
        self.txt_surface = locked_font.render(text, True, self.color)

    def handle_event(self, event):
        pass


sudoku_grid = SudokuGrid(9, 0)
sudoku_grid.enter_puzzle('easy_puzzle.txt')

solution_grid = SudokuGrid(9, 0)
solution_grid.enter_puzzle(sudoku_grid.solution_file)
solution_grid.print_grid()


def fill_cell(sudoku_grid, cells, x, y, row, col, cell_size):
    val = sudoku_grid.get_cell(row, col)
    if val == 0:
        cells.append(Cell(x, y, cell_size, cell_size, row, col, text=''))
    else:
        cells.append(LockedCell(x, y, cell_size, cell_size, row, col, text=str(val)))

def better_fill(sudoku_grid, grid_size, starting_corner):
    cell_size = int(grid_size / sudoku_grid.size) # 225 / 9 = 25
    inner_box_size = int((sudoku_grid.size / 3) * cell_size) # 9 /3 = 3 * 25 = 75

    cells = []
    grid_cells = []

    start_x, start_y = starting_corner
    x, y = copy.copy(starting_corner)
    
    for row in range(sudoku_grid.size):
        x = start_x
        for col in range(sudoku_grid.size):
            fill_cell(sudoku_grid, cells, x, y, row, col, cell_size)

            # If x is at starting coor, or if its coordinate - offset is divisible by inner_box_size
            if (x == start_x or (x - start_x) % inner_box_size == 0) and \
                (y == start_y or (y - start_y) % inner_box_size == 0):
                grid_cells.append(Rect(x, y, inner_box_size, inner_box_size))
            x += cell_size
        y += cell_size

    return cells, grid_cells

grid_size = 400
grid_coor = (100, 100)
cells, grid_cells = better_fill(sudoku_grid, grid_size, grid_coor)


def get_text_center(button, surface, font_type):
        text_x = (button.width - surface.get_width()) / 2
        text_y = (button.height - font_type.get_linesize()) / 2
        return (text_x, text_y)

def check_solution():
    for row in range(sudoku_grid.size):
        for col in range(sudoku_grid.size):
            if sudoku_grid.get_cell(row, col) != solution_grid.get_cell(row, col):
                return row + 1, col + 1
            else:
                continue
    return None

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 640), 0, 32)

    button_width = 100
    button_height = 50
    button_y = grid_size + grid_coor[1]
    button_x = ((grid_size / 2) - (button_width / 2)) + grid_coor[0]
    buttonR = Rect(button_x, button_y, button_width, button_height)
    solve_surface = cell_font.render('SOLVE', True, COLOR_INACTIVE)

    buttonY = Rect(button_x + 110, button_y, button_width, button_height)
    yes_surface = cell_font.render('YES', True, COLOR_INACTIVE)

    button_x = ((grid_size / 2) - (225 / 2)) + grid_coor[0]
    buttonBad = Rect(button_x, 25, 225, button_height)
    bad_surface = cell_font.render('CONGRATULATIONS!', True, COLOR_INACTIVE)

    r_text_x, r_text_y = get_text_center(buttonR, solve_surface, cell_font)
    y_text_x, y_text_y = get_text_center(buttonY, yes_surface, cell_font)
    b_text_x, b_text_y = get_text_center(buttonBad, bad_surface, cell_font)
    
    temp_buttons = []

    running = True

    while running:
        screen.fill((255, 255, 255))
        # pygame.draw.rect(screen, COLOR_LOCKED, main_grid, 5)
        # event handling, gets all event from the event queue
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False

            for cell in cells:
                cell.handle_event(event)

            active = False
            if event.type == MOUSEBUTTONDOWN:
                # If the user clicked on the rect.
                if buttonR.collidepoint(event.pos):
                    temp_buttons.append(buttonY)

                if buttonY.collidepoint(event.pos):
                    solution = check_solution()
                    if solution:
                        bad_surface = cell_font.render(
                            'Bad row: {}, col: {}'.format(
                                solution[0], solution[1]), 
                            True, 
                            COLOR_INACTIVE
                        )
                        temp_buttons.append(buttonBad)
                    else:
                        bad_surface = cell_font.render(
                            'CONGRATULATIONS!', True, COLOR_INACTIVE)
                        temp_buttons.append(buttonBad)

                elif not buttonR.collidepoint(event.pos):
                    temp_buttons = []
                    active = False

        for button in temp_buttons:
            pygame.draw.rect(screen, COLOR_LOCKED, button, 2)
            if button.x == buttonY.x:
                screen.blit(yes_surface, (button.x + y_text_x, button.y + y_text_y))
            elif button.x == buttonBad.x:
                b_text_x, b_text_y = get_text_center(buttonBad, bad_surface, cell_font)
                screen.blit(bad_surface, (button.x + b_text_x, button.y + b_text_y))

        for cell in grid_cells:
            pygame.draw.rect(screen, COLOR_LOCKED, cell, 5)

        for cell in cells:
            cell.draw(screen)

        pygame.draw.rect(screen, COLOR_INACTIVE, buttonR, 2)

        screen.blit(solve_surface, (buttonR.x + r_text_x, buttonR.y + r_text_y))

        pygame.display.update()

    print(sudoku_grid.print_grid())


if __name__ == "__main__":
    main()
