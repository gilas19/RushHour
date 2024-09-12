// Result.h
#ifndef RESULT_H
#define RESULT_H

#include "Move.h"
#include "Board.h"
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <ctime>
#include <map>


struct SearchResult {
    std::string boardFileName;
    std::string boardName;
    std::string algorithm;
    std::string heuristic;
    std::string opponent;
    std::string opponentHeuristic;
    std::vector<Move> solution;
    int moves;
    double executionTime;
    int expandedNodes;
    Player winner;

    // Constructor to initialize the basic details
    SearchResult(const std::string& boardName, const std::string& algorithm, const std::string& heuristic = "",
        const std::string& opponent = "", const std::string& opponentHeuristic = "")
        : boardFileName(boardName), algorithm(algorithm), heuristic(heuristic), opponent(opponent),
        opponentHeuristic(opponentHeuristic), moves(0), executionTime(0), expandedNodes(0), winner(Player::NULLPLAYER) {
        this->boardName = extractBoardName(boardName);
    }

    void updateSolution(const std::vector<Move>& solution, const std::clock_t startTime, Player winner) {
        this->solution = solution;
        this->moves = solution.size();
        this->executionTime = ((double)(clock() - startTime)) / CLOCKS_PER_SEC;
        this->winner = winner;
    }

    // Function to write results to a CSV file
    // Format: boardName, algorithm, heuristic, opponent, opponentHeuristic, moves, executionTime, expandedNodes, winner
    void writeToCSV(const std::string& filename) const {
        std::ofstream file;
        file.open(filename, std::ios_base::app); // Append to existing file
        if (!file.is_open()) {
            std::cerr << "Error opening csv file: " << filename << std::endl;
            return;
        }

        file << boardName << ","
            << algorithm << ","
            << heuristic << ","
            << opponent << ","
            << opponentHeuristic << ","
            << moves << ","
            << static_cast<double>(executionTime) << ","
            << expandedNodes << ",";

        if (winner == Player::HORIZONTAL) {
            file << "X" << std::endl;
        }
        else if (winner == Player::VERTICAL) {
            file << "Y" << std::endl;
        }
        else {
            file << "None" << std::endl;
        }

        file.close();
    }

    // Function to write the solution to a file
    // Format: [(carId, direction, steps, player), ...]
    void writeSolutionToFile(const std::string& directory) const {
        std::string filename = generateSolutionFilename();
        std::ofstream file(directory + filename);
        if (!file.is_open()) {
            std::cerr << "Error opening solution file: " << filename << std::endl;
            return;
        }
        Board board(boardFileName);
        std::map<char, std::pair<std::string, std::string>> carDirMap;
        for (const Car& car : board.cars) {
            if (car.isHorizontal) {
                carDirMap[car.id] = { "RIGHT", "LEFT" };
            }
            else {
                carDirMap[car.id] = { "DOWN", "UP" };
            }
        }
        std::stringstream moves;
        moves << "[";

        for (size_t i = 0; i < solution.size(); ++i) {
            const Move& move = solution[i];
            std::string dirStr = (move.direction == MoveDirection::FORTH) ? carDirMap[move.carId].first : carDirMap[move.carId].second;
            std::string playerStr = (move.player == Player::HORIZONTAL) ? "X" : "Y";
            moves << "('" << move.carId << "', '" << dirStr << "', " << move.steps << ", '" << playerStr << "')";

            if (i < solution.size() - 1) {
                moves << ", ";
            }
        }
        moves << "]";
        file << moves.str() << std::endl;
        file.close();
    }

    void printSolution(Board& board) {
        if (solution.empty()) {
            std::cout << "No solution found!" << std::endl;
        }
        else {
            std::cout << "Solution:" << std::endl;
            for (const Move& move : solution) {
                std::cout << move.toString() << std::endl;
                board.applyMove(move);
                board.printBoard();
            }
        }
    }

    void printHeader() const {

        std::cout << "Board: " << boardName << "\t";
        std::cout << "Algorithm: " << algorithm << "\t";

        if (!heuristic.empty()) {
            std::cout << "Heuristic: " << heuristic << "\t";
        }
        if (!opponent.empty()) {
            std::cout << "Opponent: " << opponent << "\t";
        }
        if (!opponentHeuristic.empty()) {
            std::cout << "Opponent Heuristic: " << opponentHeuristic << "\t";
        }
        std::cout << std::endl;
    }

private:
    // Helper function to generate the solution filename
    std::string generateSolutionFilename() const {

        std::string filename = boardName + "_" + algorithm;
        if (!heuristic.empty()) {
            filename += "_" + heuristic;
        }
        if (!opponent.empty()) {
            filename += "_" + opponent;
        }
        if (!opponentHeuristic.empty()) {
            filename += "_" + opponentHeuristic;
        }
        filename += "_solution.txt";
        return filename;
    }

    std::string extractBoardName(const std::string& filePath) {
        size_t lastSlash = filePath.find_last_of('/');
        size_t dotPos = filePath.find('.', lastSlash + 1);
        return filePath.substr(lastSlash + 1, dotPos - lastSlash - 1);
    }
};

#endif // RESULT_H