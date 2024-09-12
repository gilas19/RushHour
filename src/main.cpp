// main.cpp

#include "Board.h"
#include "SearchAlgorithms.h"
#include <iostream>
#include <fstream>
#include <map>
#include "Heuristics.h"
#include <string>
#include <ctime>
#include "SearchResult.h"

#define RESULTS_DIR "../results/"
#define SOLUTIONS_DIR "../results/solutions/"
#define RESULTS_FILE "../results/results.csv"
#define EXPERIMENTS_FILE "../experiments.txt"


int run_experiment(char* argv[], bool printBoard = false) {
    Board board(argv[1]);
    if (board.gridSize == 0) {
        return 1;
    }
    if (printBoard) {
        board.printBoard();
    }
    SearchResult result(argv[1], argv[2]);
    std::string algorithm = argv[2];
    if (algorithm == "random") {
        result.printHeader();
        SearchAlgorithms::Random(board, Player::HORIZONTAL, result);
    }
    else if (algorithm == "bfs") {
        result.printHeader();
        SearchAlgorithms::BFS(board, result);
    }
    else if (algorithm == "astar") {
        result.heuristic = argv[3];
        HeuristicFunc heuristic = Heuristics::factory(argv[3]);
        result.printHeader();
        SearchAlgorithms::AStar(board, heuristic, result);
    }
    else if (algorithm == "alphabeta" || algorithm == "randomAdv" || algorithm == "mcts") {
        AdverserialPlayers players;
        players.Agent = result.algorithm = argv[2];
        players.Opponent = result.opponent = argv[4];
        players.AgentHeuristic = Heuristics::factory(argv[3]);
        players.OpponentHeuristic = Heuristics::factory(argv[5]);
        result.heuristic = argv[3];
        result.opponentHeuristic = argv[5];
        result.printHeader();
        SearchAlgorithms::AdverserialGame(board, players, result);
    }
    else {
        std::cerr << "Error: Invalid algorithm" << std::endl;
        return 1;
    }

    if (result.winner == Player::NULLPLAYER) {
        std::cout << "No solution found!" << std::endl;
    }
    else {
        std::cout << "Player " << (result.winner == Player::HORIZONTAL ? "HORIZONTAL" : "VERTICAL") << " wins!" << std::endl;
    }
    result.writeSolutionToFile(SOLUTIONS_DIR);
    result.writeToCSV(RESULTS_FILE);
    if (printBoard) {
        Board board(argv[1]);
        result.printSolution(board);
    }
    return 0;
}

int experiments() {
    std::ifstream file("experiments.txt");
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file experiments.txt" << std::endl;
        return 1;
    }
    std::string line;
    char* argv[100];
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string token;
        int i = 1;
        while (std::getline(iss, token, ' ')) {
            argv[i] = new char[token.size() + 1];
            std::copy(token.begin(), token.end(), argv[i]);
            argv[i][token.size()] = '\0';
            i++;
        }
        run_experiment(argv);
    }
    return 0;
}

int main(int argc, char* argv[]) {
    if (std::string(argv[1]) == "experiments.txt") {
        return experiments();
    }
    if (argc < 3) {
        std::cout << "Usage: rushhour <board file> <algorithm> <heuristic> <opponent> <opponent heuristic>" << std::endl;
        return 1;
    }
    return run_experiment(argv, false);
}