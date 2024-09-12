import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import sys


class GameBoard:
    def __init__(self, file):
        """Initializes the game board by loading from a file and extracting vehicle information."""
        with open(f"boards/{file}", "r") as f:
            rows = f.read().splitlines()
        self.grid = [list(row) for row in rows[1:]]
        self.grid_size = len(self.grid)
        self.vehicles = self._extract_vehicles()

    def _extract_vehicles(self):
        """Extracts vehicle positions, sizes, and orientations from the grid."""
        vehicles = {}
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                vehicle = self.grid[row][col]
                if vehicle not in [".", "_"]:
                    if vehicle not in vehicles:
                        vehicles[vehicle] = {
                            "start": (row, col),
                            "end": (row, col),
                            "size": 1,
                            "horizontal": None,
                        }
                    else:
                        vehicles[vehicle]["end"] = (row, col)
                        vehicles[vehicle]["size"] += 1
                        if vehicles[vehicle]["horizontal"] is None:
                            vehicles[vehicle]["horizontal"] = row == vehicles[vehicle]["start"][0]
        return vehicles

    def locate_vehicle(self, vehicle):
        """Returns the position and orientation of the specified vehicle."""
        return self.vehicles[vehicle]

    def get_orientation(self, vehicle):
        """Returns the orientation of the vehicle: 'horizontal' or 'vertical'."""
        return "horizontal" if self.vehicles[vehicle]["horizontal"] else "vertical"

    def is_opponent(self, player, vehicle):
        """Checks if the vehicle belongs to the opponent."""
        return (player == "X" and vehicle == "Y") or (player == "Y" and vehicle == "X")

    def move(self, vehicle, direction, steps=1, player="X"):
        """Moves the specified vehicle in the given direction."""
        for _ in range(steps):
            location = self.locate_vehicle(vehicle)
            start, end = location["start"], location["end"]
            if self.get_orientation(vehicle) == "horizontal":
                self._move_horizontal(vehicle, start, end, direction)
            else:
                self._move_vertical(vehicle, start, end, direction)

    def _move_horizontal(self, vehicle, start, end, direction):
        """Handles the horizontal movement of the vehicle."""
        if direction == "LEFT":
            self.grid[start[0]][start[1] - 1] = vehicle
            self.grid[end[0]][end[1]] = "."
            self.vehicles[vehicle]["start"] = (start[0], start[1] - 1)
            self.vehicles[vehicle]["end"] = (end[0], end[1] - 1)
        elif direction == "RIGHT":
            self.grid[end[0]][end[1] + 1] = vehicle
            self.grid[start[0]][start[1]] = "."
            self.vehicles[vehicle]["start"] = (start[0], start[1] + 1)
            self.vehicles[vehicle]["end"] = (end[0], end[1] + 1)

    def _move_vertical(self, vehicle, start, end, direction):
        """Handles the vertical movement of the vehicle."""
        if direction == "UP":
            self.grid[start[0] - 1][start[1]] = vehicle
            self.grid[end[0]][end[1]] = "."
            self.vehicles[vehicle]["start"] = (start[0] - 1, start[1])
            self.vehicles[vehicle]["end"] = (end[0] - 1, end[1])
        elif direction == "DOWN":
            self.grid[end[0] + 1][end[1]] = vehicle
            self.grid[start[0]][start[1]] = "."
            self.vehicles[vehicle]["start"] = (start[0] + 1, start[1])
            self.vehicles[vehicle]["end"] = (end[0] + 1, end[1])

    def get_legal_actions(self, player="X"):
        """Returns a list of all legal actions (vehicle, direction) available for the player."""
        actions = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                vehicle = self.grid[row][col]
                if vehicle != "." and not self.is_opponent(player, vehicle):
                    self._add_horizontal_actions(vehicle, row, col, actions)
                    self._add_vertical_actions(vehicle, row, col, actions)
        return actions

    def _add_horizontal_actions(self, vehicle, row, col, actions):
        """Adds legal horizontal moves for the given vehicle."""
        if self.get_orientation(vehicle) == "horizontal":
            if col > 0 and self.grid[row][col - 1] == ".":
                actions.append((vehicle, "LEFT", 1))
            if col + 1 < self.grid_size and self.grid[row][col + 1] == ".":
                actions.append((vehicle, "RIGHT", 1))

    def _add_vertical_actions(self, vehicle, row, col, actions):
        """Adds legal vertical moves for the given vehicle."""
        if self.get_orientation(vehicle) == "vertical":
            if row > 0 and self.grid[row - 1][col] == ".":
                actions.append((vehicle, "UP", 1))
            if row + 1 < self.grid_size and self.grid[row + 1][col] == ".":
                actions.append((vehicle, "DOWN", 1))

    def print_board(self):
        for row in self.grid:
            print(" ".join(row))
        print()


class GUIView:
    """Graphical User Interface (GUI) View for visualizing the game board and moves."""

    VEHICLE_COLORS = {
        "X": "red",
        "Y": "blue",
        "A": "yellowgreen",
        "B": "gold",
        "C": "mediumpurple",
        "D": "pink",
        "E": "purple",
        "F": "turquoise",
        "G": "gray",
        "H": "tan",
        "I": "yellow",
        "J": "silver",
        "K": "white",
        "O": "orange",
        "P": "pink",
        "Q": "black",
        "R": "green",
        ".": "white",
    }

    def plot_board(
        self,
        board,
        ax,
        move=None,
        move_index=None,
        total_moves=None,
        possible_moves=False,
        two_players=False,
    ):
        self._setup_board(ax, board.grid_size)
        self._apply_move(board, move, ax, two_players)

        # Draw vehicles and exit
        red_car_row, blue_car_col = self._draw_vehicles(board, ax)
        self._draw_exit(ax, board.grid_size, red_car_row, blue_car_col, two_players)

        # Show possible moves
        if possible_moves:
            self._draw_possible_moves(ax, board, (move[3] if move else "X"))

        # Display move information
        if move_index is not None and total_moves is not None:
            if two_players:
                ax.text(
                    0.2,
                    1.05,
                    f"Move: {move_index}/{total_moves}",
                    transform=ax.transAxes,
                    ha="left",
                )
            else:
                ax.text(
                    0.5,
                    1.05,
                    f"Move: {move_index}/{total_moves}",
                    transform=ax.transAxes,
                    ha="center",
                )

    def _setup_board(self, ax, grid_size):
        """Initializes the board layout."""
        ax.clear()
        ax.set_xlim(0, grid_size)
        ax.set_ylim(0, grid_size)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(True)
        ax.invert_yaxis()

    def _apply_move(self, board, move, ax, two_players):
        """Executes the move and displays the current player's turn."""
        if move is not None:
            board.move(*move)
            if two_players:
                player = "Player 1's Turn" if move[3] == "X" else "Player 2's Turn"
                color = "red" if move[3] == "X" else "blue"
                ax.text(0.8, 1.05, player, transform=ax.transAxes, ha="right", color=color)

    def _draw_vehicles(self, board, ax):
        """Draws the vehicles on the board and returns the red and blue car positions."""
        red_car_row, blue_car_col = None, None
        for i, row in enumerate(board.grid):
            for j, cell in enumerate(row):
                color = self.VEHICLE_COLORS.get(cell, "white")
                ax.add_patch(patches.Rectangle((j, i), 1, 1, edgecolor="black", facecolor=color))
                if color == "red":
                    red_car_row = i
                if color == "blue":
                    blue_car_col = j
        return red_car_row, blue_car_col

    def _draw_exit(self, ax, grid_size, red_car_row, blue_car_col, two_players):
        """Draws the exit for both players if applicable."""
        exit_x, exit_y = grid_size - 1, red_car_row
        ax.text(
            exit_x + 1.15,
            exit_y + 0.5,
            "EXIT",
            ha="center",
            va="center",
            fontsize=12,
            color="red",
            fontweight="bold",
            rotation=90,
        )

        if two_players and blue_car_col is not None:
            ax.text(
                blue_car_col + 0.5,
                grid_size + 0.2,
                "EXIT",
                ha="center",
                va="center",
                fontsize=12,
                color="blue",
                fontweight="bold",
            )

    def _draw_possible_moves(self, ax, board, player):
        """Draws arrows indicating possible moves."""
        for vehicle, direction, _ in board.get_legal_actions(player):
            orientation = board.get_orientation(vehicle)
            vehicle_coords = board.locate_vehicle(vehicle)
            self._draw_arrow(ax, vehicle_coords, orientation, direction)

    def _draw_arrow(self, ax, vehicle_coords, orientation, direction):
        """Draws an arrow for a move."""
        start_x, start_y = vehicle_coords["start"]
        end_x, end_y = vehicle_coords["end"]

        if orientation == "horizontal":
            if direction == "LEFT":
                arrow = patches.FancyArrowPatch(
                    (start_y, start_x + 0.5),
                    (start_y - 1, start_x + 0.5),
                    mutation_scale=10,
                    color="black",
                )
            else:
                arrow = patches.FancyArrowPatch(
                    (end_y + 1, end_x + 0.5),
                    (end_y + 2, end_x + 0.5),
                    mutation_scale=10,
                    color="black",
                )
        else:
            if direction == "UP":
                arrow = patches.FancyArrowPatch(
                    (start_y + 0.5, start_x),
                    (start_y + 0.5, start_x - 1),
                    mutation_scale=10,
                    color="black",
                )
            else:
                arrow = patches.FancyArrowPatch(
                    (end_y + 0.5, end_x + 1),
                    (end_y + 0.5, end_x + 2),
                    mutation_scale=10,
                    color="black",
                )

        ax.add_patch(arrow)

    def animate_solution(
        self,
        board,
        solution,
        possible_moves=None,
        two_players=False,
        save_path=None,
        fps=2,
    ):
        def init_func():
            self.plot_board(
                board,
                ax,
                move_index=0,
                total_moves=len(solution),
                possible_moves=True,
                two_players=two_players,
            )
            board.print_board()

        def animate(i):
            self.plot_board(
                board,
                ax,
                move=solution[i],
                move_index=i,
                total_moves=len(solution) - 1,
                possible_moves=True,
                two_players=two_players,
            )
            return ax

        fig, ax = plt.subplots()
        solution.insert(0, None)
        ani = animation.FuncAnimation(fig, animate, frames=len(solution), interval=100, repeat=False)

        if save_path:
            ani.save(save_path, writer="pillow", fps=fps)
        else:
            plt.show()
        plt.clf()

    def show_board(self, board, possible_moves=False):
        fig, ax = plt.subplots()
        self.plot_board(board, ax, possible_moves=possible_moves)
        plt.show()
        plt.clf()

    def load_solution(self, solution_path):
        """Load the solution from a file."""
        with open(solution_path, "r") as f:
            return eval(f.read())


# display = GUIView()
# solution = display.load_solution("results/solutions/1_bfs_solution.txt")
# board = GameBoard("1.txt")
# display.animate_solution(board, solution, save_path="results/figures/1_bfs_solution.gif")

# display = GUIView()
# solution = display.load_solution("results/solutions/adv_sample2_mcts_nullHeuristic_randomAdv_nullHeuristic_solution.txt")
# board = GameBoard("adv_sample2.txt")
# display.animate_solution(board, solution, save_path="results/figures/adv_sample2_mcts_nullHeuristic_randomAdv_nullHeuristic_solution.gif", two_players=True)


def main(solution_filename: str) -> None:
    def animate_solution(
        view: GUIView,
        board: GameBoard,
        solution_file: str,
        output_file: str,
        two_players: bool = False,
    ) -> None:
        solution = view.load_solution(solution_file)
        view.animate_solution(board, solution, save_path=output_file, two_players=two_players)

    view = GUIView()
    solution_name = solution_filename.split(".")[0]
    solution_parts = solution_name.split("_")

    if solution_parts[0] == "adv":
        board_file = f"adv_{solution_parts[1]}.txt"
        board = GameBoard(board_file)
        animate_solution(
            view,
            board,
            f"results/solutions/{solution_name}.txt",
            f"results/figures/{solution_name}.gif",
            two_players=True,
        )
    else:
        board_file = f"{solution_parts[0]}.txt"
        board = GameBoard(board_file)
        animate_solution(
            view,
            board,
            f"results/solutions/{solution_name}.txt",
            f"results/figures/{solution_name}.gif",
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <solution_filename>")
        sys.exit(1)

    main(sys.argv[1])


if __name__ == "__main__":
    view = GUIView()
    solution_filename = sys.argv[1].split(".")[0]
    solution_splitted = solution_filename.split("_")
    if solution_splitted[0] == "adv":
        board = GameBoard("adv_" + solution_splitted[1] + ".txt")
        view.animate_solution(
            board,
            view.load_solution("results/solutions/" + solution_filename + ".txt"),
            save_path=f"results/figures/{solution_filename}.gif",
            two_players=True,
        )
    else:
        board = GameBoard(solution_filename.split("_")[0] + ".txt")
        view.animate_solution(
            board,
            view.load_solution("results/solutions/" + solution_filename + ".txt"),
            save_path=f"results/figures/{solution_filename}.gif",
        )
