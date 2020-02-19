import math
import random

import numpy as np
from .utils import get_random_coordinates, generate_coordinate_list_from_binary_map

class Food:
    '''
    Parameters
    ----------
    map_size: (int, int)
    food_spawn_location: [(int, int)] optional
        Parameter to force food to spawn in certain positions. Used for testing
        Food will spawn in the coordinates provided in the list until the list is exhausted.
        After the list is exhausted, food will be randomly spawned
    '''
    def __init__(self, map_size, food_spawn_locations=[]):
        self.map_size = map_size
        self.locations_map = np.zeros(shape=(map_size[0], map_size[1]))

        self.food_spawn_locations = food_spawn_locations
        self.max_turns_to_next_food_spawn = 9
        self.turns_since_last_food_spawn = 0

    @classmethod
    def make_from_list(cls, map_size, food_list):
        '''
        Class function to build the Food class.
        Parameters
        ---------
        map_size: (int, int)
        food_list: [(int, int)]
            Coordinates of the food locations
        '''
        cls = Food(map_size)
        for food in food_list:
            i, j = food
            cls.locations_map[i, j] = 1
        return cls

    def spawn_food(self, snake_map):
        '''
        Helper function to generate another food.
        
        Parameters:
        ----------
        snake_map, np.array(map_size[0], map_size[1], 1)
            The map of the location of each snake, generated by Snakes.get_snake_binary_map
        '''
        if len(self.food_spawn_locations) > 0:
            locations = [self.food_spawn_locations[0]]
            self.food_spawn_locations = self.food_spawn_locations[1:]
        else:
            snake_locations = generate_coordinate_list_from_binary_map(snake_map)
            locations = get_random_coordinates(self.map_size, 1, excluding=snake_locations)
        for location in locations:
            self.locations_map[location[0], location[1]] = 1

    def _calculate_food_spawn_chance(self):
        '''
        Helper function to calculate the chance of spawnning.
        Adapted from https://github.com/battlesnakeio/engine/blob/master/rules/tick.go
            calculateFoodSpawnChance()
        '''
        x = math.pow(1000/0.5, 1 / (self.max_turns_to_next_food_spawn - 1))
        y = self.turns_since_last_food_spawn
        return 0.5 * (1 - math.pow(x, y) / (1 - x))
        
    def end_of_turn(self, snake_locations, number_of_food_eaten, number_of_snakes_alive):
        '''
        Function to be called at the end of each step. 
        Adapted from https://github.com/battlesnakeio/engine/blob/master/rules/tick.go
            updateFood()
        '''
        number_of_food_to_spawn = 0
        if self.max_turns_to_next_food_spawn <= 0:
            number_of_food_to_spawn = number_of_food_eaten
        else:
            if self.turns_since_last_food_spawn >= self.max_turns_to_next_food_spawn:
                number_of_food_to_spawn = int(math.ceil(number_of_snakes_alive / 2))
            else:
                chance = random.random() * 1000
                calculated_chance = self._calculate_food_spawn_chance()
                if chance <= calculated_chance:
                    number_of_food_to_spawn = int(math.ceil(number_of_snakes_alive / 2))
                    self.turns_since_last_food_spawn = 0

        if number_of_food_to_spawn > 0:
            for i in range(number_of_food_to_spawn):
                self.spawn_food(snake_locations)
            self.turns_since_last_food_spawn = 0
        else:
            self.turns_since_last_food_spawn += 1
            
    def get_food_map(self):
        '''
        Function to get a binary image of all the present food
        Returns:
        --------
        map np.array
            binary image of size self.map_size indicating the positions
            of the food on the map.
        '''

        return self.locations_map

    def does_coord_have_food(self, coord):
        '''
        Function to check if a coordinate has food.

        Parameters
        ----------
        coord: (int, int)
            Input coordinate to check if food is available in this coordinate
        '''

        return self.locations_map[coord[0], coord[1]] == 1

    def remove_food_from_coord(self, coord):
        '''
        Function to remove a food present at coord
        '''
        self.locations_map[coord[0], coord[1]] = 0