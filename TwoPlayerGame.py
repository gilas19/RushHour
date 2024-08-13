from BoardLoader import BoardLoader
from BoardSolver import AlphaBetaAgent, RandomAgent


class TwoPlayerGame:
    def __init__(self, board_file):
        self.board = BoardLoader.load(board_file)
        self.current_player = 1
        self.agent = AlphaBetaAgent(1)
        self.opponent = RandomAgent(2)

    def play(self):
        count = 0
        deadlock = False

        # while not self.board.is_game_over():
        for _ in range(10):
            self.display_board()
            if self.current_player == 1:
                move = self.agent.get_action(self.board)
            else:
                move = self.opponent.get_action(self.board)
            print(f"Player {self.current_player} moves {move}")
            if move:
                self.apply_move(move)
                deadlock = False
            else:
                if deadlock:
                    break
                deadlock = True
            self.current_player = 1 if self.current_player == 2 else 2
            count += 1

        self.display_board()
        if deadlock:
            print("Game ended in a deadlock.")
        else:
            print(f"Player {self.current_player} won!")

    def display_board(self):
        for row in self.board.grid:
            print(" ".join(cell.name if cell else "." for cell in row))
        print()

    def apply_move(self, move):
        vehicle, direction = move
        self.board.move_vehicle(vehicle, direction)


if __name__ == "__main__":
    game = TwoPlayerGame("boards/adv.txt")
    game.play()
