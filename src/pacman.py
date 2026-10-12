import math
from pyray import draw_pixel, is_key_down, KeyboardKey

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
ALL_WALLS = 15

UP, RIGHT, DOWN, LEFT = (0, -1), (1, 0), (0, 1), (-1, 0)

# (mur de ma cellule, mur opposé de la cellule voisine)
WALL_BITS = {
    UP: (NORTH, SOUTH),
    RIGHT: (EAST, WEST),
    DOWN: (SOUTH, NORTH),
    LEFT: (WEST, EAST),
}
ROTATION = {RIGHT: 0, DOWN: 90, LEFT: 180, UP: 270}


class Pacman:
    def __init__(self, grid, color, speed: float = 4.0) -> None:
        self.grid = grid
        self.color = color
        self.speed = speed          # cellules par seconde

        self.cell = self.find_start_cell(grid)  # cellule actuelle
        self.nxt = self.cell                    # cellule visée
        self.progress = 0.0                     # 0 -> 1 entre cell et nxt
        self.dir = None                         # direction en cours
        self.wanted = None                      # direction demandée
        self.facing = None                      # orientation du dessin
        self.arrived = False                    # True quand il arrive au centre
        self.t = 0.0                            # temps d'animation de la bouche

    # ---------- placement ----------
    @staticmethod
    def find_start_cell(grid) -> tuple[int, int]:
        """Cellule praticable la plus proche du centre du labyrinthe."""
        rows, cols = len(grid), len(grid[0])
        mx, my = cols // 2, rows // 2
        walkable = [
            (x, y) for y in range(rows) for x in range(cols)
            if (grid[y][x] & ALL_WALLS) != ALL_WALLS
        ]
        return min(
            walkable,
            key=lambda c: (c[0] - mx) ** 2 + (c[1] - my) ** 2
        )

    # ---------- collision murs ----------
    def can_move(self, cell, d) -> bool:
        x, y = cell
        nx, ny = x + d[0], y + d[1]
        if not (0 <= ny < len(self.grid) and 0 <= nx < len(self.grid[0])):
            return False
        mine, theirs = WALL_BITS[d]
        return (
            not (self.grid[y][x] & mine)
            and not (self.grid[ny][nx] & theirs)
        )

    # ---------- logique ----------
    def read_input(self) -> None:
        if is_key_down(KeyboardKey.KEY_D):
            self.wanted = RIGHT
        elif is_key_down(KeyboardKey.KEY_A):
            self.wanted = LEFT
        elif is_key_down(KeyboardKey.KEY_W):
            self.wanted = UP
        elif is_key_down(KeyboardKey.KEY_S):
            self.wanted = DOWN

    def update(self, dt: float) -> None:
        self.arrived = False
        self.read_input()

        # demi-tour possible à tout moment
        if self.dir and self.wanted == (-self.dir[0], -self.dir[1]):
            self.cell, self.nxt = self.nxt, self.cell
            self.progress = 1.0 - self.progress
            self.dir = self.facing = self.wanted

        # avance vers la cellule suivante
        if self.dir:
            self.t += dt
            self.progress += self.speed * dt
            if self.progress >= 1.0:
                self.cell = self.nxt
                self.progress = 0.0
                self.dir = None
                self.arrived = True

        # au centre d'une cellule : on choisit la direction
        if self.dir is None:
            # 1) la direction demandée, 2) continuer tout droit
            for d in (self.wanted, self.facing):
                if d and self.can_move(self.cell, d):
                    self.dir = self.facing = d
                    self.nxt = (self.cell[0] + d[0], self.cell[1] + d[1])
                    break
            # sinon : mur devant -> il s'arrête

    # ---------- dessin ----------
    def pixel_pos(self, cw, ch, ox, oy) -> tuple[int, int]:
        x = self.cell[0] + (self.nxt[0] - self.cell[0]) * self.progress
        y = self.cell[1] + (self.nxt[1] - self.cell[1]) * self.progress
        return int(ox + (x + 0.5) * cw), int(oy + (y + 0.5) * ch)

    def draw(self, cw, ch, ox, oy) -> None:
        cx, cy = self.pixel_pos(cw, ch, ox, oy)
        r = max(2, min(cw, ch) // 2 - 3)    # reste à l'intérieur des murs
        rot = ROTATION[self.facing or RIGHT]
        mouth = 5 + 35 * abs(math.sin(self.t * 12))
        r2 = r * r

        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y > r2:
                    continue
                angle = (math.degrees(math.atan2(y, x)) - rot) % 360
                if mouth < angle < 360 - mouth:
                    draw_pixel(cx + x, cy + y, self.color)
