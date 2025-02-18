from random import choice

from controllers.dialogController import DialogController
from models.message import Message
from models.player import Player


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
            self.callback()
        else:
            self.callback(self.objective)


class CombatController:

    def __init__(self, enemy=Player(), player=Player(), dialogController=DialogController(), menu=None):
        self.enemy = enemy
        self.player = player
        self.dialogController = dialogController
        self.menu = menu
        self.turn_movements = []

    def validateState(self):
        if self.player.selected_pokemon and self.player.selected_pokemon.isDead() and self.player.hasMorePokemons():
            self.dialogController.addMessage(Message(self.player.selected_pokemon.name + " se ha debilitado..."))
            self.player.nextPokemon()
            self.menu.showPokemonMenu()

        if self.enemy.selected_pokemon and self.enemy.selected_pokemon.isDead() and self.enemy.hasMorePokemons():
            self.dialogController.addMessage(Message(self.enemy.selected_pokemon.name + " se ha debilitado..."))
            self.enemy.nextPokemon()

    def runMovements(self):
        if len(self.turn_movements) > 1:
            if (self.enemy.selected_pokemon.speed > self.player.selected_pokemon.speed):
                self.turn_movements.reverse()
            self.turn_movements.sort(key=lambda x: x.priority, reverse=True)

            for move in self.turn_movements:
                if self.__canMove(move):
                    text = ""
                    if move.type == Movement.ATTACK:
                        text = move.origin.name + " ha usado " + move.name
                        if move.origin == self.enemy.selected_pokemon:
                            move.objective = self.player.selected_pokemon
                        if move.origin == self.player.selected_pokemon:
                            move.objective = self.enemy.selected_pokemon

                    if move.type == Movement.POKEMON_CHANGED:
                        pokemon = self.enemy.selected_pokemon if move.origin == self.enemy else self.player.selected_pokemon
                        newPokemon = self.enemy.pokemons[move.objective] if move.origin == self.enemy else \
                            self.player.pokemons[move.objective]
                        text = pokemon.name + " ha sido cambiado por " + newPokemon.name

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
