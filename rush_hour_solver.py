import sys
import time
from controllers.board_loader import BoardLoader
from controllers.board_solver import BoardSolver
from views.console_view import ConsoleView


class RushHourSolver(object):
    def __init__(self,board_file):
        self.console_view = ConsoleView()
        self.run(board_file)

    def display_grid(self, grid, height, width):
        """Display the loaded game board."""
        # Display game board
        for row in range(height):
            for column in range(width):
                vehicle = grid[column][row]
                if vehicle:
                    print('%s ' % vehicle.get_name(),end=' ')
                else:
                    print('. ',end=' ')

                if column == width - 1:
                    print('\n')

    def run(self,board_file):
        """Run Application."""

        # Ask user which game board load
        # board_name = self.console_view.load_board_prompt()

        # if board_name:
            # Load game board from file
        loader = BoardLoader('./boards/%s.txt' % board_file)
        game_board = loader.get_game_board()

        # Display game board
        # self.console_view.display_loaded_grid(game_board.get_grid(), game_board.get_height(), game_board.get_width())
        self.display_grid(game_board.get_grid(), game_board.get_height(), game_board.get_width())
        # Find the solution to the game board
        start_time = time.perf_counter()
        solver = BoardSolver(game_board)
        # solution = solver.get_solution()
        solution = solver.a_star_search()

        end_time = time.perf_counter()


        # self.display_grid(game_board.get_grid(), game_board.get_height(), game_board.get_width())

        if solution:
            self.console_view.display_statistics(len(solution), end_time - start_time)
        else:
            self.console_view.display_statistics(time_delta=end_time - start_time)

        # self.console_view.display_solution(solution)

        # Exit system
        # self.console_view.display_exit_message()
        sys.exit()


if __name__ == "__main__":
    RushHourSolver("1")

