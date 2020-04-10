import pygame
pygame.init()

from .board import Board, BOARD_SIZE, BOARD_POS
from utils import color

GUI_SIZE = (BOARD_SIZE + 2 * BOARD_POS[0], BOARD_SIZE + 2 * BOARD_POS[1])
GUI_TITLE = 'Sudoku Solver'

class GUI:
    def __init__(self, board_data):
        self.screen = pygame.display.set_mode(GUI_SIZE)
        pygame.display.set_caption(GUI_TITLE)

        self.board = Board(self.screen, board_data)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False
                else:
                    self.board.handle_event(event)

            self.screen.fill(color.WHITE)

            self.board.update()
            self.board.render()

            pygame.display.flip()
