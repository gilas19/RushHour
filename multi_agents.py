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
        scores = [
            self.evaluation_function(game_state, action) for action in legal_moves
        ]
        best_score = max(scores)
        best_indices = [
            index for index in range(len(scores)) if scores[index] == best_score
        ]
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
        empty_cells = np.sum(board == 0)

        "*** YOUR CODE HERE ***"
        smoothness = 0
        for i in range(4):
            for j in range(3):
                if board[i, j] != 0:
                    smoothness -= abs(board[i, j] - board[i, j + 1])
                if board[j, i] != 0:
                    smoothness -= abs(board[j, i] - board[j + 1, i])

        corner_bonus = 0
        if max_tile in (board[0, 0], board[0, 3], board[3, 0], board[3, 3]):
            corner_bonus = 100

        return score + smoothness * 2 + empty_cells * 10 + max_tile * 2 + corner_bonus * 2

def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.s

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

    def __init__(self, evaluation_function="scoreEvaluationFunction", depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
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

        def minimax(state, depth, agent):
            if depth == 0 or state.done:
                return self.evaluation_function(state), Action.STOP

            if agent == 0:
                best_val = float("-inf")
                best_action = None
                for action in state.get_legal_actions(agent):
                    successor = state.generate_successor(agent, action)
                    val, _ = minimax(successor, depth, 1)
                    if val > best_val:
                        best_val = val
                        best_action = action
                return best_val, best_action
            else:
                best_val = float("inf")
                best_action = None
                for action in state.get_legal_actions(agent):
                    successor = state.generate_successor(agent, action)
                    val, _ = minimax(successor, depth - 1, 0)
                    if val < best_val:
                        best_val = val
                        best_action = action
                return best_val, best_action

        _, action = minimax(game_state, self.depth, 0)
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """*** YOUR CODE HERE ***"""

        def alpha_beta(state, depth, agent, alpha, beta):
            if depth == 0 or state.done:
                return self.evaluation_function(state), Action.STOP

            if agent == 0:
                best_val = float("-inf")
                best_action = None
                for action in state.get_legal_actions(agent):
                    successor = state.generate_successor(agent, action)
                    val, _ = alpha_beta(successor, depth, 1, alpha, beta)
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
                for action in state.get_legal_actions(agent):
                    successor = state.generate_successor(agent, action)
                    val, _ = alpha_beta(successor, depth - 1, 0, alpha, beta)
                    if val < best_val:
                        best_val = val
                        best_action = action
                    beta = min(beta, best_val)
                    if beta <= alpha:
                        break
                return best_val, best_action

        _, action = alpha_beta(game_state, self.depth, 0, float("-inf"), float("inf"))
        return action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""

        def expectimax(state, depth, agent):
            if depth == 0 or state.done:
                return self.evaluation_function(state), Action.STOP

            actions = state.get_legal_actions(agent)
            if agent == 0:
                best_val = float("-inf")
                best_action = None
                for action in actions:
                    successor = state.generate_successor(agent, action)
                    val, _ = expectimax(successor, depth, 1)
                    if val > best_val:
                        best_val = val
                        best_action = action
                return best_val, best_action
            else:
                total_val = 0
                for action in actions:
                    successor = state.generate_successor(agent, action)
                    val, _ = expectimax(successor, depth - 1, 0)
                    total_val += val
                return (
                    total_val / len(actions),
                    actions[np.random.randint(len(actions))],
                )

        _, action = expectimax(game_state, self.depth, 0)
        return action


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION:
    The evaluation function takes into account several factors:

    1. Score: The current score of the game is a primary factor.
    2. Empty Cells: The number of empty cells on the board, promotting states with more available moves.
    3. Smoothness: Measure how smooth the board is by calculating the difference between adjacent tiles,
       penalizing large diferences which indicate a less smooth board.
    4. Monotonicity: Encourages a board where values are consitently increasing or decreasing along rows or columns,
       which is a common strategy to achieve higher tiles.
    5. Max Tile Penalty: Penalizes situations where the highest tile is not in a corrner, as having high tiles in corners
       is often beneficial.
    6. Edge Preference: Adds a bonus for having higher value tiles on the edges of the board, which is generally a good strategy.

    The combined heuristic aims to balance these factors to provide a strong evaluation of the game state.

    """
    "*** YOUR CODE HERE ***"
    board = current_game_state.board
    empty_cells = np.sum(board == 0)
    max_tile = np.max(board)
    max_tile_penalty = 0

    if max_tile in (board[0, 0], board[0, 3], board[3, 0], board[3, 3]):
        max_tile_penalty = 1000 * max_tile

    # Smoothness
    horizontal_diffs = board[:, :-1] - board[:, 1:]
    horizontal_diffs = np.abs(horizontal_diffs[board[:, :-1] != 0])
    vertical_diffs = board[:-1, :] - board[1:, :]
    vertical_diffs = np.abs(vertical_diffs[board[:-1, :] != 0])
    smoothness = -(horizontal_diffs.sum() + vertical_diffs.sum())

    # Monotonicity
    diffs = np.diff(board)
    monotonicity = np.max([pow((diffs[i::2] > 0), 1.2) for i in range(2)])

    # edge priority
    edge_tiles = np.concatenate((board[0, :], board[-1, :], board[:, 0], board[:, -1]))
    edge_preference_bonus = np.sum(edge_tiles[edge_tiles > 2])

    return (
        current_game_state.score * 0.2
        + empty_cells * 10
        + smoothness * 3.5
        + monotonicity
        + max_tile_penalty
        + edge_preference_bonus * 0.4
    )


# Abbreviation
better = better_evaluation_function
