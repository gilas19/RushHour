import Heuristics
import random
import util
from util import Node


class BFSAgent:
    def __init__(self, player=1):
        self.player = player
        self.expanded_nodes = 0

    def get_solution(self, board):
        """Run the breadth first search algorithm to find the solution."""
        visited = set()
        queue = [[[], board]]

        while len(queue) > 0:
            for item in range(len(queue)):
                moves, board = queue.pop(0)
                self.expanded_nodes += 1

                if board.is_solved():
                    return moves

                for new_moves, new_grid in board.get_possible_moves(self.player):
                    if hash(str(new_grid)) not in visited:
                        queue.append([moves + new_moves, new_grid])
                        visited.add(hash(str(new_grid)))
        return []


class AStarAgent:
    def __init__(self, player=1, heuristic="distance_to_goal"):
        self.player = player
        self.heuristic = getattr(Heuristics, heuristic)
        self.expanded_nodes = 0

    def get_solution(self, board):
        prior_queue = util.PriorityQueue()
        visited = set()
        nodes_info = Node(board, [], 0)
        prior_queue.push(nodes_info, nodes_info.cost + self.heuristic(board, self.player))

        while not prior_queue.isEmpty():
            node = prior_queue.pop()
            self.expanded_nodes += 1
            if node.state.is_solved():
                return node.path
            if hash(str(node.state)) in visited:
                continue

            for new_moves, new_grid in node.state.get_possible_moves(self.player):
                child_node = Node(new_grid, node.path + new_moves, node.cost + 1)
                prior_queue.push(child_node, child_node.cost + self.heuristic(child_node.state, self.player))
            visited.add(hash(str(node.state)))

        return []


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
                print(agent, self.evaluation_function(board, agent))
                print(board.grid)
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
