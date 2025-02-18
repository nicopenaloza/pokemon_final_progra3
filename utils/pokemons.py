from models.pokemon import Pokemon
from utils.attacks import Ascuas, Placaje, PistolaAgua, Impactrueno, AtaqueRapido
from utils.constants import POKEMON_TYPES

Squirtle = Pokemon("Squirtle", 1, POKEMON_TYPES.WATER, "squirtle", [
    PistolaAgua, Ascuas
], 100, 30)

Charmander = Pokemon("Charmander", 1, POKEMON_TYPES.FIRE, "char", [
    Placaje, Ascuas
], 100, 30)

Pikachu = Pokemon("Pikachu", 1, POKEMON_TYPES.ELECTRIC, "Pika", [
    Placaje, Impactrueno, AtaqueRapido
], 100, 10)
