from GameBoard import GameBoard
from Agents import AlphaBetaAgent, RandomAgent, AStarAgent, BFSAgent
from Display import GUIView


class TwoPlayerGame:
    def __init__(self, board_file):
        self.board = GameBoard(file=board_file)
        self.current_player = 1
        self.agent = AlphaBetaAgent(1)
        self.opponent = AlphaBetaAgent(2)

    def play(self):
        count = 0
        deadlock = False

        # while not self.board.is_game_over():
        for _ in range(3):
            self.board.display()
            if self.current_player == 1:
                move = self.agent.get_action(self.board)
            else:
                move = self.opponent.get_action(self.board)
            print(f"Player {self.current_player} moves {move}")
            if move:
                self.board.move(*move)
                deadlock = False
            else:
                if deadlock:
                    break
                deadlock = True
            self.current_player = 1 if self.current_player == 2 else 2
            count += 1

        self.board.display()
        if deadlock:
            print("Game ended in a deadlock.")
        else:
            print(f"Player {self.current_player} won!")


class SinglePlayerGame:
    def __init__(self, board_file):
        self.board = GameBoard(file=board_file)
        self.current_player = 1
        self.agent = BFSAgent(1)
        self.display = GUIView()

    def play(self):
        self.board.display()
        solution = self.agent.get_solution(self.board)

        if solution:
            print(len(solution), solution)
            self.display.animate_solution(self.board, solution)


if __name__ == "__main__":
    # game = TwoPlayerGame("adv2")
    # game.play()
    game = SinglePlayerGame("beginner")
    game.play()
