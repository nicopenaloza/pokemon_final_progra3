from pygame import draw

from menus.drawableMenu import DrawableMenu
from utils.constants import COLORS, SCREEN_SETTINGS


class DefaultMenu(DrawableMenu):
    origin = (0, SCREEN_SETTINGS.HEIGHT - 150)
    offset = (SCREEN_SETTINGS.WIDTH - 300, 40)

    def draw(screen):
        draw.rect(screen, COLORS.WHITE,
                  (DefaultMenu.origin[0], DefaultMenu.origin[1], SCREEN_SETTINGS.WIDTH, 150))
        draw.rect(screen, COLORS.BLACK,
                  (DefaultMenu.origin[0], DefaultMenu.origin[1], SCREEN_SETTINGS.WIDTH, 150), 5)  # Borde de 5 píxeles
