from pygame import image, transform

from utils.constants import POKEMON_TYPES, SCREEN_SETTINGS


class Pokemon:

    def __init__(self, name, id, type, shout, attacks, life, speed):
        self.life = life
        self.max_life = life
        self.shout = shout
        self.type = type
        self.name = name
        self.id = id
        self.speed = speed
        self.image_path = f"assets/{self.name}"
        self.back_image = image.load(self.image_path + '-back.png')
        self.back_image = transform.scale(self.back_image, (300, 400))

        self.front_image = image.load(self.image_path + '-front.png')
        self.front_image = transform.scale(self.front_image, (300, 400))

        self.frames_to_tick = 0
        self.times_to_tick = 0
        self.candraw = True

        self.attacks = attacks

    def takeDamage(self, attack):
        multiplier = 1.25 if self.isWeak(attack.type, self.type) else 1
        multiplier = 0.30 if self.isStrong(attack.type, self.type) else multiplier
        self.life -= int(attack.damage * multiplier)
        response = [f"{self.name} ha perdido {int(attack.damage * multiplier)}PS"]

        if multiplier > 1:
            response.append("Es muy eficaz")
        if multiplier < 1:
            response.append("No es eficaz")

        if (self.life <= 0):
            response.append(f"{self.name} se ha debilitado.")

        self.times_to_tick = 10
        return response

    def isWeak(self, origin, objective):
        return origin in POKEMON_TYPES.WEAKNESS[objective - 1]

    def isStrong(self, origin, objective):
        return origin in POKEMON_TYPES.STRENGTHS[objective - 1]

    def isDead(self):
        return self.life <= 0

    def heal(self, amount):
        self.life += amount

    def draw(self, screen, x, y, enemy = False):
        if (self.frames_to_tick >= 0.15 * SCREEN_SETTINGS.FPS and self.times_to_tick > 0):
            self.times_to_tick -= 1
            self.frames_to_tick = 0
            self.candraw = not self.candraw

        if (self.times_to_tick <= 0):
            self.candraw = True

        if (self.candraw):
            screen.blit(self.front_image if enemy else self.back_image, (x, y))

        self.frames_to_tick += 1