import copy
import pygame

from typing import List

from ui.cell import Cell, CELL_SIZE, BORDER_WIDTH
from utils import color
from logic import solver

pygame.init()

BOARD_SIZE = CELL_SIZE * 9 + 2 * BORDER_WIDTH
BOARD_POS = (50, 50)

GUI_SIZE = (BOARD_SIZE + 2 * BOARD_POS[0], BOARD_SIZE + 2 * BOARD_POS[1])
GUI_TITLE = 'Sudoku Solver'

class GUI: 
    def __init__(self, data: List[List[int]]):
        self.screen = pygame.display.set_mode(GUI_SIZE)
        pygame.display.set_caption(GUI_TITLE)

        self.data = data
        self.initial_data = copy.deepcopy(data)
        self.solution_data = solver.solve(copy.deepcopy(data))
        self.running_sim = False

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                x = BOARD_POS[0] + BORDER_WIDTH + col * CELL_SIZE
                y = BOARD_POS[1] + BORDER_WIDTH + row * CELL_SIZE
                self.cells[row][col] = Cell(self.screen, (x, y), data[row][col])
        self.selected_cell = None

        x, y = BOARD_POS
        self.outline = [
            pygame.Rect((x, y), (BOARD_SIZE, BORDER_WIDTH)),
            pygame.Rect((x + BOARD_SIZE - BORDER_WIDTH, y), (BORDER_WIDTH, BOARD_SIZE)),
            pygame.Rect((x, y + BOARD_SIZE - BORDER_WIDTH), (BOARD_SIZE, BORDER_WIDTH)),
            pygame.Rect((x, y), (BORDER_WIDTH, BOARD_SIZE))
        ]
    
    def run(self) -> None:
        ''' Runs the pygame gameloop. Should be called directly after initialization. '''
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.screen.fill(color.WHITE)

            self.update()
            self.render()

            pygame.display.flip()

    def update(self) -> None:
        ''' Updates the grid when running simulation '''
        if self.running_sim:
            try:
                func = next(self.simulation_gen)
                func()
            except StopIteration:
                self.solving_finished = True
                self.cancel_simulation()

    def render(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.render()

        for line in self.outline:
            pygame.draw.rect(self.screen, color.BLACK, line)

    def handle_event(self, event: pygame.event) -> None:
        ''' Dispatches key and mouse events '''
        if event.type == pygame.QUIT: 
            self.running = False

        if self.running_sim:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.cancel_simulation()
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

    def set_value(self, row: int, col: int, value: int) -> None:
        self.data[row][col] = value
        self.cells[row][col].set_value(value)

    def reset(self) -> None:
        for row in range(9):
            for col in range(9):
                self.set_value(row, col, self.initial_data[row][col])
                self.cells[row][col].set_color(color.BLACK)

    def is_correct(self, cell: Cell, num: int) -> bool:
        ''' Checks if the given num is the solution for the given cell '''
        for row, cells in enumerate(self.cells):
            for col, c in enumerate(cells):
                if c == cell:
                    return self.solution_data[row][col] == num

    def select_cell_at(self, pos: List[int]) -> None:
        '''
        Selects the cell at the given position, if there is a cell there
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
    
    def cancel_simulation(self):
        self.running_sim = False
        if not self.solving_finished:
            self.reset()

    def start_simulation(self):
        '''
        Sets flags to run simulation and creates a simulation generator of the current board
        '''
        self.running_sim = True
        self.simulation_gen = self._gen_simulation()

    def _gen_simulation(self):
        '''
        Solves the board at its current stage, then yields a function to call
        that shows the step the solver took to the user
        '''
        self.solving_finished = False
        solving_log = []
        solver.solve(copy.deepcopy(self.data), log_list=solving_log)
        for log_entry in solving_log:
            def func():
                row = log_entry['pos'][0]
                col = log_entry['pos'][1]
                if log_entry['action'] == 'PUT':
                    self.set_value(row, col, log_entry['num'])
                    self.cells[row][col].set_color(color.GREEN)
                elif log_entry['action'] == 'INVALID':
                    self.set_value(row, col, log_entry['num'])
                    self.cells[row][col].set_color(color.BLACK)
                elif log_entry['action'] == 'REMOVE':
                    self.set_value(row, col, 0)
                    self.cells[row][col].set_color(color.RED)
            yield func
        