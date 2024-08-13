# def two_players(board, agent):
#     player1 = board.player1_car
#     player2 = board.player2_car
#     player1_distance = board.width - player1.get_end_location()["x"] - 1
#     player2_distance = board.height - player2.get_end_location()["y"] - 1

#     if agent == 1:
#         return player2_distance - player1_distance
#     else:
#         return player1_distance - player2_distance


# def two_players(board, agent):
#     player1 = board.locate_vehicle("X")
#     player2 = board.locate_vehicle("Y")
#     player1_distance = board.width - player1["end"][1] - 1
#     player2_distance = board.height - player2["end"][0] - 1

#     if agent == 1:
#         return player2_distance - player1_distance
#     else:
#         return player1_distance - player2_distance


def distance_to_goal(board, agent):
    vehicle = "X" if agent == 1 else "Y"
    player_vehicle = board.locate_vehicle(vehicle)
    if board.get_orientation(vehicle) == "horizontal":
        return board.width - player_vehicle["end"][1] - 1
    else:
        return board.height - player_vehicle["end"][0] - 1


def count_blockers(board, player_vehicle):
    blockers = 0
    if board.get_orientation(player_vehicle) == "horizontal":
        for col in range(player_vehicle["end"][1] + 1, board.width):
            if board.grid[player_vehicle["end"][0]][col] != ".":
                blockers += 1
    else:
        for row in range(player_vehicle["end"][0] + 1, board.height):
            if board.grid[row][player_vehicle["end"][1]] != ".":
                blockers += 1
    return blockers


def two_players(board, agent):
    player1 = board.locate_vehicle("X")
    player2 = board.locate_vehicle("Y")

    player1_distance = board.width - player1["end"][1] - 1
    player2_distance = board.height - player2["end"][0] - 1

    player1_blockers = count_blockers(board, player1)
    player2_blockers = count_blockers(board, player2)

    player1_score = 1 * (10 * player1_distance + 5 * player1_blockers)
    player2_score = 1 * (10 * player2_distance + 5 * player2_blockers)

    if agent == 1:
        return player1_score + player2_score
    else:
        return player2_score + player1_score
