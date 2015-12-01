from pprint import pprint


class grid():

    def __init__(self):
        self.grid = [[-0.04, -1, -0.4, -0.04, -0.04, -0.04],
[-0.04, -0.04, -0.04, 'W', -1, -0.04],
[-0.04, -0.04, -0.04, 'W', -0.04, +3],
[-0.04, -0.04, -0.04, 'W', -0.04, -0.04],
[1, -1, -0.04, 'W', -1, -1]]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

        self._discount_factor = 0.99
        self._intended_probability = 0.8
        self._errant_probability = 0.1

    def output(self):
        pprint(self.grid)

    def get_value_at(self, x, y):
        return self.grid[y][x]

    def is_wall(self, x, y):
        if self.get_value_at(x, y) is 'W':
            return True
        else:
            return False

    def is_start(self, x, y):
        if self.get_value_at(x, y) is 'S':
            return True
        else:
            return False

    def is_in_bounds(self, x, y):
        if (x < 0) and (x >= self.width):
            return False
        if (y < 0) and (y >= self.height):
            return False
        return True

    def is_walkable(self, x, y):
        # Tidy up by combining two verification methods
        if self.is_in_bounds(x, y) and not self.is_wall(x, y):
            return True
        else:
            return False

    def which_way_to_go_from(self, x, y):
        best_direction_yet = 'X'
        reference_utility = self.get_value_at(x, y)
        highest_utility_delta_yet = reference_utility
        # Check north
        if self.is_walkable(x, y-1):
            north_utility = self.get_value_at(x, y-1)
            if north_utility > highest_utility_delta_yet:
                highest_utility_delta_yet = north_utility
                best_direction_yet = 'N'
        # Check south
        if self.is_walkable(x, y+1):
            south_utility = self.get_value_at(x, y+1)
            if south_utility > highest_utility_delta_yet:
                highest_utility_delta_yet = south_utility
                best_direction_yet = 'S'
        # Check east
        if self.is_walkable(x+1, y):
            north_utility = self.get_value_at(x+1, y)
            if north_utility > highest_utility_delta_yet:
                highest_utility_delta_yet = north_utility
                best_direction_yet = 'E'
        # Check west
        if self.is_walkable(x-1, y):
            south_utility = self.get_value_at(x-1, y)
            if south_utility > highest_utility_delta_yet:
                highest_utility_delta_yet = south_utility
                best_direction_yet = 'W'
        return best_direction_yet

    def update_utility(self, x, y, direction, grid_canvas):
        existing_utility = self.get_value_at(x, y)
        # These variables adjust the direction.
        x_id = 0
        y_id = 0
        x_ld = 0
        y_ld = 0
        x_rd = 0
        y_rd = 0
        if direction is 'N':
            y_id = -1
            x_ld = -1
            x_rd = 1
        elif direction is 'S':
            y_id = 1
            x_ld = 1
            x_rd = -1
        elif direction is 'E':
            x_id = 1
            y_ld = -1
            y_rd = 1
        elif direction is 'W':
            x_id = -1
            y_ld = 1
            y_rd = -1
        intended_utility = self.get_value_at(x+x_id, y+y_id)
        left_errant_utility = 0
        if self.is_walkable(x+x_ld, y+y_ld):
            left_errant_utility = self.get_value_at(x+x_ld, y+y_ld)
        right_errant_utility = 0
        if self.is_walkable(x+x_rd, y+y_rd):
            right_errant_utility = self.get_value_at(x+x_rd, y+y_rd)
        new_utility = self._intended_probability * intended_utility + self._errant_probability * left_errant_utility  + self._errant_probability * right_errant_utility
        grid_canvas[y][x] = new_utility


    def compute_policy(self, number_of_iterations):
        while number_of_iterations is not 0:
            self.value_iterate()
            number_of_iterations -= 1

    def value_iterate(self):
        g_canvas = self.grid
        for y in range(0, self.height-1):
            for x in range(0, self.width-1):
                intended_direction = self.which_way_to_go_from(x, y)
                if intended_direction is not 'X':
                    # If a cardinal direction is returned, it means that a neighbor has a greater utility.
                    self.update_utility(x, y, intended_direction, g_canvas)

g = grid()

g.compute_policy(1)

g.output()
