from menus.drawableMenu import DrawableMenu
from utils.constants import SCREEN_SETTINGS, COLORS
from pygame import draw

class AttacksMenu(DrawableMenu):
    origin = (0, SCREEN_SETTINGS.HEIGHT - 150)
    offset = (25, 25)

    def draw(screen):
        draw.rect(screen, COLORS.WHITE,
                  (AttacksMenu.origin[0], AttacksMenu.origin[1], SCREEN_SETTINGS.WIDTH, 150))
        draw.rect(screen, COLORS.BLACK,
                  (AttacksMenu.origin[0], AttacksMenu.origin[1], SCREEN_SETTINGS.WIDTH, 150), 5)  # Borde de 5 píxeles
