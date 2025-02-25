from models.item import Item


class Potion(Item):
    def __init__(self, stock):
        super().__init__("Poción", "Cura 20PS del pokemon activo", stock)

    def use(self, objective):
        if self.stock > 0:
            heal_points = min(objective.max_life - objective.life, 20)
            objective.heal(heal_points)
            self.stock -= 1
            return [f"{objective.name} ha recuperado {heal_points}PS"]
        return [f"{objective.name} ha intentado beber una pocion, pero ya no le quedan"]