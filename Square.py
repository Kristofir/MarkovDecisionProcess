class Square(object):

    def __init__(self, x, y, is_wall = False, is_reward = False, initial_utility = 0):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.is_reward = is_reward
        #self.utility = [initial_utility, initial_utility]
        self.new_utility = initial_utility
        self.old_utility = initial_utility
        self.north_neighbor = None
        self.north_Q_value = 0

        self.east_neighbor = None
        self.east_Q_value = 0

        self.south_neighbor = None
        self.south_Q_value = 0

        self.west_neighbor = None
        self.west_Q_value = 0

        self.neighbor_count = 0


    def get_neighbors(self):
        neighbors = []
        for neighbor in [self.north_neighbor, self.east_neighbor, self.south_neighbor, self.west_neighbor]:
            if neighbor is not None and not neighbor.is_wall:
                neighbors.append(neighbor)
            else:
                pass
        return neighbors


    def get_neighbor_in_dir_of(self, direction):
        if direction is 'N':
            return self.north_neighbor
        elif direction is 'E':
            return self.east_neighbor
        elif direction is 'S':
            return self.south_neighbor
        elif direction is 'W':
            return self.west_neighbor
        else:
            print "fn: get_neighbor_in_dir_of. arg: invalid direction"


    def get_utility(self):
        #return self.utility[-1]
        return self.new_utility


    def get_previous_utility(self):
        #return self.utility[-2]
        return self.old_utility

    def turnover(self):
        self.old_utility = self.new_utility

    def make_neighbor(self, other):
        # other : other square
        is_neighbor = True if abs(self.x-other.x + self.y-other.y) is 1 else False
        if is_neighbor:
            # 0,0 designates top-left grid corner

            if self.x - other.x is 1:
                # other square is west
                self.west_neighbor = other
                other.east_neighbor = self

            elif self.x - other.x is -1:
                # other square is east
                self.east_neighbor = other
                other.west_neighbor = self

            elif self.y - other.y is 1:
                # other square is north
                self.north_neighbor = other
                other.south_neighbor = self

            elif self.y - other.y is -1:
                # other square is south
                self.south_neighbor = other
                other.north_neighbor = self

            # no need for else in this if statement

        else:
            print "Problem neighbor-making"


    def update_neighbor_count(self):
        count = 0
        if self.north_neighbor is not None:
            count += 1
        if self.east_neighbor is not None:
            count += 1
        if self.west_neighbor is not None:
            count += 1
        if self.south_neighbor is not None:
            count += 1
        self.neighbor_count = count


    def update_utility(self, new_utility):
        #self.utility.append(new_utility)
        self.new_utility = new_utility
