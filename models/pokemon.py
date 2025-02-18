from utils.constants import POKEMON_TYPES


class Pokemon:

    def __init__(self, name, id, type, shout, attacks, life, speed):
        self.life = life
        self.max_life = life
        self.shout = shout
        self.type = type
        self.name = name
        self.id = id
        self.speed = speed

        self.attacks = attacks

    def takeDamage(self, attack):
        multiplier = 1.25 if self.isWeak(attack.type, self.type) else 1
        multiplier = 0.30 if self.isStrong(attack.type, self.type) else multiplier
        self.life -= attack.damage * multiplier
        response = [f"{self.name} ha perdido {attack.damage * multiplier}PS"]
        if multiplier > 1:
            response.append("Es muy eficaz")
        if multiplier < 1:
            response.append("No es eficaz")

    def isWeak(self, origin, objective):
        return origin in POKEMON_TYPES.WEAKNESS[objective - 1]

    def isStrong(self, origin, objective):
        return origin in POKEMON_TYPES.STRENGTHS[objective - 1]

    def isDead(self):
        return self.life <= 0
