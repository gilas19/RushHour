import curses
import math
from util import Direction, Orientation
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation


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
    "Q": "blue",
    "R": "green",
    ".": "white",
}

SHOW_POSSIBLE_MOVES = True


class GUIView:
    """Graphical User Interface (GUI) View for visualizing the game board and moves."""

    def plot_board(self, board, move, ax, move_index=None, total_moves=None, possible_moves=None):
        """Render the current state of the board, including vehicle positions and possible moves.

        Args:
            grid (list of lists): 2D list representing the game board.
            ax (matplotlib.axes.Axes): Matplotlib axes object to draw the board on.
            move_index (int, optional): The index of the current move. Defaults to None.
            total_moves (int, optional): The total number of moves in the solution. Defaults to None.
            possible_moves (list of tuples, optional): List of possible moves. Each move is a tuple
                                                       containing vehicle information and direction. Defaults to None.
        """
        ax.clear()
        ax.set_xlim(0, board.width)
        ax.set_ylim(0, board.height)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(True)
        ax.invert_yaxis()

        print(move)
        board.move(*move)

        # Draw the board and vehicles
        for i, row in enumerate(board.grid):
            for j, cell in enumerate(row):
                color = "white" if cell == 0 else VEHICLE_COLORS[cell]
                ax.add_patch(patches.Rectangle((j, i), 1, 1, edgecolor="black", facecolor=color))

        # Draw arrows indicating possible moves
        if SHOW_POSSIBLE_MOVES:
            for state in board.get_legal_actions():
                vehicle, direction = state
                orientation = board.get_orientation(vehicle)
                vehicle = board.locate_vehicle(vehicle)
                start_x, start_y = vehicle["start"]
                end_x, end_y = vehicle["end"]
                if orientation == "horizontal":
                    if direction == "left":
                        arrow = patches.FancyArrowPatch(
                            (vehicle["start"][1], vehicle["start"][0] + 0.5),
                            (vehicle["start"][1] - 1, vehicle["start"][0] + 0.5),
                            mutation_scale=10,
                            color="black",
                        )
                    else:
                        arrow = patches.FancyArrowPatch(
                            (vehicle["end"][1] + 1, vehicle["end"][0] + 0.5),
                            (vehicle["end"][1] + 2, vehicle["end"][0] + 0.5),
                            mutation_scale=10,
                            color="black",
                        )
                else:
                    if direction == "up":
                        arrow = patches.FancyArrowPatch(
                            (vehicle["start"][1] + 0.5, vehicle["start"][0]),
                            (vehicle["start"][1] + 0.5, vehicle["start"][0] - 1),
                            mutation_scale=10,
                            color="black",
                        )
                    else:
                        arrow = patches.FancyArrowPatch(
                            (vehicle["end"][1] + 0.5, vehicle["end"][0] + 1),
                            (vehicle["end"][1] + 0.5, vehicle["end"][0] + 2),
                            mutation_scale=10,
                            color="black",
                        )

                ax.add_patch(arrow)

        # Display move count if provided
        if move_index is not None and total_moves is not None:
            ax.text(0.5, 1.05, f"Move: {move_index}/{total_moves}", transform=ax.transAxes, ha="center")

    def animate_solution(self, board, solution, possible_moves=None):
        """Animate the solution, displaying the sequence of moves on the board.

        Args:
            board: The game board instance.
            grids (list of lists): Sequence of grid states representing each move.
            possible_moves (list of tuples, optional): Possible moves for each grid state. Defaults to None.
        """
        fig, ax = plt.subplots()

        def animate(i):
            self.plot_board(board, solution[i], ax, move_index=i, total_moves=len(solution))
            return ax

        ani = animation.FuncAnimation(fig, animate, frames=len(solution), interval=1000, repeat=False, init_func=lambda: None)
        plt.show()
        plt.clf()

    def show_board(self, board, possible_moves=None):
        """Display the current state of the board without animation.

        Args:
            board: The game board instance.
            possible_moves (list of tuples, optional): Possible moves for the current board state. Defaults to None.
        """
        fig, ax = plt.subplots()
        self.plot_board(board, ax, possible_moves=board.get_legal_actions())
        plt.show()
        plt.clf()

    def show_statistics(self, time_delta, expanded_nodes, num_moves="--"):
        """Display statistical information after the solution is computed.

        Args:
            time_delta (float): Time taken to compute the solution.
            expanded_nodes (int): Number of nodes expanded during the search.
            num_moves (int or str, optional): Number of moves in the solution. Defaults to "--".
        """
        print("\n\nStatistics:\n")
        print(f"Amount of Moves: {num_moves}\n")
        print(f"Time Passed: {time_delta:.3f} seconds\n")
        print(f"Expanded Nodes: {expanded_nodes}\n")
