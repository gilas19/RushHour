def create_move(car_name, direction, old_start_x, old_start_y, new_end_x, new_end_y):
    name = "%s_Move_%s_To_%s_%s" % (car_name, direction, new_end_x, new_end_y)

    if direction == "right":
        opp_dir = "left"
        new_start_x = old_start_x + 1
        new_start_y = old_start_y
        old_end_x = new_end_x - 1
        old_end_y = new_end_y

    elif direction == "left":
        opp_dir = "right"
        new_start_x = old_start_x - 1
        new_start_y = old_start_y
        old_end_x = new_end_x + 1
        old_end_y = new_end_y

    elif direction == "up":
        opp_dir = "down"
        new_start_x = old_start_x
        new_start_y = old_start_y - 1
        old_end_x = new_end_x
        old_end_y = new_end_y + 1

    elif direction == "down":
        opp_dir = "up"
        new_start_x = old_start_x
        new_start_y = old_start_y + 1
        old_end_x = new_end_x
        old_end_y = new_end_y - 1

    pre = [
        f"{new_end_x}_{new_end_y}_empty",
        f"{car_name}_{direction}_{old_end_x}_{old_end_y}",
    ]

    add = [
        f"{old_start_x}_{old_start_y}_empty",
        f"{car_name}_{direction}_{new_end_x}_{new_end_y}",
        f"{car_name}_{opp_dir}_{new_start_x}_{new_start_y}",
    ]

    dell = [
        f"{new_end_x}_{new_end_y}_empty",
        f"{car_name}_{direction}_{old_end_x}_{old_end_y}",
        f"{car_name}_{opp_dir}_{old_start_x}_{old_start_y}",
    ]

    return "\n".join(
        [
            "Name: " + name,
            "pre: " + " ".join(pre),
            "add: " + " ".join(add),
            "del: " + " ".join(dell),
        ]
    )


def parse_vehicle_list(content):
    # parse vehicle list from problem file
    # update main_vehicle, horizontal_vehicles and vertical_vehicles

    main_vehicle = [[-1, -1], [-1, -1]]  # (left(x,y), right(x,y))
    horizontal_vehicles = []  # (name, left(x,y), right(x,y)) name = h0
    vertical_vehicles = []  # (name, up(x,y), bottom(x,y)) name = v0
    empty_squares = []
    vehicles = dict()  # letter : (start(x,y) , end(x,y))

    # parse board into list of vehicles
    for row_index, line in enumerate(content):
        for column_index, letter in enumerate(line):
            vehicle_type = letter if letter.isupper() else None
            if vehicle_type:
                if vehicle_type == "X":
                    if main_vehicle[0][0] == -1:
                        main_vehicle[0] = [column_index, row_index]
                    main_vehicle[1] = [column_index, row_index]
                    continue
                if letter not in vehicles.keys():
                    # set start location
                    vehicles[letter] = (
                        column_index,
                        row_index,
                        column_index,
                        row_index,
                    )
                else:
                    # update end location
                    vehicles[letter] = (
                        vehicles[letter][0],
                        vehicles[letter][1],
                        column_index,
                        row_index,
                    )
            else:
                empty_squares.append((column_index, row_index))

    # parse vehicle list into categories
    for letter in vehicles:
        startX, startY, endX, endY = vehicles[letter]
        if startX == endX:
            vertical_vehicles.append((letter, (startX, startY), (endX, endY)))
        elif startY == endY:
            horizontal_vehicles.append((letter, (startX, startY), (endX, endY)))

    return main_vehicle, horizontal_vehicles, vertical_vehicles, empty_squares


def create_propositions(
    main_vehicle, horizontal_vehicles, vertical_vehicles, height, width
):
    propositions = []
    actions = []

    # empty squares propositions
    for x in range(width):
        for y in range(height):
            propositions.append(f"{x}_{y}_empty")

    # horizontal vehicles propositions
    for car, (leftX, leftY), (rightX, rightY) in horizontal_vehicles:
        length = rightX - leftX + 1
        left = 0
        right = length - 1
        while (left + length) < (width + 1):
            propositions.append(f"{car}_left_{left}_{leftY}")
            propositions.append(f"{car}_right_{right}_{rightY}")

            if right < width - 1:
                actions.append(create_move(car, "right", left, leftY, right + 1, leftY))

            if left > 0:
                actions.append(create_move(car, "left", right, leftY, left - 1, leftY))

            left += 1
            right += 1

    # vertical vehicles propositions
    for car, (topX, topY), (bottomX, bottomY) in vertical_vehicles:
        length = bottomY - topY + 1
        top = 0
        bottom = length - 1
        while (top + length) < (height + 1):
            propositions.append(f"{car}_up_{topX}_{top}")
            propositions.append(f"{car}_down_{bottomX}_{bottom}")

            if bottom < height - 1:
                actions.append(create_move(car, "down", topX, top, topX, bottom + 1))

            if top > 0:
                actions.append(create_move(car, "up", topX, bottom, topX, top - 1))

            top += 1
            bottom += 1

    # main_vehicle propositions
    main_length = int(float(main_vehicle[1][0])) - int(float(main_vehicle[0][0])) + 1
    main_y = main_vehicle[0][1]
    main_left = 0
    main_right = main_length - 1
    while (main_left + main_length) < (width + 1):
        propositions.append(f"X_left_{main_left}_{main_y}")
        propositions.append(f"X_right_{main_right}_{main_y}")

        if main_right < width - 1:
            actions.append(
                create_move("X", "right", main_left, main_y, main_right + 1, main_y)
            )

        if main_left > 0:
            actions.append(
                create_move("X", "left", main_right, main_y, main_left - 1, main_y)
            )

        main_left += 1
        main_right += 1

    return propositions, actions


def create_domain_file(
    domain_file_name,
    main_vehicle,
    horizontal_vehicles,
    vertical_vehicles,
    height=6,
    width=6,
):
    propositions, actions = create_propositions(
        main_vehicle, horizontal_vehicles, vertical_vehicles, height, width
    )
    with open(domain_file_name, "w") as domain_file:
        domain_file.write("Propositions:\n" + " ".join(propositions))
        domain_file.write("\nActions:\n" + "\n".join(actions))


def create_problem_file(
    problem_file_name,
    main_vehicle,
    horizontal_vehicles,
    vertical_vehicles,
    empty_squares,
    height=6,
    width=6,
):
    initial_state = []
    goal_state = []

    # add empty spots for all non occupied spots
    for x, y in empty_squares:
        initial_state.append(f"{x}_{y}_empty")

    # horizontal vehicles propositions
    for car, (leftX, leftY), (rightX, rightY) in horizontal_vehicles:
        initial_state.append(f"{car}_left_{leftX}_{leftY}")
        initial_state.append(f"{car}_right_{rightX}_{rightY}")

    # vertical vehicles propositions
    for car, (topX, topY), (bottomX, bottomY) in vertical_vehicles:
        initial_state.append(f"{car}_up_{topX}_{topY}")
        initial_state.append(f"{car}_down_{bottomX}_{bottomY}")

    # main_vehicle propositions
    initial_state.append(f"X_left_{main_vehicle[0][0]}_{main_vehicle[0][1]}")
    initial_state.append(f"X_right_{main_vehicle[1][0]}_{main_vehicle[1][1]}")

    goal_state.append(f"X_right_{width - 1}_{main_vehicle[1][1]}")

    with open(problem_file_name, "w") as problem_file:
        problem_file.write("Initial State: " + " ".join(initial_state))
        problem_file.write("\nGoal State: " + " ".join(goal_state))
