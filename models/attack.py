import random


class Attack:
    def __init__(self, damage, type, name, pp, precision, priority):
        self.damage = damage
        self.type = type
        self.name = name
        self.pp = pp
        self.precision = precision
        self.priority = priority

    def attack(self, pokemon):
        if not pokemon:
            return
        response = []
        if self.pp > 0:
            if random.randrange(100) <= self.precision:
                response = pokemon.takeDamage(self)

            self.pp -= 1
        print(response, "x")
        return response