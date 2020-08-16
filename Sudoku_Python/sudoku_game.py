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
    # Checks the player's grid against the solution grid
    # If something doesn't match returns it's coordinates
    for row in range(sudoku_grid.size):
        for col in range(sudoku_grid.size):
            if sudoku_grid.get_cell(row, col) != solution_grid.get_cell(row, col):
                return row + 1, col + 1
            else:
                continue
    return None

class Button():
    def __init__(self, x, y, width, height, color, font_type, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = Rect(x, y, width, height)
        self.font_type = font_type
        self.surface = cell_font.render(text, True, color)
    
    def get_text_center(self):
        self.text_x = (self.width - self.surface.get_width()) / 2
        self.text_y = (self.height - self.font_type.get_linesize()) / 2

    def draw(self, screen):
        self.get_text_center()
        screen.blit(self.surface, (self.x + self.text_x, self.y + self.text_y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640), 0, 32)

    button_width = 100
    button_height = 50
    button_y = grid_size + grid_coor[1]
    button_x = ((grid_size / 2) - (button_width / 2)) + grid_coor[0]

    solve_button = Button(button_x, button_y, 100, 50, COLOR_INACTIVE, cell_font, 'SOLVE')
    yes_button = Button(button_x + 110, button_y, 100, 50, COLOR_INACTIVE, cell_font, 'YES')

    button_x = ((grid_size / 2) - (225 / 2)) + grid_coor[0]
    status_button = Button(button_x, 25, 225, 50, COLOR_INACTIVE, cell_font, 'CONGRATULATIONS')
    
    temp_buttons = []

    running = True

    while running:
        screen.fill((255, 255, 255))
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
                if solve_button.rect.collidepoint(event.pos):
                    temp_buttons.append(yes_button)

                if yes_button.rect.collidepoint(event.pos):
                    bad_coor = check_solution()
                    if bad_coor:
                        status_button.surface = cell_font.render(
                            'Bad row: {}, col: {}'.format(
                                bad_coor[0], bad_coor[1]), 
                            True, 
                            COLOR_INACTIVE
                        )
                        temp_buttons.append(status_button)
                    else:
                        status_button.surface = cell_font.render(
                            'CONGRATULATIONS!', True, COLOR_INACTIVE)
                        temp_buttons.append(status_button)

                elif not solve_button.rect.collidepoint(event.pos):
                    temp_buttons = []
                    active = False

        for button in temp_buttons:
            pygame.draw.rect(screen, COLOR_LOCKED, button, 2)
            if button.x == yes_button.x:
                yes_button.draw(screen)

            elif button.x == status_button.x:
                status_button.draw(screen)

        for cell in grid_cells:
            pygame.draw.rect(screen, COLOR_LOCKED, cell, 5)

        for cell in cells:
            cell.draw(screen)

        pygame.draw.rect(screen, COLOR_INACTIVE, solve_button, 2)

        solve_button.draw(screen)

        pygame.display.update()

    print(sudoku_grid.print_grid())


if __name__ == "__main__":
    main()
