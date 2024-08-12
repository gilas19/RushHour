from util import Orientation, Direction
from copy import deepcopy


class GameBoard:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = self.generate_grid()
        self.player1_car = None
        self.player2_car = None

    def __deepcopy__(self, memo):
        new_board = GameBoard(self.height, self.width)
        new_board.grid = deepcopy(self.grid)
        new_board.player1_car = deepcopy(self.player1_car)
        new_board.player2_car = deepcopy(self.player2_car)
        return new_board

    def generate_grid(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def get_grid(self):
        return self.grid

    def add_vehicle(self, vehicle, locations):
        for location in locations:
            x, y = location["x"], location["y"]
            if self.is_within_bounds(x, y):
                self.grid[y][x] = vehicle
            else:
                raise ValueError(f"Location ({x}, {y}) is out of bounds for the board.")

    def add_player_car(self, vehicle, player):
        if player == 1:
            self.player1_car = vehicle
        elif player == 2:
            self.player2_car = vehicle
        self.add_vehicle(vehicle, vehicle.get_occupied_locations())

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def is_game_over(self):
        return self.is_player_won(1) or self.is_player_won(2)

    def is_player_won(self, player):
        if player == 1:
            return self.player1_car.get_end_location()["x"] == self.width - 1
        elif player == 2:
            return self.player2_car.get_end_location()["y"] == self.height - 1
        return False

    def move_vehicle(self, vehicle, direction):
        old_locations = vehicle.get_occupied_locations()
        if direction == Direction.FORWARD:
            vehicle.move_forward()
        elif direction == Direction.BACKWARD:
            vehicle.move_backward()
        new_locations = vehicle.get_occupied_locations()

        for loc in old_locations:
            self.grid[loc["y"]][loc["x"]] = 0
        for loc in new_locations:
            self.grid[loc["y"]][loc["x"]] = vehicle


class Vehicle:
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
    }

    def __init__(self, name, type, start={"x": None, "y": None}, end={"x": None, "y": None}):
        self.name = name
        self.type = type
        self.start = start
        self.end = end
        self.color = self.VEHICLE_COLORS.get(name, "black")

    def __deepcopy__(self, memo):
        return Vehicle(self.name, self.type, deepcopy(self.start), deepcopy(self.end))

    def set_start_location(self, x, y):
        self.start = {"x": x, "y": y}

    def get_start_location(self):
        return self.start

    def set_end_location(self, x, y):
        self.end = {"x": x, "y": y}

    def get_end_location(self):
        return self.end

    def get_occupied_locations(self):
        occupied_locations = []
        if self.get_orientation() == Orientation.HORIZONTAL:
            occupied_locations = [{"x": self.start["x"] + i, "y": self.start["y"]} for i in range(self.end["x"] - self.start["x"] + 1)]
        elif self.get_orientation() == Orientation.VERTICAL:
            occupied_locations = [{"x": self.start["x"], "y": self.start["y"] + i} for i in range(self.end["y"] - self.start["y"] + 1)]
        return occupied_locations

    def get_name(self):
        return self.name

    def is_player_car(self):
        return self.type in ["player1_car", "player2_car"]

    def is_opponent_vehicle(self, player):
        if player == 1:
            return self.type == "player2_car"
        elif player == 2:
            return self.type == "player1_car"
        return False

    def get_orientation(self):
        if self.start["x"] == self.end["x"]:
            return Orientation.VERTICAL
        elif self.start["y"] == self.end["y"]:
            return Orientation.HORIZONTAL
        else:
            raise ValueError("Invalid vehicle position: Start and end points do not align horizontally or vertically.")

    def move_forward(self):
        if self.get_orientation() == Orientation.HORIZONTAL:
            self.start["x"] += 1
            self.end["x"] += 1
        elif self.get_orientation() == Orientation.VERTICAL:
            self.start["y"] += 1
            self.end["y"] += 1

    def move_backward(self):
        if self.get_orientation() == Orientation.HORIZONTAL:
            self.start["x"] -= 1
            self.end["x"] -= 1
        elif self.get_orientation() == Orientation.VERTICAL:
            self.start["y"] -= 1
            self.end["y"] -= 1

    def __repr__(self):
        return self.name
