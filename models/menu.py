from pygame import draw, font

from controllers.combatController import Movement
from controllers.dialogController import DialogController
from controllers.eventController import EventController
from menus.attacksMenu import AttacksMenu
from menus.defaultMenu import DefaultMenu
from menus.dialogMenu import DialogMenu
from menus.pokemonMenu import PokemonMenu
from models.player import Player
from utils.constants import EVENTS, COLORS, SCREEN_SETTINGS, MENU_TYPE, POKEMON_TYPES


class Option:
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback

    def select(self):
        self.callback()

    def run(self, payload):
        self.callback(payload)


class Menu:
    def __init__(self, player=Player(), event_controller=EventController(), dialog_controller=DialogController()):
        self.player = player
        self.dialog_controller = dialog_controller
        self.event_controller = event_controller
        self.cursor_position = (0, 0)
        self.default_options = [
            [
                Option("Atacar", self.__showAttacksMenu),
                Option("Mochila", self.__showBackpackMenu),
            ],
            [
                Option("Pokemon", self.showPokemonMenu),
                Option("Salir", self.event_controller.close),
            ],
        ]

        self.current_options = self.default_options
        self.menu_type = MENU_TYPE.DEFAULT
        self.tick = 0
        self.font = font.Font(None, 30)


    def init(self):
        self.event_controller.subscribe((EVENTS.MENU_CONTROLLER, self.onInput))

    def __move_cursor(self, direction):
        xpos, ypos = self.cursor_position[0] + direction[0], self.cursor_position[1] + direction[1]
        self.cursor_position = (self.cursor_position[0] if xpos >= len(self.current_options[0]) else xpos,
                                self.cursor_position[1] if ypos >= len(self.current_options) else ypos)

    def onInput(self, event):
        if (event.key == EVENTS.KEY_UP and self.cursor_position[1] > 0):
            self.__move_cursor((0, -1))
        if (event.key == EVENTS.KEY_DOWN and self.cursor_position[1] < len(self.current_options)):
            self.__move_cursor((0, 1))
            if self.cursor_position[0] >= len(self.current_options[1]):
                self.__move_cursor((-1, 0))
        if (event.key == EVENTS.KEY_LEFT and self.cursor_position[0] > 0):
            self.__move_cursor((-1, 0))
        if (event.key == EVENTS.KEY_RIGHT and self.cursor_position[0] + 1 < len(
                self.current_options[self.cursor_position[1]])):
            self.__move_cursor((1, 0))

        if (event.key == EVENTS.ENTER):
            self.current_options[self.cursor_position[1]][self.cursor_position[0]].select()

        if (event.key == EVENTS.BACK):
            self.__defaultMenu()

    def draw(self, screen):
        menu = self.__get_menu()

        menu.draw(screen)

        y_offset = menu.offset[1]

        is_default = self.menu_type == MENU_TYPE.DEFAULT

        if (self.menu_type != MENU_TYPE.DIALOG):
            for row_index, row in enumerate(self.current_options):
                x_offset = menu.offset[0]

                for col_index, option in enumerate(row):
                    color_texto = COLORS.BLACK
                    texto = self.font.render(option.name, True, color_texto)
                    extra_offset = 0

                    if (col_index, row_index) == self.cursor_position:
                        triangle_points = [
                            (menu.origin[0] + x_offset + 5, menu.origin[1] + y_offset + 8),  # Punta izquierda
                            (menu.origin[0] + x_offset - 5, menu.origin[1] + y_offset + 4),  # Arriba
                            (menu.origin[0] + x_offset - 5, menu.origin[1] + y_offset + 13)  # Abajo
                        ]
                        draw.polygon(screen, COLORS.BLACK, triangle_points)
                        extra_offset = 10

                    screen.blit(texto, (menu.origin[0] + x_offset + extra_offset, menu.origin[1] + y_offset))

                    x_offset += 150 if is_default else 250

                y_offset += 50
        else:
            DialogMenu.drawText(screen, self.dialog_controller.first().text, int(self.tick * 2))

        if self.menu_type == MENU_TYPE.ATTACKS:
            draw.rect(screen, COLORS.BLACK,
                      (SCREEN_SETTINGS.WIDTH - 300, SCREEN_SETTINGS.HEIGHT - 150, 300, 150), 5)
            attack_index = self.cursor_position[1] + self.cursor_position[0]
            attack = self.player.selected_pokemon.attacks[attack_index]
            pps = "PP: " + str(attack.pp)
            type = "TIPO: " + POKEMON_TYPES.TRANSLATIONS[attack.type]
            texto = self.font.render(pps, True, COLORS.BLACK)
            texto2 = self.font.render(type, True, COLORS.BLACK)
            screen.blit(texto, (SCREEN_SETTINGS.WIDTH - 300 + 25, SCREEN_SETTINGS.HEIGHT - 150 + 25))
            screen.blit(texto2, (SCREEN_SETTINGS.WIDTH - 300 + 25, SCREEN_SETTINGS.HEIGHT - 150 + 50))

        self.tick += SCREEN_SETTINGS.FPS / 1000

    def __get_menu(self):
        if self.dialog_controller.hasMessages() and self.menu_type != MENU_TYPE.DIALOG:
            self.__showMessage()

        if self.menu_type == MENU_TYPE.DIALOG:
            return DialogMenu
        if self.menu_type == MENU_TYPE.ATTACKS:
            return AttacksMenu
        if self.menu_type == MENU_TYPE.POKEMONS:
            return PokemonMenu
        return DefaultMenu

    def __defaultMenu(self):
        self.menu_type = MENU_TYPE.DEFAULT
        self.cursor_position = (0, 0)
        self.current_options = self.default_options

    def __showBackpackMenu(self):
        self.menu_type = MENU_TYPE.BACKPACK
        for item in self.player.items:
            print(item.name)

    def __selectPokemon(self):
        pokemon = self.cursor_position[1] + self.cursor_position[0]
        if pokemon >= 0:
            self.event_controller.emitEvent(
                EVENTS.MOVEMENT,
                Movement(
                    type=Movement.POKEMON_CHANGED,
                    callback=self.player.selectPokemon,
                    priority=1000,
                    objective=pokemon
                )
            )

            self.__defaultMenu()

    def showPokemonMenu(self):
        self.current_options = []
        self.cursor_position = (0, 0)
        self.menu_type = MENU_TYPE.POKEMONS
        for i in range(len(self.player.pokemons)):
            self.current_options.append([Option(self.player.pokemons[i].name, self.__selectPokemon)])

    def __selectAttack(self):
        columna, fila = self.cursor_position
        ataque = self.current_options[fila][columna].name
        selected_attack = next((atk for atk in self.player.selected_pokemon.attacks if atk.name == ataque), None)
        if selected_attack:
            self.event_controller.emitEvent(
                EVENTS.MOVEMENT,
                Movement(
                    Movement.ATTACK,
                    selected_attack.attack,
                    selected_attack.priority,
                    self.player.selected_pokemon,
                    None,
                    selected_attack.name
                )
            )

        self.__defaultMenu()

    def __showAttacksMenu(self):
        self.current_options = []
        self.cursor_position = (0, 0)
        self.menu_type = MENU_TYPE.ATTACKS

        attacks = self.player.selected_pokemon.attacks
        filas = []

        for i in range(0, len(attacks), 2):
            fila = [Option(attacks[j].name, self.__selectAttack) for j in range(i, min(i + 2, len(attacks)))]
            filas.append(fila)
        print(filas)
        self.current_options = filas

    def __nextMessage(self):
        self.dialog_controller.pop()
        self.__defaultMenu()

    def __showMessage(self):
        self.tick = 0
        self.menu_type = MENU_TYPE.DIALOG
        self.current_options = [[Option("Continuar", self.__nextMessage)]]
