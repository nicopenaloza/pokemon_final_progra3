from models.drawableEntity import DrawableEntity
from models.pokemon import Pokemon


class Player(DrawableEntity):

    def __init__(self):
        super().__init__(0, 1, size=40, media_path='')

        self.items = []
        self.pokemons = []
        self.selected_pokemon = None

    def select_pokemon(self, i):
        self.selected_pokemon = self.pokemons[i]

    def addPokemon(self, pokemon):
        self.pokemons.append(pokemon)

    def addPokemons(self, pokemons):
        for p in pokemons:
            self.pokemons.append(p)

    def hasMorePokemons(self):
        response = False
        i = 0
        while i < len(self.pokemons) and not response:
            if not self.pokemons[i].isDead():
                response = True
            i += 1
        return response

    def __nextPokemonId(self):
        i = -1
        flag = False
        while i < len(self.pokemons) and not flag:
            i += 1
            if not self.pokemons[i].isDead():
                flag = True

        return i

    def nextPokemon(self):
        nextPokemonId = self.__nextPokemonId()
        self.selected_pokemon = self.pokemons[nextPokemonId]