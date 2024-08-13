def distance_and_blocking(grid, height, width):
    num_vehicles = 0
    main_vehicle = None
    for row in range(height):
        for column in range(width):
            vehicle = grid[column][row]

            if vehicle and vehicle.is_main_vehicle():
                main_vehicle = (row, column)

    for column in range(main_vehicle[1], width):
        vehicle = grid[column][main_vehicle[0]]
        if vehicle and not vehicle.is_main_vehicle():
            num_vehicles += 1

    # print("num_vehicles" , num_vehicles)
    return num_vehicles + (width - main_vehicle[1] - 1)


def distance(grid, height, width):
    main_vehicle = None
    for row in range(height):
        for column in range(width):
            vehicle = grid[column][row]

            if vehicle and vehicle.is_main_vehicle():
                main_vehicle = (row, column)

    return width - main_vehicle[1] - 1


def blocking(grid, height, width):
    num_vehicles = 0
    main_vehicle = None
    for row in range(height):
        for column in range(width):
            vehicle = grid[column][row]

            if vehicle and vehicle.is_main_vehicle():
                main_vehicle = (row, column)

    for column in range(main_vehicle[1], width):
        vehicle = grid[column][main_vehicle[0]]
        if vehicle and not vehicle.is_main_vehicle():
            num_vehicles += 1

    # print("num_vehicles" , num_vehicles)
    return num_vehicles


def null(grid, height, width):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

    # def two_player_heuristic(game_board, player):
    #     player1_distance = game_board.width - game_board.player1_car.get_end_location()["x"] - 1
    #     player2_distance = game_board.height - game_board.player2_car.get_end_location()["y"] - 1

    #     if player == 1:
    #         return player2_distance - player1_distance
    #     else:
    #         return player1_distance - player2_distance


# def find_vehicle(grid, name):
#     for row in grid:
#         for vehicle in row:
#             if vehicle and vehicle.get_name() == name:
#                 return vehicle


# def two_players(grid, player):
#     player1 = find_vehicle(grid, "X")
#     player2 = find_vehicle(grid, "Y")
#     player1_distance = len(grid[0]) - player1.end["x"] - 1
#     player2_distance = len(grid) - player2.end["y"] - 1

#     if player == 1:
#         return player2_distance - player1_distance
#     else:
#         return player1_distance - player2_distance
# if player == 1:
#     return len(grid[0]) - find_vehicle(grid, "X").end["x"] - 1
# else:
#     return len(grid) - find_vehicle(grid, "Y").end["y"] - 1


def two_players(board, agent):
    player1 = board.player1_car
    player2 = board.player2_car
    player1_distance = board.width - player1.get_end_location()["x"] - 1
    player2_distance = board.height - player2.get_end_location()["y"] - 1

    if agent == 1:
        return player2_distance - player1_distance
    else:
        return player1_distance - player2_distance
