import copy
import pygame

from .cell import Cell, CELL_SIZE, BORDER_WIDTH
from utils import color
from logic import solver

BOARD_SIZE = CELL_SIZE * 9 + 2 * BORDER_WIDTH
BOARD_POS = (50, 50)

class Board: 
    def __init__(self, surface, data):
        self.data = data
        self.solution_data = solver.solve(copy.deepcopy(data))
        self.surface = surface
        self.running_sim = False

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                x = BOARD_POS[0] + BORDER_WIDTH + col * CELL_SIZE
                y = BOARD_POS[1] + BORDER_WIDTH + row * CELL_SIZE
                self.cells[row][col] = Cell(self.surface, (x, y), data[row][col])
        self.selected_cell = None

        x, y = BOARD_POS
        self.outline = [
            pygame.Rect((x, y), (BOARD_SIZE, BORDER_WIDTH)),
            pygame.Rect((x + BOARD_SIZE - BORDER_WIDTH, y), (BORDER_WIDTH, BOARD_SIZE)),
            pygame.Rect((x, y + BOARD_SIZE - BORDER_WIDTH), (BOARD_SIZE, BORDER_WIDTH)),
            pygame.Rect((x, y), (BORDER_WIDTH, BOARD_SIZE))
        ]
    
    def update(self):
        if self.running_sim:
            for row in range(9):
                for col in range(9):
                    self.cells[row][col].set_value(self.solution_data[row][col])

    def render(self):
        for row in self.cells:
            for cell in row:
                cell.render()

        for line in self.outline:
            pygame.draw.rect(self.surface, color.BLACK, line)


    def handle_event(self, event):
        if self.running_sim:
            if event.type == pygame.MOUSEBUTTONUP and event.key == pygame.K_ESCAPE:
                self.running_sim = False
            return

        if event.type == pygame.MOUSEBUTTONUP:
            self.select_cell_at(pygame.mouse.get_pos())

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1: self.selected_cell.set_provisional_value(1)
            if event.key == pygame.K_2: self.selected_cell.set_provisional_value(2)
            if event.key == pygame.K_3: self.selected_cell.set_provisional_value(3)
            if event.key == pygame.K_4: self.selected_cell.set_provisional_value(4)
            if event.key == pygame.K_5: self.selected_cell.set_provisional_value(5)
            if event.key == pygame.K_6: self.selected_cell.set_provisional_value(6)
            if event.key == pygame.K_7: self.selected_cell.set_provisional_value(7)
            if event.key == pygame.K_8: self.selected_cell.set_provisional_value(8)
            if event.key == pygame.K_9: self.selected_cell.set_provisional_value(9)

            if event.key == pygame.K_SPACE:
                self.start_simulation()
            if event.key == pygame.K_RETURN:
                self.confirm_provisional()

    def set_value(self, row, col, value):
        self.data[row][col] = value
        self.cells[row][col].set_value(value)

    def is_correct(self, cell, num):
        for row, cells in enumerate(self.cells):
            for col, c in enumerate(cells):
                if c == cell:
                    return self.solution_data[row][col] == num

    def select_cell_at(self, pos):
        '''
        Selects the cell at the given position, if there is a cell there
        :param pos: int[]
        '''
        row = (pos[1] - BOARD_POS[1] - BORDER_WIDTH) // CELL_SIZE
        col = (pos[0] - BOARD_POS[0] - BORDER_WIDTH) // CELL_SIZE

        if self.selected_cell: self.selected_cell.set_color(color.BLACK)
        try:
            cell = self.cells[row][col]
            cell.set_color(color.RED)
            self.selected_cell = cell
        except IndexError:
            self.selected_cell = None

    def confirm_provisional(self):
        '''
        If the user has set a provisional value for the current selected cell,
        that number will be confirmed if valid, else user will get one fault
        '''
        if self.selected_cell and self.selected_cell.provisional_value != 0:
            if self.is_correct(self.selected_cell, self.selected_cell.provisional_value):
                self.selected_cell.set_value(self.selected_cell.provisional_value)
        
    def start_simulation(self):
        '''
        Sets flags to run simulation and creates a simulation generator of the current board
        '''
        self.running_sim = True

    def _gen_simulation(self):
        '''
        Solves the board at its current stage, then yields a function to call
        that shows the step the solver took to the user
        '''
        pass
        