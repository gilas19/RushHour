// Heuristics.cpp

#include "Heuristics.h"

HeuristicFunc Heuristics::factory(const std::string& name) {
    if (name == "null") {
        return nullHeuristic;
    }
    else if (name == "distanceToExit") {
        return distanceToExit;
    }
    else if (name == "blockersCount") {
        return blockersCount;
    }
    else if (name == "blockersTotalSize") {
        return blockersTotalSize;
    }
    else if (name == "stepsToClearPath") {
        return stepsToClearPath;
    }
    else if (name == "singlePlayer") {
        return singlePlayer;
    }
    else if (name == "twoPlayers") {
        return twoPlayers;
    }
    return nullHeuristic;
}

int Heuristics::nullHeuristic(const Board& board, const Player player) {
    return 0;
}

int Heuristics::distanceToExit(const Board& board, const Player player) {
    for (const auto& car : board.cars) {
        if (player == Player::HORIZONTAL && car.id == 'X') {
            return board.gridSize - car.position.x - car.length;
        }
        else if (player == Player::VERTICAL && car.id == 'Y') {
            return board.gridSize - car.position.y - car.length;
        }
    }
    return 0;
}

// TODO: fix for otherPlayer use
int Heuristics::blockersCount(const Board& board, const Player player) {
    int count = 0;
    for (const auto& car : board.cars) {
        if ((player == Player::HORIZONTAL && car.id == 'X') || (player == Player::VERTICAL && car.id == 'Y')) {
            for (int i = 1; i < board.gridSize; ++i) {
                if (player == Player::HORIZONTAL) {
                    if (car.position.x + car.length + i < board.gridSize
                        && board.grid[car.position.y][car.position.x + car.length + i] != '.') {
                        count++;
                    }
                }
                else {
                    if (car.position.y + car.length + i < board.gridSize
                        && board.grid[car.position.y + car.length + i][car.position.x] != '.') {
                        count++;
                    }
                }
            }
        }
    }
    return count;
}

// TODO: fix for otherPlayer use
int Heuristics::blockersTotalSize(const Board& board, const Player player) {
    int totalSize = 0;
    for (const auto& car : board.cars) {
        if ((player == Player::HORIZONTAL && car.id == 'X') || (player == Player::VERTICAL && car.id == 'Y')) {
            for (int i = 1; i < board.gridSize; ++i) {
                if (player == Player::HORIZONTAL) {
                    if (car.position.x + car.length + i >= board.gridSize) {
                        break;
                    }
                    char blockingCarId = board.grid[car.position.y][car.position.x + car.length + i];
                    if (blockingCarId != '.') {
                        Car blockingCar = board.getCarById(blockingCarId);
                        totalSize += blockingCar.length;
                    }
                }
                else {
                    if (car.position.y + car.length + i >= board.gridSize) {
                        break;
                    }
                    char blockingCarId = board.grid[car.position.y + car.length + i][car.position.x];
                    if (blockingCarId != '.') {
                        Car blockingCar = board.getCarById(blockingCarId);
                        totalSize += blockingCar.length;
                    }
                }
            }
        }
        break;
    }
    return totalSize;
}

int Heuristics::stepsToClearPath(const Board& board, const Player player) {
    int steps = 0;
    for (const auto& car : board.cars) {
        if ((player == Player::HORIZONTAL && car.id == 'X') || (player == Player::VERTICAL && car.id == 'Y')) {
            if (car.isHorizontal) {
                for (int row = car.position.y + car.length; row < board.gridSize; ++row) {
                    char blockingCarId = board.grid[row][car.position.x];
                    if (blockingCarId != '.') {
                        Car blockingCar = board.getCarById(blockingCarId);
                        steps += std::min(blockingCar.position.x - car.position.x, car.position.x - blockingCar.position.x) + 1;
                    }
                }
            }
            else {
                for (int col = car.position.x + car.length; col < board.gridSize; ++col) {
                    char blockingCarId = board.grid[car.position.y][col];
                    if (blockingCarId != '.') {
                        Car blockingCar = board.getCarById(blockingCarId);
                        steps += std::min(blockingCar.position.y - car.position.y, car.position.y - blockingCar.position.y) + 1;
                    }
                }
            }
        }
    }
    return steps;
}

int Heuristics::singlePlayer(const Board& board, const Player player) {
    // return (1.2 * pow(distanceToExit(board, player), 3)) + (1.2 * pow(blockersCount(board, player), 2)) + (1 * pow(stepsToClearPath(board, player), 2));
    return 10*distanceToExit(board, player) + blockersCount(board, player) + stepsToClearPath(board, player);
}

int Heuristics::twoPlayers(const Board& board, const Player player) {
    Player otherPlayer = (player == Player::HORIZONTAL) ? Player::VERTICAL : Player::HORIZONTAL;

    return (2 * singlePlayer(board, player)) - (2 * distanceToExit(board, otherPlayer));
}