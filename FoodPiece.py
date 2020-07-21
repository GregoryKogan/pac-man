class FoodPiece:
    def __init__(self, i, j, type=None):
        self.i = i
        self.j = j
        self.type = None
        if type:
            self.type = "Energizer"
        else:
            self.type = "Normal"
