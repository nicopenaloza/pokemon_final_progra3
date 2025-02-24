from models.item import Item


class Potion(Item):
    def __init__(self, stock):
        super().__init__("Poción", "Cura 20PS del pokemon activo", stock)

    def use(self, objective):
        heal_points = min(objective.max_life - objective.life, 20)
        objective.heal(heal_points)
        return [f"{objective.name} ha recuperado {heal_points}PS"]