import sys
from planning.graph_plan import GraphPlan, parse_solution
from planning.rushhour import (
    parse_vehicle_list,
    create_problem_file,
    create_domain_file,
)
import time


def main(board):
    board_filename = f"boards/{board}.txt"
    domain_filename = f"planning/gp_problem_domain/{board}_domain.txt"
    problem_filename = f"planning/gp_problem_domain/{board}_problem.txt"

    with open(board_filename, "r") as file:
        content = file.read().splitlines()

    main_vehicle, horizontal_vehicles, vertical_vehicles, empty_squares = (
        parse_vehicle_list(content[1:])
    )
    create_domain_file(
        domain_filename, main_vehicle, horizontal_vehicles, vertical_vehicles
    )
    create_problem_file(
        problem_filename,
        main_vehicle,
        horizontal_vehicles,
        vertical_vehicles,
        empty_squares,
    )

    gp = GraphPlan(domain_filename, problem_filename)
    start = time.perf_counter()
    plan = gp.graph_plan()
    elapsed = time.perf_counter() - start
    if plan is not None:
        print(
            "Plan found with %d actions in %.6f seconds"
            % (len([act for act in plan if not act.is_noop()]), elapsed)
        )
        solution = parse_solution(plan)
        print(solution)
    else:
        print("Could not find a plan in %.6f seconds" % elapsed)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 graphplan.py <board>")
        sys.exit(1)

    main(sys.argv[1])
