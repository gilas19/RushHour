# Define the base lists for boards and heuristics
boards = [f"{board}.txt" for board in ["1", "2", "11", "21", "39", "40"]]
adv_boards = [f"adv_{board}.txt" for board in ["sample1", "sample2", "sample3"]]
heuristics = [
    "distanceToExit",
    "blockersCount",
    "blockersTotalSize",
    "stepsToClearPath",
    "singlePlayer",
    "twoPlayers",
]


def add_experiments(experiments, board_list, algorithm, *args):
    """Adds experiment configurations to the experiment list."""
    for board in board_list:
        experiments.append([board, algorithm] + list(args))


def generate_basic_experiments(experiments):
    """Generates basic experiments for Random, BFS, and A* algorithms."""
    add_experiments(experiments, boards, "random")
    add_experiments(experiments, boards, "bfs")
    for heuristic in [h for h in heuristics if h != "twoPlayers"]:  # Exclude 'twoPlayers' heuristic
        add_experiments(experiments, boards, "astar", heuristic)


def generate_adverserial_experiments(experiments):
    """Generates adverserial experiments for RandomAdv and AlphaBeta algorithms."""
    add_experiments(
        experiments,
        adv_boards,
        "randomAdv",
        "nullHeuristic",
        "randomAdv",
        "nullHeuristic",
    )

    for heuristic in heuristics:
        add_experiments(
            experiments,
            adv_boards,
            "alphabeta",
            heuristic,
            "randomAdv",
            "nullHeuristic",
        )
        add_experiments(
            experiments,
            adv_boards,
            "randomAdv",
            "nullHeuristic",
            "alphabeta",
            heuristic,
        )

    for heuristic in [h for h in heuristics if h != "twoPlayers"]:
        add_experiments(experiments, adv_boards, "alphabeta", "twoPlayers", "alphabeta", heuristic)

    add_experiments(experiments, adv_boards, "mcts", "nullHeuristic", "randomAdv", "nullHeuristic")
    add_experiments(experiments, adv_boards, "randomAdv", "nullHeuristic", "mcts", "nullHeuristic")
    add_experiments(experiments, adv_boards, "mcts", "nullHeuristic", "alphabeta", "twoPlayers")
    add_experiments(experiments, adv_boards, "alphabeta", "twoPlayers", "mcts", "nullHeuristic")


# def custom_experiments(experiments):
#     """Generates custom experiments for the given board and algorithm."""
#     add_experiments(experiments, boards, "bfs")
#     add_experiments(experiments, boards, "astar", "singlePlayer")
#     add_experiments(experiments, adv_boards, "alphabeta", "twoPlayers", "randomAdv", "nullHeuristic")


def main():
    """Main function to run all experiment generation and save results to a file."""
    all_experiments = []
    generate_basic_experiments(all_experiments)
    generate_adverserial_experiments(all_experiments)
    # custom_experiments(all_experiments)
    with open("experiments.txt", "w") as file:
        for experiment in all_experiments:
            file.write(" ".join(experiment) + "\n")

    print("Experiments generated and saved to file.")


if __name__ == "__main__":
    main()
