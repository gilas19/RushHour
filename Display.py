import curses
import math
from util import Direction, Orientation
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation


class GUIView:
    """Graphical User Interface (GUI) View for visualizing the game board and moves."""

    def plot_board(self, grid, ax, move_index=None, total_moves=None, possible_moves=None):
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
        ax.set_xlim(0, len(grid[0]))
        ax.set_ylim(0, len(grid))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(True)
        ax.invert_yaxis()

        # Draw the board and vehicles
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                color = "white" if cell == 0 else cell.color if cell.type != "broken_down" else "black"
                ax.add_patch(patches.Rectangle((i, j), 1, 1, edgecolor="black", facecolor=color))

        # Draw arrows indicating possible moves
        if possible_moves:
            for state in possible_moves:
                vehicle, direction = state[0][0]
                orientation = vehicle.get_orientation()
                x_start, y_start = vehicle.start.values()
                x_end, y_end = vehicle.end.values()

                if orientation == Orientation.HORIZONTAL:
                    if direction == Direction.FORWARD:
                        arrow = patches.Arrow(x_end + 0.5, y_end + 0.5, 1, 0, facecolor="red", edgecolor="red")
                    elif direction == Direction.BACKWARD:
                        arrow = patches.Arrow(x_start + 0.5, y_start + 0.5, -1, 0, facecolor="red", edgecolor="red")

                elif orientation == Orientation.VERTICAL:
                    if direction == Direction.FORWARD:
                        arrow = patches.Arrow(x_end + 0.5, y_end + 0.5, 0, 1, facecolor="red", edgecolor="red")
                    elif direction == Direction.BACKWARD:
                        arrow = patches.Arrow(x_start + 0.5, y_start + 0.5, 0, -1, facecolor="red", edgecolor="red")

                ax.add_patch(arrow)

        # Display move count if provided
        if move_index is not None and total_moves is not None:
            ax.text(0.5, 1.05, f"Move: {move_index}/{total_moves}", transform=ax.transAxes, ha="center")

    def show_solution(self, board, grids, possible_moves=None, save_location=None):
        """Animate the solution, displaying the sequence of moves on the board.

        Args:
            board: The game board instance.
            grids (list of lists): Sequence of grid states representing each move.
            possible_moves (list of tuples, optional): Possible moves for each grid state. Defaults to None.
        """
        fig, ax = plt.subplots()

        def animate(i):
            self.plot_board(grids[i], ax, move_index=i, total_moves=len(grids) - 1, possible_moves=possible_moves[i])
            return ax

        ani = animation.FuncAnimation(fig, animate, frames=len(grids), interval=400)
        if save_location:
            ani.save(save_location, writer="pillow")
        else:
            plt.show()
            plt.clf()

    def show_board(self, board, possible_moves=None):
        """Display the current state of the board without animation.

        Args:
            board: The game board instance.
            possible_moves (list of tuples, optional): Possible moves for the current board state. Defaults to None.
        """
        fig, ax = plt.subplots()
        grid = board.get_grid()
        self.plot_board(grid, ax, possible_moves=possible_moves)
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


class ConsoleView(object):

    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.scrollok(1)
        self.stdscr.idlok(1)
        self.stdscr.syncok(1)
        curses.setupterm()

    def show_board(self, board):
        """Display the loaded game board."""
        grid, height, width = board.get_grid(), board.get_height(), board.get_width()
        # self.stdscr.clear()

        # Display game board
        self.stdscr.addstr("The Puzzle: \n", curses.A_BOLD)
        self.stdscr.addstr("\n")
        for row in range(height):
            for column in range(width):
                vehicle = grid[column][row]
                if vehicle:
                    self.stdscr.addstr("%s " % vehicle.get_name())
                else:
                    self.stdscr.addstr(". ")

                if column == width - 1:
                    self.stdscr.addstr("\n")
        self.stdscr.refresh()

    def show_statistics(self, time_delta, expanded_nodes, amount_moves="--"):
        print("\n")
        print("\n")
        print("Statistics: \n")
        print("Amount of Moves: %s \n" % amount_moves)
        print("Time Passed: %.3f seconds\n" % time_delta)
        print("Expanded Nodes: %s\n" % expanded_nodes)

    def display_solution(self, solution):
        """Display the moves to solve the puzzle."""
        print("\n")
        print("\n")

        if solution:
            # Convert moves to a user friendly format and display them
            print("The Solution: \n", curses.A_BOLD)
            print("\n")

            solution_size = len(solution)
            items_per_row = math.ceil(solution_size / 4)
            for row_index in range(items_per_row):
                collection = []
                for index in range(4):
                    limit = (index * (items_per_row + 1)) + row_index
                    if limit < solution_size:
                        collection.append(limit)

                for column_index, move in enumerate(solution[i] for i in collection):
                    vehicle = move[0]
                    direction = move[1]
                    direction_name = ""
                    if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.FORWARD:
                        direction_name = "Right"

                    if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.BACKWARD:
                        direction_name = "Left"

                    if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.FORWARD:
                        direction_name = "Down"

                    if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.BACKWARD:
                        direction_name = "Up"

                    display_text = "%02d: %s -> %s " % (collection[column_index] + 1, vehicle.get_name(), direction_name)
                    print(display_text)
                    print(" " * (20 - len(display_text)))

                    if column_index == len(collection) - 1:
                        print("\n")
        else:
            print("This puzzle is unsolvable. Even for me! :( \n")
