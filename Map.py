from Tile import Tile
from Animal import Animal
import random
import math
from scipy.stats import bernoulli
import numpy as  np
from Animal import Animal
from Animal import Predator
from Animal import Prey
import copy

# different dictionaries for each variable and then
# we pass in a coordinate to determine what is there
# coordinates will list the characteristics of what
# is there

class Map:
    #called in Simulation
    def __init__(self, mapSize, startingTemp, rateOfTempChange, startingAnimalDistribution):
        self.mapSize = mapSize #tuple
        self.size_x = mapSize[0]
        self.size_y = mapSize[1]
        self.startTemp = startingTemp
        self.currTemp = startingTemp
        self.numAnimals = 0
        self.numPredators = 0
        self.numPrey = 0
        self.animal_id = 0
        self.map = [[Tile() for i in range(self.size_x)] for j in range(self.size_y)]

        self.IDtoAnimal = {}
        self.IDtoLoc = {} # dictionary from animal IDs to locations
        self.current_order = [] # list of animal ID's: specifies order of action
        self.current_index = 0
        self.next_order = []

        self.initialize_animals()

    def convertIDtoLoc(self, animal_id):
        return self.IDtoLoc[animal_id]

    def convertIDtoTile(self, animal_id):
        animal_loc = self.convertIDtoLoc(animal_id)
        return self.map[animal_loc[1]][animal_loc[0]]

    def convertIDtoAnimal(self, animal_id):
        return self.IDtoAnimal[animal_id]

    def locToTile(self,loc):
        return self.map[loc[1]][loc[0]]


    def print_my_map(self):
        for i in self.mapSize:
            print("\n")   #printing a new line?????
            for j in self.mapSize:
                if(self.map[i][j].is_food()):
                    print('F ')
                if(self.map[i][j].is_water()):
                    print('W ')
                if(self.map[i][j].is_pred()):
                    print('P ')
                if(self.map[i][j].is_prey()):
                    print('p ')
                else:
                    print('E ')


    # function that makes a sine function that we
    # can pass back to tile to make curvy rivers
    def river_maker(self, size_x):
        x = [0] * len(self.size_x)
        y = [0] * len(self.size_x)
        coef = [0] * 4
        for i in range(4):
            coef[i] = random.random()
        for i in range(x):
            y[i] = 1/coef[0] * math.sin(coef[1] * x[i] + coef[2]) + coef[3]
            self.map[x[i]][y[i]].set_water()
        return

    def generate_food(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                if (self.currTemp >= 40 | self.currTemp <= 80) and (self.map[i][j].get_terrain() == "E"):
                    p = 0.5
                    newfood = bernoulli(p)
                    if newfood == 1:
                        self.map[i][j].set_food()
            return

    def delete_food(self, loc):
        tile = self.convertIDtoTile(loc)
        tile.totalFood = tile.totalFood - 1
        tile.food = False
        return

    def initialize_animals(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                p1 = .1
                p2 = 0.05
                newpredator = (np.random.rand() < p1) #bernoulli(p1)
                newprey =  (np.random.rand() < p2) #bernoulli(p2)
                location = (i, j)
                if (newpredator == 1):
                    newprey = False
                    self.create_predator(location)
                if (newprey == 1):
                    self.create_prey(location)
        self.current_order = copy.deepcopy(self.next_order)
        self.next_order = []
        return

    def create_predator(self, loc):
        # loc is pass in as "x, y"
        x = loc[0]
        y = loc[1]
        newPred = Predator(self.size_x,self.size_y, x, y, self.animal_id)
        self.IDtoAnimal[self.animal_id] = newPred
        self.IDtoLoc[self.animal_id] = loc
        self.next_order.append(self.animal_id)
        self.map[y][x].set_predator()

        self.animal_id = self.animal_id + 1
        self.numAnimals = self.numAnimals + 1
        self.numPredators += 1

        return

    def create_prey(self, loc):
        x = loc[0]
        y = loc[1]

        newPrey = Prey(self.size_x, self.size_y,x,y, self.animal_id)
        self.IDtoLoc[self.animal_id] = loc
        self.IDtoAnimal[self.animal_id] = newPrey
        self.next_order.append(self.animal_id)
        self.map[y][x].set_prey()

        self.animal_id = self.animal_id + 1
        self.numAnimals = self.numAnimals + 1
        self.numPrey += 1
        return

    def move_animal(self, animal_id, loc):
        animal = self.convertIDtoAnimal(animal_id)
        tile = self.convertIDtoTile(animal_id)
        newTile = self.locToTile(loc)


        #clear old tile
        tile.animal = False
        tile.has_pred = False
        tile.has_prey = False

        #update new tile
        newTile.animal = animal_id
        if animal.isPrey:
            newTile.has_prey = True
        else:
            newTile.has_pred = True




        self.IDtoLoc[animal_id] = loc
        return

    def delete_animal(self, animal_id):
        tile = self.convertIDtoTile(animal_id)
        tile.has_pred = 0
        tile.has_prey = 0
        tile.animal = False
        self.numAnimals = self.numAnimals - 1

        #if animal_id in self.current_order:
        #    self.current_order.remove(animal_id)

        if animal_id in self.next_order:
            self.next_order.remove(animal_id)

        if self.convertIDtoAnimal(animal_id).isPrey:
            self.numPrey -= 1
        else:
            self.numPredators -= 1

        self.IDtoAnimal.pop(animal_id)
        self.IDtoLoc.pop(animal_id)

        return

    def getNearbyFood(self, animalID):
        loc = self.convertIDtoLoc(animalID)
        locs_with_food = []
        search_dist = 1
        for i in range (loc[0] - search_dist, loc[1] + search_dist):
            for j in range (loc[0] - search_dist, loc[1] + search_dist):
                if self.locToTile((i, j)).has_food == True:
                    locs_with_food.append((i,j))
        return locs_with_food

    def getNearbyPredators(self, animalID):
        loc = self.convertIDtoLoc(animalID)
        locs_with_predators = []
        x = loc[0]
        y = loc[1]
        for i in range(x-1,x+1):
            for j in range(y-1,y+1):
                if self.map[j][i].is_pred():
                    locs_with_predators.append((i % self.size_x, j % self.size_y))
        return locs_with_predators

    def getNearbyPrey(self, animalID):
        loc = self.convertIDtoLoc(animalID)
        locs_with_prey = []
        x = loc[0]
        y = loc[1]
        for i in range(x-1,x+1):
            for j in range(y-1,y+1):
                if self.map[j][i].is_prey():
                    locs_with_prey.append((i % self.size_x, j % self.size_y))
        return locs_with_prey

    def getNearbyWater(self, animalID):
        loc = self.convertIDtoLoc(animalID)
        locs_with_water = []
        search_dist = 1
        for i in range (loc[0] - search_dist, loc[1] + search_dist):
            for j in range (loc[0] - search_dist, loc[1] + search_dist):
                if self.locToTile((i, j)).has_water == True:
                    locs_with_water.append((i,j))
        return locs_with_water

    def getTemp(self):
        return self.currTemp

    def getNextAnimal(self):
        if self.current_index >= len(self.current_order):
            self.current_index = 0
            self.current_order = copy.deepcopy(self.next_order)
            self.next_order = []
            return None

        self.current_index += 1
        return self.current_order[self.current_index - 1]

    def getNumAnimals(self):
        return self.numAnimals

    def getNumPredators(self):
        return self.numPredators

    def getNumPrey(self):
        return self.numPrey

