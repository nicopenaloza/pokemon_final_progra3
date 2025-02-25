class Movement:
    ITEM_USED = 0
    POKEMON_CHANGED = 1
    ATTACK = 2

    def __init__(self, type, callback, priority=100, origin=None, objective=None, name=""):
        self.type = type
        self.callback = callback
        self.priority = priority
        self.objective = objective
        self.origin = origin
        self.name = name

    def run(self):
        if (self.objective == None and self.type != Movement.ATTACK):
            return self.callback()
        else:
            if (self.type == Movement.ATTACK):
                return self.callback(self.objective.selected_pokemon)
            return self.callback(self.objective)
