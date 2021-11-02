class Simulation:

    def __init__(self):
        animal1 = Animal("pig", [2,3])
        print("Map!")
        map1 = Map(4,5)
        map1.printAll()

    def simulationLoop(self):
#move animals

#update map with animal locations

class Animal:

    def __init__(self, name, loc=[0,0]):
        self.name = name
        self.health = 100
        self.speed = 1
        self.hunger = 10 #starts at 10 which means full
        self.loc = loc
        self.marker = 'p'


    def move (self, direction):
        #function body TO DO
        if direction == "up":
            self.loc[1] += 1
        elif direction == "right":
            self.loc[0] += 1
        elif direction == "left":
            self.loc[0] -= 1
        elif direction == "down":
            self.loc[1] -= 1



    def health (self):
        #function body TO DO
        pass

class Map:

    def __init__(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.grid = [[(0,'e') for col in range(numCols)] for row in range(numRows)]
        for row in self.grid:
            print(row)
    def printTiles(self):
        for row in self.grid:
            print(row[0])
    def printAnimals(self):
        for row in self.grid:
            print(row[1])
    def printAll(self):
        for row in self.grid:
            print(row)


class Tile:

    def __init__(self):
        pass

sim1 = Simulation()
