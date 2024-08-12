from BoardLoader import BoardLoader
from BoardSolver import BoardSolver


class TwoPlayerGame:
    def __init__(self, board_file):
        self.board = BoardLoader.load(board_file)
        self.current_player = 1

    def play(self):
        solver = BoardSolver(self.board)
        count = 0
        deadlock = False

        while not self.board.is_game_over():
            count += 1
            print(f"Player {self.current_player}'s turn")
            self.display_board()

            _, best_move = solver.minimax(self.board.grid, depth=2, player=self.current_player)
            print(f"Best move: {best_move}")
            print(best_move)
            if best_move:
                self.apply_move(best_move)
                deadlock = False
            else:
                deadlock = True

            if deadlock:
                print("Deadlock detected! Exiting...")
                break

            self.current_player = 3 - self.current_player  # Switch players (1 -> 2, 2 -> 1)

        self.display_board()
        winner = 1 if self.board.is_player_won(1) else 2
        print(f"Player {winner} wins!")

    def display_board(self):
        for row in self.board.grid:
            print(" ".join(cell.name if cell else "." for cell in row))
        print()

    def apply_move(self, move):
        vehicle, direction = move
        print(vehicle.get_occupied_locations())
        self.board.move_vehicle(vehicle, direction)


if __name__ == "__main__":
    game = TwoPlayerGame("boards/adv.txt")
    game.play()
