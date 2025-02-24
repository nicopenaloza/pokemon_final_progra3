from menus.drawableMenu import DrawableMenu
from utils.constants import SCREEN_SETTINGS, COLORS
from pygame import draw, transform, image

imagen = image.load("assets/pokemon_bg.png")
background = transform.scale(imagen, (800, 600))

class BagMenu(DrawableMenu):
    origin = (0, 0)
    offset = (SCREEN_SETTINGS.WIDTH - 150, 25)
    has_item_renderer = True


    def draw(screen):
        screen.blit(background, (0, 0))

    def drawItem(self, screen, pokemon, ypos):
        draw.rect(screen, COLORS.WHITE,
                  (BagMenu.origin[0], BagMenu.origin[1], SCREEN_SETTINGS.WIDTH, SCREEN_SETTINGS.HEIGHT))
        draw.rect(screen, COLORS.BLACK,
                  (BagMenu.origin[0], BagMenu.origin[1], SCREEN_SETTINGS.WIDTH, SCREEN_SETTINGS.HEIGHT), 5)  # Borde de 5 píxeles
