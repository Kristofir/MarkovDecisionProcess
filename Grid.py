from types import *

from Square import Square

import collections
Location = collections.namedtuple('Location', 'x y')

class Grid(object):
    def __init__(self, raw_grid):
        self.grid_height = len(raw_grid)
        self.grid_width = len(raw_grid[0])

        self.grid = self.process(raw_grid)
        self.grid = self.network(self.grid)

        # Used as a top-down directory to order Squares.
        # Once raw data is processed, there will be a parallel but bottom-up directory ordering the Squares contained in and distributed among the Square objects themselves.
        # self.grid is processed in two steps: process() to populate then network() to link together squares


    def get_square(self, x, y):
        #from top directory
        return self.grid[y][x]


    def get_neighbors_locations(self, square):
        # from top directory

        neighbors_list = []
        # list of locations of neighbor within top directory, not the neighbor objects themselves

        def get_neighbors_locations_helper(x_adjacency, y_adjacency):
            neighbor_location = Location(square.x + x_adjacency, square.y + y_adjacency)
            if neighbor_location.x in range(0, self.grid_width) and neighbor_location.y in range(0, self.grid_height):
                #neighbor = self.get_square(neighbor_location.x, neighbor_location.y)
                neighbors_list.append(neighbor_location)
            else:
                pass

        for x_adjacency in [1, -1]:
            get_neighbors_locations_helper(x_adjacency, 0)
        for y_adjacency in [1, -1]:
            get_neighbors_locations_helper(0, y_adjacency)

        return neighbors_list


    def process(self, raw_grid):
        grid_container = []
        grid_height = len(raw_grid)
        grid_width = len(raw_grid[0])
        for y in range(0, grid_height):
            row_container = []
            for x in range(0, grid_width):
                square_value = raw_grid[y][x]
                is_wall = True if square_value is 'W' else False
                is_reward = True if type(square_value) is IntType and (square_value >= 1 or square_value <= -1) else False
                base_utility = square_value if type(square_value) is IntType or FloatType else 0
                new_square = Square(x, y, is_wall, is_reward, base_utility)
                # Create Square object based on values pulled from raw_grid
                row_container.append(new_square)
            grid_container.append(row_container)
        return grid_container


    def network(self, grid):
        for row in grid:
            for square in row:
                # each square is a Square object
                for neighbor_location in self.get_neighbors_locations(square):
                    square.make_neighbor(self.get_square(neighbor_location.x, neighbor_location.y))
                    square.update_neighbor_count()
        return grid



