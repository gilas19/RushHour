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
