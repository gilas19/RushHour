import numpy as np
import abc
import util
from game import Agent, Action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score

        "*** YOUR CODE HERE ***"

        return (score / max_tile) + len(successor_game_state.get_agent_legal_actions()) + max_tile


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def miniMax_min(self, current_depth, game_state):
        legal_actions = game_state.get_legal_actions(1)
        if current_depth == self.depth or len(legal_actions) == 0:
            return self.evaluation_function(game_state), Action.STOP
        value_action = dict()  # values : action
        for action in legal_actions:
            child = game_state.generate_successor(agent_index=1, action=action)
            value, given_action = self.miniMax_max(current_depth + 1, child)
            value_action[value] = action
        min_value = min(value_action.keys())
        return min_value, value_action[min_value]

    def miniMax_max(self, current_depth, game_state):
        legal_actions = game_state.get_legal_actions(0)
        if current_depth == self.depth or len(legal_actions) == 0:
            return self.evaluation_function(game_state), Action.STOP
        value_action = dict()  # values : action
        for action in legal_actions:
            child = game_state.generate_successor(agent_index=0, action=action)
            value, given_action = self.miniMax_min(current_depth, child)
            value_action[value] = action
        max_value = max(value_action.keys())
        return max_value, value_action[max_value]

    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        """*** YOUR CODE HERE ***"""
        ans = self.miniMax_max(0, game_state)
        return ans[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def AlphaBeta_min(self, current_depth, game_state, alpha, beta):
        legal_actions = game_state.get_legal_actions(1)
        if current_depth == self.depth or len(legal_actions) == 0:
            return self.evaluation_function(game_state), Action.STOP
        min_action = Action.STOP
        for action in legal_actions:
            if alpha >= beta:
                break
            child = game_state.generate_successor(agent_index=1, action=action)
            value, given_action = self.AlphaBeta_max(current_depth + 1, child, alpha, beta)
            if beta > value:
                beta = value
                min_action = action

        return beta, min_action

    def AlphaBeta_max(self, current_depth, game_state, alpha, beta):
        legal_actions = game_state.get_legal_actions(0)
        if current_depth == self.depth or len(legal_actions) == 0:
            return self.evaluation_function(game_state), Action.STOP
        max_action = Action.STOP
        for action in legal_actions:
            if alpha >= beta:
                break
            child = game_state.generate_successor(agent_index=0, action=action)
            value, given_action = self.AlphaBeta_min(current_depth, child, alpha, beta)
            if alpha < value:
                alpha = value
                max_action = action

        return alpha, max_action

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """*** YOUR CODE HERE ***"""
        ans = self.AlphaBeta_max(0, game_state, float("-inf"), float("inf"))
        return ans[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def ExpectimaxAgent_expected_value(self, current_depth, game_state):
        legal_actions = game_state.get_legal_actions(1)
        if current_depth == self.depth or len(legal_actions) == 0:
            return self.evaluation_function(game_state), Action.STOP
        total_value = 0
        for action in legal_actions:
            child = game_state.generate_successor(agent_index=1, action=action)
            value, given_action = self.ExpectimaxAgent_max(current_depth + 1, child)
            total_value += value

        return total_value / len(legal_actions), Action.STOP

    def ExpectimaxAgent_max(self, current_depth, game_state):
        legal_actions = game_state.get_legal_actions(0)
        if current_depth == self.depth or len(legal_actions) == 0:
            return self.evaluation_function(game_state), Action.STOP
        value_action = dict()  # values : action
        for action in legal_actions:
            child = game_state.generate_successor(agent_index=0, action=action)
            value, given_action = self.ExpectimaxAgent_expected_value(current_depth, child)
            value_action[value] = action
        max_value = max(value_action.keys())
        return max_value, value_action[max_value]

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        ans = self.ExpectimaxAgent_max(0, game_state)
        return ans[1]


def depth_first_search(problem):
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    visited = set()
    # stack gets tuple of (state,path)
    stack.push((problem.get_start_state(), []))

    while not stack.isEmpty():
        (state, path) = stack.pop()
        if problem.is_goal_state(state):
            return path
        if state in visited:
            continue

        for child in problem.get_successors(state):
            stack.push((child[0], path + [child[1]]))
        visited.add(state)

    return []


LOG_OF_TILE = {2 ** i: np.log2(2 ** i) for i in range(20)}


def get_tile_value(board, row, col):
    return board[row][col]


def large_values_on_edge(board):
    score = 0
    board_size = len(board)
    for i in range(board_size):
        if get_tile_value(board, 0, i) > 2:
            score += get_tile_value(board, 0, i)
        if get_tile_value(board, board_size - 1, i) > 2:
            score += get_tile_value(board, board_size - 1, i)
        if get_tile_value(board, i, 0) > 2:
            score += get_tile_value(board, i, 0)
        if get_tile_value(board, i, board_size - 1) > 2:
            score += get_tile_value(board, i, board_size - 1)
    return score


def highest_tile_in_corner(board):
    highest_tile = max(max(row) for row in board)
    board_size = len(board)
    corners = [board[0][0], board[0][board_size - 1], board[board_size - 1][0],
               board[board_size - 1][board_size - 1]]
    return highest_tile if highest_tile in corners else 0


def penaltie_smoothness(prev_val, cur_val):
    if prev_val == 0:
        return 0
    return max(1, abs(prev_val - cur_val))


def bonus_potential_merges(prev_val, cur_val):
    if prev_val == cur_val:
        return 1
    return 0


def better_evaluation_calculate(board):
    empty_squares = 0
    weighted_sum = 0
    potential_merges = 0
    smoothness_penalties = 0
    row_dict = dict()
    col_dict = dict()
    for i in range(board.shape[0]):
        row_dict[i] = 0
        for j in range(board.shape[1]):
            if i == 0:
                col_dict[j] = 0
            if board[i, j] > 0:
                smoothness_penalties -= (
                        penaltie_smoothness(row_dict[i], board[i, j]) +
                        penaltie_smoothness(col_dict[j],board[i, j]))
                potential_merges += (
                        bonus_potential_merges(row_dict[i], board[i, j]) +
                        bonus_potential_merges(col_dict[j],board[i, j]))

                row_dict[i] = board[i, j]
                col_dict[j] = board[i, j]
                if board[i, j] <= 32:
                    weighted_sum += board[i, j] * LOG_OF_TILE[board[i, j]]
                else:
                    weighted_sum += board[i, j] * LOG_OF_TILE[board[i, j]] * 2
            else:
                empty_squares += 1
    large_edge_score = large_values_on_edge(board)
    corner_score = highest_tile_in_corner(board)
    return weighted_sum + 3 * smoothness_penalties + 4 * empty_squares \
           + 1.5 * large_edge_score\
           + 3 * potential_merges\
           + 3 * corner_score


def better_evaluation_function(current_game_state):
    board = current_game_state.board
    return better_evaluation_calculate(board)


# Abbreviation
better = better_evaluation_function
