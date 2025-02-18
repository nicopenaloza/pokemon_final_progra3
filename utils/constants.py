from pygame import QUIT, KEYDOWN, KEYUP, K_LEFT, K_UP, K_DOWN, K_RIGHT, K_RETURN, K_BACKSPACE, font


class COLORS:
    BACKGROUND = (230, 230, 230)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


class SCREEN_SETTINGS:
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    CAPTION = "Pokémon - Grupo 8"

class MENU_TYPE:
    ATTACKS = 0
    POKEMONS = 1
    BACKPACK = 2
    DEFAULT = 3
    DIALOG = 4

class EVENTS:
    QUIT = QUIT
    MENU_CONTROLLER = "menu_event"
    KEYDOWN = KEYDOWN
    KEYUP = KEYUP
    KEY_UP = K_UP
    KEY_DOWN = K_DOWN
    KEY_LEFT = K_LEFT
    KEY_RIGHT = K_RIGHT
    ENTER = K_RETURN
    BACK = K_BACKSPACE
    MOVEMENT = "movement"

class POKEMON_TYPES:
    FIRE = 1
    PLANT = 2
    WATER = 3
    ELECTRIC = 4
    ROCK = 5
    NORMAL = 6

    WEAKNESS = [[WATER, ROCK], [FIRE, ROCK], [PLANT, ELECTRIC], [ROCK], [WATER], []]
    STRENGTHS = [[PLANT, FIRE], [WATER, PLANT], [WATER, FIRE, ROCK], [ELECTRIC], [ROCK, WATER], [NORMAL]]
    TRANSLATIONS = ["", "Fuego", "Planta", "Agua", "Electrico", "Roca", "Normal"]

class MOVEMENT_ORIGIN:
    player = 0
    enemy = 1