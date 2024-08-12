from copy import deepcopy
from util import Direction, Orientation
import Heuristics


class BoardSolver:
    def __init__(self, game_board):
        self.game_board = game_board

    def minimax(self, state, depth, player, alpha=float("-inf"), beta=float("inf")):
        if depth == 0 or state.is_game_over():
            return Heuristics.two_player_heuristic(state, player), None

        if player == 1:
            best_value = float("-inf")
            best_move = None
            for move in self.get_legal_moves(state, player):
                new_state = self.apply_move(state, move, player)
                value, _ = self.minimax(new_state, depth - 1, 2, alpha, beta)
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
            for move in self.get_legal_moves(state, player):
                new_state = self.apply_move(state, move, player)
                value, _ = self.minimax(new_state, depth - 1, 1, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move

    def get_legal_moves(self, state, player):
        legal_moves = []
        for row in range(state.get_height()):
            for col in range(state.get_width()):
                vehicle = state.grid[row][col]
                if vehicle and not vehicle.is_opponent_vehicle(player):
                    for direction in Direction:
                        if self.is_movable(vehicle, direction, state):
                            legal_moves.append((vehicle, direction))
        return legal_moves

    def apply_move(self, state, move, player):
        new_state = deepcopy(state)
        vehicle, direction = move
        new_state.move_vehicle(vehicle, direction)
        return new_state

    def is_movable(self, vehicle, direction, state):
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

        return state.is_within_bounds(new_x, new_y) and state.grid[new_y][new_x] == 0
