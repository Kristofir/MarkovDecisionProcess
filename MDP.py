from types import *

import svgwrite

from Grid import Grid

class MDP(Grid):

    def __init__(self, raw_grid):
        Grid.__init__(self, raw_grid)
        # Inherits Grid class
        self.number_of_iterations_yet = 0
        self.gamma = 0.7
        # gamma : discount factor

        self.errant_probability = 0.1
        # two errant outcomes
        self.intended_probability = 0.8
        # one intended outcome


    def analyze_environment(self, number_of_cycles):
        while number_of_cycles is not 0:
            print "cycles remaining: " + str(number_of_cycles)
            self.value_iterate()
            number_of_cycles -= 1


    def value_iterate(self):

        for row in self.grid:
            for square in row:
                # don't want to modify reward states...
                # ... IF THEY'RE ABSORBING!
                if not square.is_reward and not square.is_wall:

                    transition_utilities = []
                    for direction in ['N', 'E', 'S', 'W']:
                        transition_utility = self.compute_utility(square, direction)
                        if (square.x, square.y) == (2, 2):
                            print direction, (square.get_neighbor_in_dir_of(direction)).get_utility(), transition_utility
                        transition_utilities.append(transition_utility)

                    bellman_eqn = self.gamma * max(transition_utilities)

                    if (square.x, square.y) == (2, 2):
                        print "Tran utils: " + str(transition_utilities),
                        print str(bellman_eqn) + " chosen"
                    square.update_utility(bellman_eqn)

                else:
                    pass

        for row in self.grid:
            for square in row:
                square.turnover()

        self.number_of_iterations_yet += 1


    def get_errant_directions(self, intended_direction):
        # used in self.compute_utility(...)

        errant_directions = []

        if intended_direction is 'N' or 'S':
            errant_directions = ['W', 'E']

        elif intended_direction is 'E' or 'W':
            errant_directions = ['N', 'S']

        return errant_directions


    def compute_utility(self, base_square, intended_direction):
        # uses self.get_errant_directions(...)

        transition_utility = float(0)

        # errant outcomes:
        for errant_direction in self.get_errant_directions(intended_direction):

            errant_neighbor = base_square.get_neighbor_in_dir_of(errant_direction)
            # returns Square obj; errant neighbor may be None.

            errant_utility = float(0)

            if errant_neighbor is not None and not errant_neighbor.is_wall:
                errant_utility = float(self.errant_probability * errant_neighbor.get_previous_utility())
            else:
                pass

            transition_utility += errant_utility

        # intended outcome:
        intended_neighbor = base_square.get_neighbor_in_dir_of(intended_direction)
        if intended_neighbor is not None and not intended_neighbor.is_wall:

            intended_utility = float(self.intended_probability * intended_neighbor.get_previous_utility())

            transition_utility += intended_utility

        return transition_utility


    def output(self):
        for row in self.grid:
            for square in row:
                print square.get_utility(),
                #print square.north_neighbor.x if square.north_neighbor is not None else 0,
                #print square.neighbor_count,
            print
        print "grid.output() successful."
        return 0


    def output_state_map(self):
        for row in self.grid:
            for square in row:
                if square.is_reward:
                    print "X",
                else:
                    print "O",
            print


    def graphic_output(self):

        cell_size = 100
        canvas_width = self.grid_width * cell_size
        canvas_height = self.grid_height * cell_size

        fname = "graph i=" + str(self.number_of_iterations_yet) + " width=" + str(canvas_width) + " height=" +str(canvas_height) + ".svg"

        dwg = svgwrite.Drawing(filename = fname, size = (canvas_width, canvas_height), debug = True)

        # Draw horizontal grid lines
        #for x in range(0, self.grid_width):
        #    dwg.add( dwg.line((x*cell_size, 0), (x*cell_size, canvas_height), stroke=svgwrite.rgb(0, 0, 0, "%")) )

        #for y in range(0, self.grid_height):
        #    dwg.add( dwg.line((0, y*cell_size), (canvas_width, y*cell_size), stroke=svgwrite.rgb(0, 0, 0, "%")) )

        for row in self.grid:
            for square in row:
                shapes = dwg.add(dwg.g(id='shapes', fill='red'))
                color_numerator = float(square.get_utility())  if type(square.get_utility()) is IntType else 0
                color_denominator = 2
                fill_color = svgwrite.rgb(255, 255, 255)
                if color_numerator > 0:
                    fill_color = svgwrite.rgb(255-250*(color_numerator/color_denominator), 220, 255-200*(color_denominator/color_denominator))
                elif color_numerator < 0:
                    fill_color = svgwrite.rgb(220, 255-250*(abs(color_numerator)/color_denominator), 255-250*(abs(color_numerator)/color_denominator) )

                shapes.add( dwg.rect(insert=(square.x*cell_size, square.y*cell_size), size=(cell_size, cell_size), fill=fill_color) )
                paragraph = dwg.add(dwg.g(font_size=16))
                paragraph.add(dwg.text(square.get_utility(), ( (square.x + 0.5) * cell_size, (square.y + 0.5) * cell_size)))

        dwg.save()
        print "grid.graphic_output() successful"
        return 0

raw_grid = [[-0.04, -1, -0.4, -0.04, -0.04, -0.04],
[-0.04, -0.04, -0.04, 'W', -1, -0.04],
[-0.04, -0.04, -0.04, 'W', -0.04, +3],
[-0.04, -0.04, -0.04, 'W', -0.04, -0.04],
[-0.04, -0.04, -0.04, -0.04, -0.04, -0.04],
[1, -1, -0.04, 'W', -1, -1]]

g = MDP(raw_grid)
g.output_state_map()
g.graphic_output()

#for row in g.grid:
#    for obj in row:
#        print type(obj.utility)

g.analyze_environment(1)
g.output()
g.graphic_output()