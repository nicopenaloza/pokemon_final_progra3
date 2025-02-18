from random import choice

from models.player import Player


class Movement:
    ITEM_USED = 0
    POKEMON_CHANGED = 1
    ATTACK = 2

    def __init__(self, type, callback, priority=100, objective=None):
        self.type = type
        self.callback = callback
        self.priority = priority
        self.objective = objective

    def run(self):
        if (self.objective == None and self.type != Movement.ATTACK):
            self.callback()
        else:
            self.callback(self.objective)


class CombatController:

    def __init__(self, enemy=Player(), player=Player()):
        self.enemy = enemy
        self.player = player
        self.turn_movements = []

    def validateState(self):
        if self.player.selected_pokemon.isDead() and self.player.hasMorePokemons():
            self.player.nextPokemon()

        if self.enemy.selected_pokemon.isDead() and self.enemy.hasMorePokemons():
            self.enemy.nextPokemon()

    def runMovements(self):
        if len(self.turn_movements) > 1:
            self.turn_movements.sort(key=lambda x: x.priority, reverse=True)
            for move in self.turn_movements:
                if self.__canMove(move):
                    move.run()

            self.turn_movements = []

        self.turn_movements = []

    def __canMove(self, move):
        return (move.type == Movement.ATTACK and (
                    move.objective == self.player.selected_pokemon and not self.enemy.selected_pokemon.isDead() or (
                        move.objective == self.enemy.selected_pokemon and not self.player.selected_pokemon.isDead()))) or move.type != Movement.ATTACK

    def addMovement(self, movement):
        if movement.type == Movement.ITEM_USED:
            movement.objective = self.player.selected_pokemon
        if movement.type == Movement.ATTACK:
            movement.objective = self.enemy.selected_pokemon

        self.turn_movements.append(movement)
        self.selectEnemyMovement()

    def selectEnemyMovement(self):
        movement = choice(self.enemy.selected_pokemon.attacks)
        self.turn_movements.append(
            Movement(Movement.ATTACK, movement.attack, movement.priority, self.player.selected_pokemon))
