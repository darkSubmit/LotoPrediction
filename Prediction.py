class Prediction:
    
    nbChance: int

    tirage =  [0] * 5
    
    # parameterized constructor
    def __init__(self, nbChance, tirage):
        self.nbChance = nbChance
        self.tirage = tirage

    def stringifyPrediction(self):
        return str(self.tirage[0]) + " " + str(self.tirage[1]) + " " +  str(self.tirage[2]) + " " + str(self.tirage[3]) + " " + str(self.tirage[4]) + "  " + str(self.nbChance)