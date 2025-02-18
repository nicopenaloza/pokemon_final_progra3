from pygame import draw, font

from menus.drawableMenu import DrawableMenu
from utils.constants import SCREEN_SETTINGS, COLORS

class DialogMenu(DrawableMenu):
    origin = (0, SCREEN_SETTINGS.HEIGHT - 150)
    offset = (SCREEN_SETTINGS.WIDTH - 300, 40)

    def draw(screen):
        draw.rect(screen, COLORS.WHITE,
                  (DialogMenu.origin[0], DialogMenu.origin[1], SCREEN_SETTINGS.WIDTH, 150))
        draw.rect(screen, COLORS.BLACK,
                  (DialogMenu.origin[0], DialogMenu.origin[1], SCREEN_SETTINGS.WIDTH, 150), 5)  # Borde de 5 píxeles

    def drawText(screen, message, tick):
        title = font.Font("assets/pokemon_fire_red.ttf", 30)
        message = title.render(message[:tick], True, COLORS.BLACK)
        screen.blit(message, (DialogMenu.origin[0] + 25, DialogMenu.origin[1] + 60))
