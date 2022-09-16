from Map import Map
from Animal import Animal
from SensoryRange import SensoryRange
import random
from IPython.display import clear_output
import matplotlib.pyplot as plt
import numpy as np
# animal movement showing up on the grid
# animal interaction
# boundaries for map and animal movement
# generate map


class Simulation():
    def __init__(self, mapSize=(300,200), startingTemp=70, rateOfTempChange=1, numStartingAnimals=50, startingAnimalDistribution=[0.5,0.5], simulationLength=100):
        self.mapSize = mapSize
        # self.percentWaterTiles = percentWaterTiles
        self.startingTemp = startingTemp
        self.rateOfTempChange = rateOfTempChange
        self.numStartingAnimals = numStartingAnimals
        self.startingAnimalDistribution = startingAnimalDistribution
        self.simulationLength = simulationLength


        self.map = Map(self.mapSize, self.startingTemp, self.rateOfTempChange, self.startingAnimalDistribution)

        self.iteration = 0

    def simulationLoop(self, t):
        # Map.get_next_animal() -> either animal object or None

        animal = self.map.getNextAnimal()
        while animal != None:
            animal_sr = SensoryRange()

            #get data surrounding animal
            nearby_food = self.map.getNearbyFood(animal)
            animal_sr.setNearbyFood(nearby_food)
            nearby_predators = self.map.getNearbyPredators(animal)
            nearby_prey = self.map.getNearbyPrey(animal)
            animal_sr.setNearbyPredators(nearby_predators)
            animal_sr.setNearbyPrey(nearby_prey)
            nearby_tiles = self.map.getNearbyWater(animal)
            animal_sr.setNearbyWater(nearby_tiles)
            temp = self.map.getTemp()
            animal_sr.setTemp(temp)

            #pass data to animal and receive actions
            animal_obj = self.map.convertIDtoAnimal(animal)
            if animal_obj.isPrey:
                actions = animal_obj.preyReact(animal_sr)
            else:
                actions = animal_obj.predReact(animal_sr)


            #carry out actions

            survives = True
            for action in actions:
                if (action.type == "eat"):
                    if action.foodType == "animal":
                        self.map.delete_animal(action.foodLocation)
                    elif action.foodType == "plant":
                        self.map.delete_plant(action.foodLocation)

                elif (action.type == "move"):
                    self.map.move_animal(animal, action.endLocation)
                    #position x, position y

                elif (action.type == "reproduce"):
                    self.map.create_animal(animal, action.endLocation)

                elif (action.type == "drink"):
                    pass #no action needed
                elif (action.type == "die"):
                    self.map.delete_animal(animal)
                    survives = False
                    break #remove from map, delete animal
                else:
                    print("Invalid action type")
                    exit(1)

            if survives:
                self.map.next_order.append(animal)

            #end of animal loop
            animal = self.map.getNextAnimal()

        #Food
        self.map.generate_food()

        #Other Miscellanous
        #self.map.environmental_change()


    def run_simulation(self):
        num_predators = [self.map.getNumPredators()]
        num_prey = [self.map.getNumPrey()]
        time_graph = [0]


        animalMap = []
        for row in self.map.map:
            rowData = []
            for tile in row:
                if tile.is_prey():
                    rowData.append(1)
                elif tile.is_pred():
                    rowData.append(2)
                else:
                    rowData.append(0)

            animalMap.append(rowData)

        plt.imshow(animalMap)
        plt.show()

        t = 0
        while t < self.simulationLength:
            self.simulationLoop(t)
            t += 1
            # Visualize Current Simulation State
            time_graph.append(t)
            num_predators.append(self.map.getNumPredators())
            num_prey.append(self.map.getNumPrey())

            animalMap = []
            for row in self.map.map:
                rowData = []
                for tile in row:
                    if tile.is_prey():
                        rowData.append(1)
                    elif tile.is_pred():
                        rowData.append(2)
                    else:
                        rowData.append(0)

                animalMap.append(rowData)

            fig, ax = plt.subplots()
            plot = ax.imshow(animalMap)
            plt.show()
            clear_output(wait=True)
        """
        plt.plot(time_graph, num_predators, label = "Number of Predators")
        print(num_predators)
        plt.plot(time_graph, num_prey, label = "Number of Prey")
        print(num_prey)
        plt.legend()
        plt.show()
        plt.xlabel('Time')
        plt.ylabel('Number of Animals')
        plt.title("Population Dynamics")
        """


    # create the data to plot: example
    #x = np.t # time
    #y1 = np.num_predators
    #y2 = np.num_prey
    # add y3 = num_food, etc. as desired

    # makes interactive graph


    #for num in time_graph:
    #x = np.time_graph[num]
    #y1 = np.num_predators[num]
    #y2 = np.num_prey[num]
    # makes just one plot
    #line1, = ax.plot(x, y1, 'b-')
    #line2, = ax.plot(x, y2, 'r-')




    #hl, = plt.plot([], [])

    #def update_line(time, predators, prey):
    #line1.set_xdata(np.append(line1.get_xdata(), time))
    # line2.set_xdata(np.append(line2.get_xdata(), time))
    #line1.set_ydata(np.append(line1.get_ydata(),
    #predators))
    #line2.set_ydata(np.append(line2.get_ydata(),
    #prey))
    #plt.draw()

    #for phase in np.linspace(0, 200):
    #  self.run_simulation()
    #   update_line(t, num_predators, num_prey)




