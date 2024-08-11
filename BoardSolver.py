import threading
from copy import deepcopy
from util import Direction, Orientation
import util
import time
import Heuristics
from util import Node, PriorityQueue


class BoardSolver(object):
    def __init__(self, game_board, search_algo, heuristic=None):
        self.game_board = game_board
        self.search_algo = getattr(self, search_algo)
        self.heuristic = getattr(Heuristics, heuristic) if heuristic else None
        self.solution = None
        self.expanded_nodes = 0

    def solve(self):
        """Run the search algorithm to find the solution."""
        start_time = time.time()
        if self.heuristic:
            self.solution = self.search_algo(self.heuristic)
        else:
            self.solution = self.search_algo()
        end_time = time.time()
        time_delta = end_time - start_time
        return time_delta

    def from_moves_to_grids(self, moves):
        """Convert moves to grids."""
        grids = [self.game_board.get_grid()]
        for move in moves:
            grid = deepcopy(grids[-1])
            vehicle = move[0]
            direction = move[1]
            old_locations = vehicle.get_occupied_locations()

            if direction == Direction.FORWARD:
                vehicle.move_forward()
            if direction == Direction.BACKWARD:
                vehicle.move_backward()

            new_locations = vehicle.get_occupied_locations()
            grid = self.update_vehicle(grid, vehicle, old_locations, new_locations)
            grids.append(grid)
        return grids

    def get_states(self, grid):
        """Calculate different possible states"""
        states = []
        self.expanded_nodes += 1

        for row in range(self.game_board.get_height()):
            for column in range(self.game_board.get_width()):
                vehicle = grid[column][row]
                if vehicle and vehicle.type != "broken_down":
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
            x = location["x"]
            y = location["y"]
            grid[x][y] = 0

        for location in new_locations:
            x = location["x"]
            y = location["y"]
            grid[x][y] = vehicle

        return grid

    def is_movable(self, vehicle, direction, grid):
        """Check if vehicle object is movable to the next empty space."""
        if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.FORWARD:
            location = vehicle.get_end_location()
            x = location["x"] + 1
            y = location["y"]

            if x < self.game_board.get_width():
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.BACKWARD:
            location = vehicle.get_start_location()
            x = location["x"] - 1
            y = location["y"]

            if x > -1:
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.FORWARD:
            location = vehicle.get_end_location()
            x = location["x"]
            y = location["y"] + 1

            if y < self.game_board.get_height():
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.BACKWARD:
            location = vehicle.get_start_location()
            x = location["x"]
            y = location["y"] - 1

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

    def astar(self, heuristic=None):
        """
        Search the node that has the lowest combined cost and heuristic first.
        """

        prior_queue = PriorityQueue()
        visited = set()
        game_board = self.game_board
        nodes_info = Node(game_board.get_grid(), [], 0)
        # prior_queue.push(nodes_info, nodes_info.cost + null_heuristic(start_state, problem))
        prior_queue.push(nodes_info, nodes_info.cost + heuristic(game_board.get_grid(), game_board.get_height(), game_board.get_width()))

        while not prior_queue.isEmpty():
            node = prior_queue.pop()
            if self.is_solved(node.state):
                return node.path
            if hash(str(node.state)) in visited:
                continue

            # states.append([[[vehicle, direction]], new_grid])
            # vehicle == successor
            for [(vehicle, direction)], new_grid in self.get_states(node.state):
                # print("successor",vehicle)
                # print("direction",direction)
                # print("new_grid",new_grid)

                child_node = Node(new_grid, node.path + [(vehicle, direction)], node.cost + 1)
                prior_queue.push(child_node, child_node.cost + heuristic(child_node.state, game_board.get_height(), game_board.get_width()))
                # prior_queue.push(child_node, child_node.cost + null_heuristic(successor, problem))

            visited.add(hash(str(node.state)))
        return []

    def bfs(self):
        """Run the breadth first search algorithm to find the solution."""
        grid = self.game_board.get_grid()
        visited = set()
        queue = [[[], grid]]

        while len(queue) > 0:
            for item in range(len(queue)):
                moves, grid = queue.pop(0)
                if self.is_solved(grid):
                    return moves

                for new_moves, new_grid in self.get_states(grid):
                    if hash(str(new_grid)) not in visited:
                        queue.append([moves + new_moves, new_grid])
                        visited.add(hash(str(new_grid)))
        return None
