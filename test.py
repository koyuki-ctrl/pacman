import math
from pyray import *

def pixel_sector(cx, cy, radius, start_angle, end_angle, color):
    """Dessine un secteur de disque plein, pixel par pixel.
    Angles en degrés (0 = droite, sens horaire car l'axe Y de l'écran va vers le bas)."""
    start = start_angle % 360
    end = end_angle % 360
    r2 = radius * radius

    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            # 1. dans le disque ?
            if x * x + y * y > r2:
                continue

            # 2. angle du pixel, entre 0 et 360
            angle = math.degrees(math.atan2(y, x)) % 360

            # 3. dans le secteur ? (gère le cas où le secteur passe par 0°)
            if start <= end:
                inside = start <= angle <= end
            else:
                inside = angle >= start or angle <= end

            if inside:
                draw_pixel(int(cx + x), int(cy + y), color)


init_window(640, 480, "Pacman pixels")
set_target_fps(60)

t = 0.0
while not window_should_close():
    t += get_frame_time()
    mouth = 5 + 40 * abs(math.sin(t * 8))   # demi-ouverture de la bouche

    begin_drawing()
    clear_background(BLACK)
    # le secteur va de "mouth" à "360 - mouth" : la bouche est le trou à droite
    pixel_sector(320, 240, 50, mouth, 360 - mouth, YELLOW)
    end_drawing()

close_window()