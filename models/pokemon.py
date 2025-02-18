from utils.constants import POKEMON_TYPES


class Pokemon:

    def __init__(self, name, id, type, shout, attacks, life):
        self.life = life - 25
        self.max_life = life
        self.shout = shout
        self.type = type
        self.name = name
        self.id = id

        self.attacks = attacks

    def takeDamage(self, attack):
        multiplier = 1.25 if self.isWeak(attack.type, self.type) else 1
        multiplier = 0.75 if self.isStrong(attack.type, self.type) else multiplier
        self.life -= attack.damage * multiplier

    def isWeak(self, origin, objective):
        return origin in POKEMON_TYPES.WEAKNESS[objective - 1]

    def isStrong(self, origin, objective):
        return origin in POKEMON_TYPES.STRENGTHS[objective - 1]

    def isDead(self):
        return self.life <= 0