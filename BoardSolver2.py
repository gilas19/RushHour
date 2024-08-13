from copy import deepcopy
from util import Direction, Orientation
import Heuristics


class BoardSolver:
    def __init__(self, game_board):
        self.game_board = game_board

    def minimax(self, grid, depth, player, alpha=float("-inf"), beta=float("inf")):
        if depth == 0 or self.is_game_over(grid):
            return Heuristics.two_player_heuristic(grid, player), None

        if player == 1:
            best_value = float("-inf")
            best_move = None
            for move in self.get_legal_moves(grid, player):
                new_grid = self.apply_move(deepcopy(grid), move)
                value, _ = self.minimax(new_grid, depth - 1, 2, alpha, beta)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move
        else:
            best_value = float("inf")
            best_move = None
            for move in self.get_legal_moves(grid, player):
                new_grid = self.apply_move(deepcopy(grid), move)
                value, _ = self.minimax(new_grid, depth - 1, 1, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move

    def get_legal_moves(self, grid, player):
        legal_moves = []
        for row in grid:
            for cell in row:
                if vehicle and not vehicle.is_opponent_vehicle(player):
                    for direction in Direction:
                        if self.is_movable(vehicle, direction, grid):
                            legal_moves.append((vehicle, direction))
        return legal_moves

    def is_movable(self, vehicle, direction, grid):
        if vehicle.get_orientation() == Orientation.HORIZONTAL:
            if direction == Direction.FORWARD:
                new_x = vehicle.get_end_location()["x"] + 1
                new_y = vehicle.get_end_location()["y"]
            else:
                new_x = vehicle.get_start_location()["x"] - 1
                new_y = vehicle.get_start_location()["y"]
        else:
            if direction == Direction.FORWARD:
                new_x = vehicle.get_end_location()["x"]
                new_y = vehicle.get_end_location()["y"] + 1
            else:
                new_x = vehicle.get_start_location()["x"]
                new_y = vehicle.get_start_location()["y"] - 1

        return (0 <= new_x < len(grid[0])) and (0 <= new_y < len(grid)) and (grid[new_y][new_x] == 0)

    def find_vehicle(self, grid, name):
        for row in grid:
            for vehicle in row:
                if vehicle and vehicle.get_name() == name:
                    return vehicle

    def is_game_over(self, grid):
        return self.find_vehicle(grid, "X").end["x"] == len(grid[0]) - 1 or self.find_vehicle(grid, "Y").end["y"] == len(grid) - 1

    def apply_move(self, grid, move):
        vehicle, direction = move
        old_locations = vehicle.get_occupied_locations()
        if direction == Direction.FORWARD:
            vehicle.move_forward()
        else:
            vehicle.move_backward()
        new_locations = vehicle.get_occupied_locations()

        for location in old_locations:
            x, y = location["x"], location["y"]
            grid[x][y] = 0

        for location in new_locations:
            x, y = location["x"], location["y"]
            grid[x][y] = vehicle

        return grid











import threading
from copy import deepcopy
from BoardObjects import Vehicle
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

    def get_states(self, grid, player=1):
        """Calculate different possible states"""
        states = []
        self.expanded_nodes += 1

        for row in range(self.game_board.get_height()):
            for col in range(self.game_board.get_width()):
                vehicle = grid[col][row]
                if vehicle and vehicle.type != "broken_down" and not vehicle.is_opponent_vehicle(player):
                    for direction in Direction:
                        if self.is_movable(vehicle, direction, grid):
                            if player == 1:
                                new_grid = deepcopy(grid)
                            else:
                                new_grid = grid
                            new_vehicle = new_grid[col][row]

                            if direction == Direction.BACKWARD:
                                new_vehicle.move_backward()

                            if direction == Direction.FORWARD:
                                new_vehicle.move_forward()

                            old_locations = vehicle.get_occupied_locations()
                            new_locations = new_vehicle.get_occupied_locations()
                            new_grid = self.update_vehicle(new_grid, new_vehicle, old_locations, new_locations)
                            states.append([[[vehicle, direction]], new_grid])
        return states

    def copy_grid(self, grid):
        new_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
        for j in range(self.game_board.get_height()):
            for i in range(self.game_board.get_width()):
                if grid[i][j] != 0:
                    new_grid[i][j] = Vehicle(grid[i][j].name, grid[i][j].type, grid[i][j].start, grid[i][j].end)
        return new_grid

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

    # def is_solved(self, grid):
    #     """Check if game board is solved."""
    #     for row in range(self.game_board.get_height()):
    #         for column in range(self.game_board.get_width()):
    #             vehicle = grid[column][row]

    #             if (
    #                 vehicle
    #                 and vehicle.is_player_car()
    #                 and (column == self.game_board.get_width() - 1 or row == self.game_board.get_height() - 1)
    #             ):
    #                 return True
    #     return False

    def is_solved(self, grid):
        for row in grid:
            for vehicle in row:
                if vehicle and vehicle.is_player_car():
                    if (
                        vehicle.get_end_location()["x"] == self.game_board.get_width() - 1
                        or vehicle.get_end_location()["y"] == self.game_board.get_height() - 1
                    ):
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

    def minimax(self, grid, depth, player, alpha=float("-inf"), beta=float("inf")):
        if depth == 0 or self.is_solved(grid):
            return Heuristics.two_player_heuristic(grid, player), None

        if player == 1:
            best_value = float("-inf")
            best_move = None
            for state in self.get_states(grid, player):
                new_grid = state[1]
                value, _ = self.minimax(new_grid, depth - 1, 2, alpha, beta)
                if value > best_value:
                    best_value = value
                    best_move = state[0]
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move
        else:
            best_value = float("inf")
            best_move = None
            for state in self.get_states(grid, player):
                new_grid = state[1]
                value, _ = self.minimax(new_grid, depth - 1, 1, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_move = state[0]
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move
