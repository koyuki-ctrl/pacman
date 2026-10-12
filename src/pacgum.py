import random
from pyray import draw_circle

# Bits du MazeGenerator (voir maze.py)
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

ALL_WALLS = NORTH | EAST | SOUTH | WEST  # = 15


class Pacgum:
    def __init__(self, cell_x: int, cell_y: int, super_pacgum: bool = False):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.super_pacgum = super_pacgum
        self.eaten = False

    def draw(self, cell_w, cell_h, offset_x, offset_y, color) -> None:
        cx = offset_x + self.cell_x * cell_w + cell_w // 2
        cy = offset_y + self.cell_y * cell_h + cell_h // 2
        radius = max(3, cell_w // 5) if self.super_pacgum else max(1, cell_w // 10)
        draw_circle(cx, cy, radius, color)


class PacgumManager:
    def __init__(self, grid: list[list[int]], nb_pacgum: int, seed: int | None = None):
        self.pacgums: list[Pacgum] = []
        if seed is not None:
            random.seed(seed)
        self._place(grid, nb_pacgum)

    @staticmethod
    def _is_walkable(grid, x: int, y: int) -> bool:
        """Une cellule est praticable si elle n'est PAS totalement fermée."""
        return (grid[y][x] & ALL_WALLS) != ALL_WALLS

    def _place(self, grid, nb_pacgum: int) -> None:
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        # 4 super pacgums aux coins … mais seulement si la cellule est praticable
        corners = [(0, 0), (cols - 1, 0), (0, rows - 1), (cols - 1, rows - 1)]
        corner_set = {
            (x, y) for (x, y) in corners
            if self._is_walkable(grid, x, y)
        }
        for (x, y) in corner_set:
            self.pacgums.append(Pacgum(x, y, super_pacgum=True))

        # Candidats : cellule praticable ET pas déjà utilisée par un super pacgum
        candidates = [
            (x, y)
            for y in range(rows)
            for x in range(cols)
            if self._is_walkable(grid, x, y) and (x, y) not in corner_set
        ]

        n = min(nb_pacgum, len(candidates))
        for (x, y) in random.sample(candidates, n):
            self.pacgums.append(Pacgum(x, y))

    def draw(self, cell_w, cell_h, offset_x, offset_y, color) -> None:
        for p in self.pacgums:
            if not p.eaten:
                p.draw(cell_w, cell_h, offset_x, offset_y, color)
