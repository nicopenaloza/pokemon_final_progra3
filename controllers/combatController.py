from random import choice

from controllers.dialogController import DialogController
from controllers.eventController import EventController
from models.message import Message
from models.movement import Movement
from models.player import Player
from utils.constants import EVENTS


class CombatController:

    def __init__(self, enemy=Player(), player=Player(), dialogController=DialogController(), menu=None,
                 eventController=EventController()):
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

            if self.player.hasMorePokemons():
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
                    message = Message(text)

                    if move.type == Movement.ATTACK:
                        text = move.origin.name + " ha usado " + move.name
                        if move.origin == self.enemy.selected_pokemon:
                            move.objective = self.player
                        if move.origin == self.player.selected_pokemon:
                            move.objective = self.enemy

                        message.origin = move.origin

                    if move.type == Movement.ITEM_USED:
                        text = f"{move.origin.name} ha bebido una poción"

                    if move.type == Movement.POKEMON_CHANGED:
                        pokemon = self.enemy.pokemons[move.objective] if move.origin == self.enemy else \
                            self.player.pokemons[move.objective]
                        text = f"{move.origin.name} ha sido cambiado por {pokemon.name}"

                    if not move.origin.isDead():
                        message.text = text
                        message.callback = move.run
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

    def __expected_damage(self, attack, defender):
        multiplier = 1.25 if defender.isWeak(attack.type, defender.type) else 1
        multiplier = 0.30 if defender.isStrong(attack.type, defender.type) else multiplier
        return int(attack.damage * multiplier)

    def __minimax(self, enemy_pokemon, enemy_life, player_pokemon, player_life, depth, maximizing):
        if depth == 0 or enemy_life <= 0 or player_life <= 0:
            return enemy_life - player_life

        if maximizing:
            best_value = -float('inf')
            # Movimientos de ataque del enemigo.
            for attack in enemy_pokemon.attacks:
                if attack.pp <= 0:
                    continue
                damage = self.__expected_damage(attack, player_pokemon)
                new_player_life = max(0, player_life - damage)
                value = self.__minimax(enemy_pokemon, enemy_life, player_pokemon, new_player_life, depth - 1, False)
                best_value = max(best_value, value)

            for candidate in self.enemy.pokemons:
                if candidate == enemy_pokemon or candidate.isDead():
                    continue
                new_enemy_life = candidate.life
                value = self.__minimax(candidate, new_enemy_life, player_pokemon, player_life, depth - 1, False)
                best_value = max(best_value, value)

            if hasattr(self.enemy, "items"):
                for item in self.enemy.items:
                    if item.stock > 0 and enemy_life < enemy_pokemon.max_life:
                        heal_amount = min(enemy_pokemon.max_life - enemy_life, 20)
                        new_enemy_life = enemy_life + heal_amount
                        value = self.__minimax(enemy_pokemon, new_enemy_life, player_pokemon, player_life, depth - 1,
                                               False)
                        best_value = max(best_value, value)
            return best_value

        else:
            best_value = float('inf')

            for attack in player_pokemon.attacks:
                if attack.pp <= 0:
                    continue
                damage = self.__expected_damage(attack, enemy_pokemon)
                new_enemy_life = max(0, enemy_life - damage)
                value = self.__minimax(enemy_pokemon, new_enemy_life, player_pokemon, player_life, depth - 1, True)
                best_value = min(best_value, value)

            for candidate in self.player.pokemons:
                if candidate == player_pokemon or candidate.isDead():
                    continue
                new_player_life = candidate.life
                value = self.__minimax(enemy_pokemon, enemy_life, candidate, new_player_life, depth - 1, True)
                best_value = min(best_value, value)

            if hasattr(self.player, "items"):
                for item in self.player.items:
                    if item.stock > 0 and player_life < player_pokemon.max_life:
                        heal_amount = min(player_pokemon.max_life - player_life, 20)
                        new_player_life = player_life + heal_amount
                        value = self.__minimax(enemy_pokemon, enemy_life, player_pokemon, new_player_life, depth - 1,
                                               True)
                        best_value = min(best_value, value)
            return best_value

    def selectEnemyMovement(self):
        enemy_pokemon = self.enemy.selected_pokemon
        player_pokemon = self.player.selected_pokemon
        current_enemy_life = enemy_pokemon.life
        current_player_life = player_pokemon.life
        search_depth = 3

        best_value = -float('inf')
        best_move = None

        for attack in enemy_pokemon.attacks:
            if attack.pp <= 0:
                continue
            damage = self.__expected_damage(attack, player_pokemon)
            new_player_life = max(0, current_player_life - damage)
            value = self.__minimax(enemy_pokemon, current_enemy_life, player_pokemon, new_player_life, search_depth - 1,
                                   False)
            if value > best_value:
                best_value = value
                best_move = ("attack", attack)

        for candidate in self.enemy.pokemons:
            if candidate == enemy_pokemon or candidate.isDead():
                continue
            new_enemy_life = candidate.life
            value = self.__minimax(candidate, new_enemy_life, player_pokemon, current_player_life, search_depth - 1,
                                   False)
            if value > best_value:
                best_value = value
                best_move = ("switch", candidate)

        if hasattr(self.enemy, "items"):
            for item in self.enemy.items:
                if item.stock > 0 and current_enemy_life < enemy_pokemon.max_life:
                    heal_amount = min(enemy_pokemon.max_life - current_enemy_life, 20)
                    new_enemy_life = current_enemy_life + heal_amount
                    value = self.__minimax(enemy_pokemon, new_enemy_life, player_pokemon, current_player_life,
                                           search_depth - 1, False)
                    if value > best_value:
                        best_value = value
                        best_move = ("potion", item)

        if best_move is None:
            best_attack = choice(enemy_pokemon.attacks)
            best_move = ("attack", best_attack)

        if best_move[0] == "attack":
            chosen_attack = best_move[1]
            self.turn_movements.append(
                Movement(Movement.ATTACK, chosen_attack.attack, chosen_attack.priority, enemy_pokemon,
                         player_pokemon, chosen_attack.name)
            )

        elif best_move[0] == "switch":
            candidate = best_move[1]
            index = self.enemy.pokemons.index(candidate)
            self.turn_movements.append(
                Movement(Movement.POKEMON_CHANGED, self.enemy.selectPokemon, 1000, enemy_pokemon, index)
            )

        elif best_move[0] == "potion":
            potion_item = best_move[1]
            self.turn_movements.append(
                Movement(Movement.ITEM_USED, potion_item.use, 1000, enemy_pokemon, enemy_pokemon)
            )
