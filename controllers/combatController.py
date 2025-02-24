from random import choice

from controllers.dialogController import DialogController
from controllers.eventController import EventController
from models.message import Message
from models.player import Player
from utils.constants import EVENTS


class Movement:
    ITEM_USED = 0
    POKEMON_CHANGED = 1
    ATTACK = 2

    def __init__(self, type, callback, priority=100, origin=None, objective=None, name=""):
        self.type = type
        self.callback = callback
        self.priority = priority
        self.objective = objective
        self.origin = origin
        self.name = name

    def run(self):
        if (self.objective == None and self.type != Movement.ATTACK):
            return self.callback()
        else:
            return self.callback(self.objective)


class CombatController:

    def __init__(self, enemy=Player(), player=Player(), dialogController=DialogController(), menu=None, eventController = EventController()):
        self.enemy = enemy
        self.player = player
        self.dialogController = dialogController
        self.eventController = eventController
        self.menu = menu
        self.turn_movements = []

    def validateState(self):
        if self.player.selected_pokemon and self.player.selected_pokemon.isDead() and self.player.hasMorePokemons():
            self.dialogController.clear()
            self.dialogController.addMessage(
                Message(f"{self.player.selected_pokemon.name} ha sido debilitado.")
            )

            if self.enemy.hasMorePokemons():
                self.player.nextPokemon()
            else:
                self.dialogController.addMessage(
                    Message("Mala suerte, perdiste... :(.")
                )
                self.eventController.emitEvent(EVENTS.LOSE)

            self.menu.showPokemonMenu()

        if self.enemy.selected_pokemon and self.enemy.selected_pokemon.isDead():
            self.dialogController.clear()
            if self.enemy.hasMorePokemons():
                self.dialogController.addMessage(
                    Message(f"{self.enemy.selected_pokemon.name} ha sido debilitado.", self.enemy.nextPokemon)
                )
            else:
                self.dialogController.addMessage(
                    Message(f"{self.enemy.selected_pokemon.name} ha sido debilitado.")
                )
                self.dialogController.addMessage(
                    Message("Felicidades ¡Ganaste el juego!")
                )
                self.eventController.emitEvent(EVENTS.WIN)

    def runMovements(self):
        if len(self.turn_movements) > 1:
            self.turn_movements.sort(
                key=lambda x: (x.priority, x.origin.speed if x.origin else 0),
                reverse=True
            )

            for move in self.turn_movements:
                if self.__canMove(move):
                    text = ""
                    if move.type == Movement.ATTACK:
                        text = move.origin.name + " ha usado " + move.name
                        if move.origin == self.enemy.selected_pokemon:
                            move.objective = self.player.selected_pokemon
                        if move.origin == self.player.selected_pokemon:
                            move.objective = self.enemy.selected_pokemon

                    if move.type == Movement.ITEM_USED:
                        text = f"{move.origin.name} ha bebido una pocion"

                    if move.type == Movement.POKEMON_CHANGED:
                        pokemon = self.enemy.pokemons[move.objective] if move.origin == self.enemy else \
                            self.player.pokemons[move.objective]
                        text = f"{move.origin.name} ha sido cambiado por {pokemon.name}"

                    if not move.origin.isDead():
                        self.dialogController.addMessage(Message(text, move.run))

            self.turn_movements = []

        self.turn_movements = []

    def __canMove(self, move):
        return (move.type == Movement.ATTACK and (
                move.objective == self.player.selected_pokemon and not self.enemy.selected_pokemon.isDead() or (
                move.objective == self.enemy.selected_pokemon and not self.player.selected_pokemon.isDead()))) or move.type != Movement.ATTACK

    def addMovement(self, movement):
        movement.origin = self.player.selected_pokemon

        if movement.type == Movement.ITEM_USED:
            movement.objective = self.player.selected_pokemon
        if movement.type == Movement.ATTACK:
            movement.objective = self.enemy.selected_pokemon

        self.turn_movements.append(movement)
        self.selectEnemyMovement()

    def selectEnemyMovement(self):
        movement = choice(self.enemy.selected_pokemon.attacks)
        print(movement)
        self.turn_movements.append(
            Movement(Movement.ATTACK, movement.attack, movement.priority, self.enemy.selected_pokemon,
                     self.player.selected_pokemon, movement.name))
