from __future__ import annotations

import pygame
from dataclasses import dataclass
from typing import Tuple

from .core.game_state import GameState

Color = Tuple[int, int, int]


@dataclass
class Theme:
    background: Color = (30, 30, 30)
    grid: Color = (45, 45, 45)
    snake_head: Color = (255, 204, 0)
    snake_body: Color = (255, 255, 255)
    food: Color = (240, 80, 80)
    text: Color = (220, 220, 220)
    overlay: Color = (0, 0, 0, 180)


class GameRenderer:
    def __init__(self, cell_size: int = 24, theme: Theme | None = None) -> None:
        self.cell_size = cell_size
        self.theme = theme or Theme()

    def draw(self, screen: pygame.Surface, state: GameState) -> None:
        screen.fill(self.theme.background)
        self._draw_grid(screen, state)
        self._draw_food(screen, state)
        self._draw_snake(screen, state)
        self._draw_score(screen, state)
        if state.game_over:
            self._draw_game_over(screen, state)

    def _draw_grid(self, screen: pygame.Surface, state: GameState) -> None:
        width, height = state.grid_size
        for x in range(width):
            for y in range(height):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, self.theme.grid, rect, width=1)

    def _draw_food(self, screen: pygame.Surface, state: GameState) -> None:
        fx, fy = state.food
        rect = pygame.Rect(
            fx * self.cell_size + 2,
            fy * self.cell_size + 2,
            self.cell_size - 4,
            self.cell_size - 4,
        )
        pygame.draw.rect(screen, self.theme.food, rect, border_radius=6)

    def _draw_snake(self, screen: pygame.Surface, state: GameState) -> None:
        for index, (x, y) in enumerate(state.snake.segments()):
            rect = pygame.Rect(
                x * self.cell_size + 1,
                y * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2,
            )
            color = self.theme.snake_head if index == 0 else self.theme.snake_body
            pygame.draw.rect(screen, color, rect, border_radius=4)

    def _draw_score(self, screen: pygame.Surface, state: GameState) -> None:
        font = pygame.font.SysFont("arial", 20)
        text = font.render(f"Score: {state.score}", True, self.theme.text)
        screen.blit(text, (10, 10))

    def _draw_game_over(self, screen: pygame.Surface, state: GameState) -> None:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(self.theme.overlay)
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("arial", 36, bold=True)
        small = pygame.font.SysFont("arial", 20)
        label = font.render("Game Over", True, self.theme.text)
        prompt = small.render("Press Enter to play again or Esc to quit", True, self.theme.text)

        rect = label.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        screen.blit(label, rect)
        prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        screen.blit(prompt, prompt_rect)
