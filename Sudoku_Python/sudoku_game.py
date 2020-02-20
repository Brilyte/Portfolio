import pygame
from pygame.locals import *
from sudoku import SudokuGrid
from pygame_textinput import TextInput

SCREENRECT = Rect(0, 0, 640, 480)
COLOR_INACTIVE = pygame.Color(223, 97, 97)
COLOR_ACTIVE = pygame.Color(0, 0, 255)
COLOR_LOCKED = pygame.Color(0, 0, 0)

pygame.font.init()
font_path = pygame.font.match_font('dejavusansextralight')
player_font = pygame.font.Font(font_path, 20)
player_font.set_bold(True)
locked_font = pygame.font.Font(font_path, 20)
locked_font.set_bold(True)

# textinput = TextInput('hello', 'dejavusansextralight')

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, row, col, text='', locked=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = COLOR_LOCKED
        self.txt_surface = player_font.render(text, True, self.color)
        self.active = False
        self.row = row
        self.col = col
        self.width = 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the rect.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            self.color = COLOR_INACTIVE if self.active else COLOR_LOCKED
            self.width = 4 if self.active else 1

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                if len(self.text) > 1:
                    self.text = self.text[:1]
                # Re-render the text.
                sudoku_grid.fill_cell(self.row + 1, self.col + 1, self.text)
                self.txt_surface = player_font.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text. Use x and y variance to center text!
        # center_x = self.rect.x  # Left
        # center_y = (self.rect.y)  # Top
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y))
        
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
x, y = 0, 0  # coordinates of starting corner will be this

cells = []
grid_cells = []

for row in range(sudoku_grid.size):
    x = 0
    for col in range(sudoku_grid.size):
        val = sudoku_grid.get_cell(row, col)
        if val == 0:
            cells.append(Cell(x, y, 25, 25, row, col, text=''))
        else:
            cells.append(LockedCell(x, y, 25, 25, row, col, text=str(val)))
        if (x == 0 or x % 75 == 0) and (y == 0 or y % 75 == 0):
            grid_cells.append(Rect(x, y, 75, 75))
        x += 25
    y += 25

main_grid = Rect(0, 0, 25*9, 25*9)

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.draw.rect(screen, COLOR_LOCKED, main_grid, 2)

    white = (255,255,255)
    running = True

    while running:
        screen.fill(white)
        pygame.draw.rect(screen, COLOR_LOCKED, main_grid, 5)
        # event handling, gets all event from the event queue
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
            for cell in cells:
                cell.handle_event(event)

        for cell in grid_cells:
            pygame.draw.rect(screen, COLOR_LOCKED, cell, 5)

        for cell in cells:
            cell.draw(screen)

        pygame.display.update()

    print(sudoku_grid.print_grid())

if __name__=="__main__":
    main()