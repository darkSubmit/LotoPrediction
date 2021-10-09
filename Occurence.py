class Occurence:
    
    number: int

    totalOccurence = 1
    
    # parameterized constructor
    def __init__(self, number):
        self.number = number

    def incrementOccurence(self):
        self.totalOccurence += 1