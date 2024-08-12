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


def two_player_heuristic(game_board, player):
    player1_distance = game_board.width - game_board.player1_car.get_end_location()["x"] - 1
    player2_distance = game_board.height - game_board.player2_car.get_end_location()["y"] - 1

    if player == 1:
        return player2_distance - player1_distance
    else:
        return player1_distance - player2_distance
