import threading
from copy import deepcopy
from enums.direction import Direction
from enums.orientation import Orientation
import util


class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost


class BoardSolver(object):
    def __init__(self, game_board):
        self.game_board = game_board
        # self.console_view = console_view
        self.solution = None

    def display_grid(self, grid, height, width):
        """Display the loaded game board."""
        # Display game board
        print('\n')
        print('\n')
        for row in range(height):
            for column in range(width):
                vehicle = grid[column][row]
                if vehicle:
                    print('%s ' % vehicle.get_name(),end=' ')
                else:
                    print('. ',end=' ')

                if column == width - 1:
                    print('\n')

    # def get_successors(self, state):
    #     """
    #     state: Search state
    #
    #     For a given state, this should return a list of triples,
    #     (successor, action, stepCost), where 'successor' is a
    #     successor to the current state, 'action' is the action
    #     required to get there, and 'stepCost' is the incremental
    #     cost of expanding to that successor
    #     """
    #     # Note that for the search problem, there is only one player - #0
    #     self.expanded = self.expanded + 1
    #     return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_states(0)]


    def a_star_search(self, heuristic=None):
        """
        Search the node that has the lowest combined cost and heuristic first.
        """
        "*** YOUR CODE HERE ***"
        prior_queue = util.PriorityQueue()
        visited = set()
        start_state = self.game_board.get_grid()
        nodes_info = Node(start_state, [], 0)
        # prior_queue.push(nodes_info, nodes_info.cost + null_heuristic(start_state, problem))
        prior_queue.push(nodes_info, nodes_info.cost + 0)


        while not prior_queue.isEmpty():
            node = prior_queue.pop()
            if self.is_solved(node.state):
                self.display_grid(node.state, self.game_board.get_height(), self.game_board.get_width())

                return node.path
            if hash(str(node.state)) in visited:
                continue

            #states.append([[[vehicle, direction]], new_grid])
            #vehicle == successor
            for [(vehicle, direction)], new_grid in self.get_states(node.state):
                # print("successor",vehicle)
                # print("direction",direction)
                # print("new_grid",new_grid)

                child_node = Node(new_grid, node.path + [(vehicle,direction)], node.cost + 1)
                prior_queue.push(child_node, child_node.cost + 0)
                # prior_queue.push(child_node, child_node.cost + null_heuristic(successor, problem))


            visited.add(hash(str(node.state)))

        return []



    def get_solution_BFS(self):
        """Run the breadth first search algorithm to find the solution."""
        grid = self.game_board.get_grid()
        visited = set()
        queue = [[[], grid]]

        while len(queue) > 0:
            for item in range(len(queue)):
                moves, grid = queue.pop(0)


                if self.is_solved(grid):
                    self.display_grid(grid, self.game_board.get_height(), self.game_board.get_width())
                    return moves

                for new_moves, new_grid in self.get_states(grid):
                    if hash(str(new_grid)) not in visited:
                        queue.append([moves + new_moves, new_grid])
                        visited.add(hash(str(new_grid)))

        self.display_grid(grid, self.game_board.get_height(), self.game_board.get_width())

        return None

    def get_states(self, grid):
        """Calculate different possible states"""
        states = []

        for row in range(self.game_board.get_height()):
            for column in range(self.game_board.get_width()):
                vehicle = grid[column][row]
                if vehicle:
                    for direction in Direction:
                        if self.is_movable(vehicle, direction, grid):
                            new_grid = deepcopy(grid)

                            new_vehicle = new_grid[column][row]

                            if direction == Direction.BACKWARD:
                                new_vehicle.move_backward()

                            if direction == Direction.FORWARD:
                                new_vehicle.move_forward()

                            old_locations = vehicle.get_occupied_locations()
                            new_locations = new_vehicle.get_occupied_locations()
                            new_grid = self.update_vehicle(new_grid, new_vehicle, old_locations, new_locations)
                            states.append([[[vehicle, direction]], new_grid])
        return states

    @staticmethod
    def update_vehicle(grid, vehicle, old_locations, new_locations):
        """Update grid with the vehicles' new location."""
        for location in old_locations:
            x = location['x']
            y = location['y']
            grid[x][y] = 0

        for location in new_locations:
            x = location['x']
            y = location['y']
            grid[x][y] = vehicle

        return grid

    def is_movable(self, vehicle, direction, grid):
        """Check if vehicle object is movable to the next empty space."""
        if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.FORWARD:
            location = vehicle.get_end_location()
            x = location['x'] + 1
            y = location['y']

            if x < self.game_board.get_width():
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.BACKWARD:
            location = vehicle.get_start_location()
            x = location['x'] - 1
            y = location['y']

            if x > -1:
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.FORWARD:
            location = vehicle.get_end_location()
            x = location['x']
            y = location['y'] + 1

            if y < self.game_board.get_height():
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.BACKWARD:
            location = vehicle.get_start_location()
            x = location['x']
            y = location['y'] - 1

            if y > -1:
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        return True

    def is_solved(self, grid):
        """Check if game board is solved."""
        for row in range(self.game_board.get_height()):
            for column in range(self.game_board.get_width()):
                vehicle = grid[column][row]

                if vehicle and vehicle.is_main_vehicle() and column == self.game_board.get_width() - 1:
                    return True
        return False


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
