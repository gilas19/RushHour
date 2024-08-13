from collections import defaultdict
import re
import numpy as np
from copy import deepcopy


class GameBoard:
    def __init__(self, file="beginner", grid=None):
        if grid is None:
            self.grid = self.load(file)
        else:
            self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        # self.vehicles = self.get_vehicles()

    def load(self, file):
        with open(f"boards/{file}.txt", "r") as f:
            grid = f.read().splitlines()
            # return np.array([list(row) for row in grid])
            return [list(row) for row in grid]

    def get_vehicles(self):
        vehicles = {}
        for row in range(self.height):
            for col in range(self.width):
                vehicle = self.grid[row][col]
                if self.grid[row][col] != ".":
                    if self.grid[row][col] not in vehicles:
                        vehicles[vehicle] = {"start": (row, col), "end": (row, col)}
                    else:
                        vehicles[vehicle]["end"] = (row, col)
        return vehicles

    # def locate_vehicle(self, vehicle):
    #     return self.vehicles[vehicle]

    def locate_vehicle(self, vehicle):
        location = {"start": (-1, -1), "end": (-1, -1)}
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == vehicle:
                    if location["start"] == (-1, -1):
                        location["start"] = (row, col)
                    else:
                        location["end"] = (row, col)
        return location

    def get_orientation(self, vehicle):
        location = self.locate_vehicle(vehicle)
        if location["start"][0] == location["end"][0]:
            return "horizontal"
        else:
            return "vertical"

    def move(self, vehicle, direction):
        location = self.locate_vehicle(vehicle)
        start, end = location["start"], location["end"]
        if self.get_orientation(vehicle) == "horizontal":
            if direction == "left":
                self.grid[start[0]][start[1] - 1] = vehicle
                self.grid[end[0]][end[1]] = "."
            elif direction == "right":
                self.grid[end[0]][end[1] + 1] = vehicle
                self.grid[start[0]][start[1]] = "."
        else:
            if direction == "up":
                self.grid[start[0] - 1][start[1]] = vehicle
                self.grid[end[0]][end[1]] = "."
            elif direction == "down":
                self.grid[end[0] + 1][end[1]] = vehicle
                self.grid[start[0]][start[1]] = "."

    def is_solved(self):
        if "X" in [row[-1] for row in self.grid] or "Y" in self.grid[-1]:
            return True
        return False

    def get_legal_actions(self, player=1):
        actions = []
        for row in range(self.height):
            for col in range(self.width):
                vehicle = self.grid[row][col]
                if vehicle != "." and not self.is_opponent(player, vehicle):
                    if self.get_orientation(vehicle) == "horizontal":
                        if col > 0 and self.grid[row][col - 1] == ".":
                            actions.append((vehicle, "left"))
                        if col < self.width - 1 and self.grid[row][col + 1] == ".":
                            actions.append((vehicle, "right"))
                    else:
                        if row > 0 and self.grid[row - 1][col] == ".":
                            actions.append((vehicle, "up"))
                        if row < self.height - 1 and self.grid[row + 1][col] == ".":
                            actions.append((vehicle, "down"))
        return actions

    def generate_successor(self, vehicle, action):
        new_board = GameBoard(grid=deepcopy(self.grid))
        new_board.move(vehicle, action)
        return new_board

    def display(self):
        for row in self.grid:
            print(" ".join(cell for cell in row))
        print()

    def is_opponent(self, player, vehicle):
        if player == 1:
            return vehicle == "Y"
        else:
            return vehicle == "X"

    def get_possible_moves(self, player):
        actions = self.get_legal_actions(player)
        return [([(vehicle, action)], self.generate_successor(vehicle, action)) for vehicle, action in actions]
