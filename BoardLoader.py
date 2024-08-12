import re
from BoardObjects import GameBoard, Vehicle

class BoardLoader:
    @staticmethod
    def load(filename):
        content = BoardLoader.read(filename)
        BoardLoader.validate(content)
        return BoardLoader.parse_to_objects(content)

    @staticmethod
    def read(filename):
        try:
            with open(filename, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found! Please provide the correct file location.")

    @staticmethod
    def parse_to_objects(content):
        vehicles = {}
        for row_index, line in enumerate(content):
            for column_index, letter in enumerate(line):
                vehicle_type = BoardLoader.determine_vehicle_type(letter)
                if vehicle_type:
                    if letter not in vehicles:
                        vehicle = Vehicle(name=letter, type=vehicle_type)
                        vehicle.set_start_location(column_index, row_index)
                        vehicles[letter] = vehicle
                    else:
                        vehicle = vehicles[letter]
                        vehicle.set_end_location(column_index, row_index)

        return BoardLoader.initialize_game_board(content, vehicles)

    @staticmethod
    def determine_vehicle_type(letter):
        if letter == "X":
            return "player1_car"
        elif letter == "Y":
            return "player2_car"
        elif letter.isupper():
            return "vehicle"
        elif letter.islower():
            return "broken_down"
        return None

    @staticmethod
    def initialize_game_board(content, vehicles):
        board_width = len(content[0])
        board_height = len(content)
        game_board = GameBoard(board_height, board_width)
        for vehicle in sorted(vehicles.values(), key=lambda v: v.name):
            locations = vehicle.get_occupied_locations()
            if vehicle.type == "player1_car":
                game_board.add_player_car(vehicle, 1)
            elif vehicle.type == "player2_car":
                game_board.add_player_car(vehicle, 2)
            else:
                game_board.add_vehicle(vehicle, locations)
        return game_board

    @staticmethod
    def validate(content):
        if not content:
            raise ValueError("The file is empty! Please select a file with the correct data format.")

        line_length = len(content[0])
        player1_car_size = 0
        player2_car_size = 0

        for line in content:
            if len(line) != line_length:
                raise ValueError("The data format is incorrect! All text lines must be the same length.")
            if re.sub(r"[A-Za-z.]+", "", line):
                raise ValueError("The data format is incorrect! Only letters and '.' are allowed.")
            if "X" in line:
                player1_car_size += 1
            if "Y" in line:
                player2_car_size += 1

        if player1_car_size == 0 or player2_car_size == 0:
            raise ValueError("The data format is incorrect! Both player cars (X and Y) must be present.")