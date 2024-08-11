from util import Orientation


class GameBoard:
    """Represents the game board for the Rush Hour game."""

    def __init__(self, height, width):
        """Initialize the game board with specified dimensions."""
        self.height = height
        self.width = width
        self.grid = self.generate_grid()

    def generate_grid(self):
        """Generate an empty grid based on the board dimensions."""
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def get_grid(self):
        """Return the current state of the grid."""
        return self.grid

    def add_vehicle(self, vehicle, locations):
        """Place a vehicle on the board at specified locations.

        Args:
            vehicle: The vehicle object to be placed on the board.
            locations (list of dicts): A list of locations where the vehicle occupies, each location
                                       is represented as a dictionary with 'x' and 'y' keys.
        """
        for location in locations:
            x, y = location["x"], location["y"]
            if self.is_within_bounds(x, y):
                self.grid[x][y] = vehicle
            else:
                raise ValueError(f"Location ({x}, {y}) is out of bounds for the board.")

    def is_within_bounds(self, x, y):
        """Check if the given coordinates are within the bounds of the board."""
        return 0 <= x < self.height and 0 <= y < self.width

    def get_height(self):
        """Return the height of the game board."""
        return self.height

    def get_width(self):
        """Return the width of the game board."""
        return self.width


class Vehicle:
    """Represents a vehicle on the Rush Hour game board."""

    VEHICLE_COLORS = {
        "X": "red",
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
    }

    def __init__(self, name, type):
        """Initialize a vehicle with a name and type."""
        self.name = name
        self.type = type  # main, vehicle, broken_down
        self.start = {"x": None, "y": None}
        self.end = {"x": None, "y": None}
        self.color = self.VEHICLE_COLORS.get(name, "black")
        self.occupied_locations = []

    def set_start_location(self, x, y):
        """Set the start location of the vehicle."""
        self.start = {"x": x, "y": y}

    def get_start_location(self):
        """Return the start location of the vehicle."""
        return self.start

    def set_end_location(self, x, y):
        """Set the end location of the vehicle."""
        self.end = {"x": x, "y": y}

    def get_end_location(self):
        """Return the end location of the vehicle."""
        return self.end

    def get_occupied_locations(self):
        """Calculate and return the list of locations occupied by the vehicle."""
        self.occupied_locations = []

        if self.get_orientation() == Orientation.HORIZONTAL:
            self.occupied_locations = [{"x": self.start["x"] + i, "y": self.start["y"]} for i in range(self.end["x"] - self.start["x"] + 1)]
        elif self.get_orientation() == Orientation.VERTICAL:
            self.occupied_locations = [{"x": self.start["x"], "y": self.start["y"] + i} for i in range(self.end["y"] - self.start["y"] + 1)]

        return self.occupied_locations

    def get_name(self):
        """Return the name of the vehicle."""
        return self.name

    def is_main_vehicle(self):
        """Check if the vehicle is the main (red car) vehicle."""
        return self.type == "main"

    def get_orientation(self):
        """Determine and return the orientation of the vehicle."""
        if self.start["x"] == self.end["x"]:
            return Orientation.VERTICAL
        elif self.start["y"] == self.end["y"]:
            return Orientation.HORIZONTAL
        else:
            raise ValueError("Invalid vehicle position: Start and end points do not align horizontally or vertically.")

    def move_forward(self):
        """Move the vehicle one step forward."""
        if self.get_orientation() == Orientation.HORIZONTAL:
            self.start["x"] += 1
            self.end["x"] += 1
        elif self.get_orientation() == Orientation.VERTICAL:
            self.start["y"] += 1
            self.end["y"] += 1

    def move_backward(self):
        """Move the vehicle one step backward."""
        if self.get_orientation() == Orientation.HORIZONTAL:
            self.start["x"] -= 1
            self.end["x"] -= 1
        elif self.get_orientation() == Orientation.VERTICAL:
            self.start["y"] -= 1
            self.end["y"] -= 1

    def __repr__(self):
        """Return a string representation of the vehicle."""
        # return f"{self.name} - {self.start} to {self.end}"
        return self.name
