from mazegenerator import MazeGenerator
from utils import Utils


class Maze:
    def __init__(self):
        self.north = 1
        self.south = 4
        self.east = 2
        self.west = 8
        self.wall_thick = 2
        self.cells = []
        self.entry = ()
        self.exit = ()
        self.utils = Utils()

    def load_maze(self, width: int, height: int, seed: int) -> MazeGenerator:
        if not width:
            width = 720
        if not height:
            height = 720
        if not seed:
            seed = 42
        return MazeGenerator(
            size=(width, height),
            perfect=False,
            entry_cell=(0, 0),
            exit_cell=(-1, -1),
            seed=seed,
        )

    def compute_cell_size(
        self, maze_w: int, maze_h: int,
        screen_w: int, screen_h: int,
        margin: int = 0,
    ) -> tuple[int, int]:
        return (
            max(1, (screen_w - 2 * margin) // maze_w),
            max(1, (screen_h - 2 * margin) // maze_h),
        )

    def compute_offsets(
        self, maze_w: int, maze_h: int,
        cell_w: int, cell_h: int,
        screen_w: int, screen_h: int,
    ) -> tuple[int, int]:
        ox = (screen_w - maze_w * cell_w) // 2
        oy = (screen_h - maze_h * cell_h) // 2
        return ox, oy

    def draw_maze(
        self,
        maze: MazeGenerator,
        cell_w: int, cell_h: int,
        offset_x: int, offset_y: int,
        thick: int,
        color,
    ) -> None:
        thick = max(1, min(thick, cell_w, cell_h))

        grid = maze.maze
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        for y in range(rows):
            for x in range(cols):
                m = grid[y][x]

                x0 = offset_x + x * cell_w
                y0 = offset_y + y * cell_h

                if m & self.north:
                    if y == 0 or not (grid[y - 1][x] & self.south):
                        self.utils.thick_hline(x0, y0, cell_w, thick, color)

                if m & self.west:
                    if x == 0 or not (grid[y][x - 1] & self.east):
                        self.utils.thick_vline(x0, y0, cell_h, thick, color)

                if m & self.south:
                    self.utils.thick_hline(
                        x0, y0 + cell_h - thick,
                        cell_w, thick, color,
                    )

                if m & self.east:
                    self.utils.thick_vline(
                        x0 + cell_w - thick, y0,
                        cell_h, thick, color,
                    )
