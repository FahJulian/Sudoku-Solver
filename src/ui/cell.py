import pygame
from typing import List

from utils import color

CELL_SIZE = 50
BORDER_WIDTH = 2

class Cell:
    def __init__(self, surface: pygame.display, pos: List[int], value: int):
        self.surface = surface
        self.pos = pos
        self.value = value
        self.provisional_value = 0
        self.color = color.BLACK

        x, y = pos
        self.outline = [
            pygame.Rect((x, y), (CELL_SIZE, BORDER_WIDTH)),
            pygame.Rect((x + CELL_SIZE - BORDER_WIDTH, y), (BORDER_WIDTH, CELL_SIZE)),
            pygame.Rect((x, y + CELL_SIZE - BORDER_WIDTH), (CELL_SIZE, BORDER_WIDTH)),
            pygame.Rect((x, y), (BORDER_WIDTH, CELL_SIZE))
        ]

    def set_value(self, value:int) -> None:
        self.value = value

    def set_provisional_value(self, value: int) -> None:
        self.provisional_value = value

    def render(self) -> None:
        if self.value != 0:
            text = pygame.font.Font(None, 50).render(str(self.value), 1, color.BLACK)
            text_pos = text.get_rect()
            text_pos.center = (self.pos[0] + CELL_SIZE // 2, self.pos[1] + CELL_SIZE // 2)
            self.surface.blit(text, text_pos)

        elif self.provisional_value != 0:
            text = pygame.font.Font(None, 30).render(str(self.provisional_value), 1, color.BLACK)
            text_pos = text.get_rect()
            text_pos.center = (self.pos[0] + CELL_SIZE // 4, self.pos[1] + CELL_SIZE // 3)
            self.surface.blit(text, text_pos)

        for line in self.outline:
            pygame.draw.rect(self.surface, self.color, line)

    def set_color(self, color: List[int]) -> None:
        self.color = color
