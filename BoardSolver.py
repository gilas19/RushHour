import Heuristics
import random


class RandomAgent:
    def __init__(self, player):
        self.player = player

    def get_action(self, game_board):
        actions = game_board.get_legal_actions(self.player)
        return random.choice(actions)


class AlphaBetaAgent:
    def __init__(self, player, depth=2, evaluation_function="two_players"):
        self.player = player
        self.depth = depth
        self.evaluation_function = getattr(Heuristics, evaluation_function)

    def get_action(self, game_board):

        def alpha_beta(board, depth, agent, alpha, beta):
            if depth == 0 or board.is_solved():
                return self.evaluation_function(board, agent), None

            if agent == 1:
                best_val = float("-inf")
                best_action = None
                for action in board.get_legal_actions(agent):
                    successor = board.generate_successor(agent, action)
                    val, _ = alpha_beta(successor, depth, 2, alpha, beta)
                    if val > best_val:
                        best_val = val
                        best_action = action
                    alpha = max(alpha, best_val)
                    if beta <= alpha:
                        break
                return best_val, best_action
            else:
                best_val = float("inf")
                best_action = None
                for action in board.get_legal_actions(agent):
                    successor = board.generate_successor(agent, action)
                    val, _ = alpha_beta(successor, depth - 1, 1, alpha, beta)
                    if val < best_val:
                        best_val = val
                        best_action = action
                    beta = min(beta, best_val)
                    if beta <= alpha:
                        break
                return best_val, best_action

        _, action = alpha_beta(game_board, self.depth, self.player, float("-inf"), float("inf"))
        return action
