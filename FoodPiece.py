class FoodPiece:
    def __init__(self, i, j, type=None):
        self.i = i
        self.j = j
        self.type = None
        self.type = "Energizer" if type else "Normal"
