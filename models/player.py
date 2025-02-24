from copy import copy

from models.drawableEntity import DrawableEntity
from models.potion import Potion
from utils.pokemons import Pikachu


class Player(DrawableEntity):

    def __init__(self):
        super().__init__(0, 1, size=40, media_path='')

        self.items = [Potion(3)]
        self.pokemons = []
        self.selected_pokemon = copy(Pikachu)

    def selectPokemon(self, i):
        self.selected_pokemon = self.pokemons[i]

    def addPokemon(self, pokemon):
        self.pokemons.append(copy(pokemon))

    def addPokemons(self, pokemons):
        for p in pokemons:
            self.pokemons.append(copy(p))

    def hasMorePokemons(self):
        response = False
        i = 0
        while i < len(self.pokemons) and not response:
            if not self.pokemons[i].isDead():
                response = True
            i += 1
        return response

    def nextPokemonId(self):
        i = -1
        flag = False
        while i < len(self.pokemons) and not flag:
            i += 1
            if not self.pokemons[i].isDead():
                flag = True

        return i

    def nextPokemon(self):
        self.selected_pokemon = self.pokemons[self.nextPokemonId()]
        return [f"{self.selected_pokemon.name} ha entrado en la arena"]