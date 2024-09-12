// Boadr.h
#ifndef BOARD_H
#define BOARD_H

#include "Car.h"
#include "Move.h"
#include "Player.h"
#include <algorithm>
#include <fstream>
#include <functional>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <vector>

#define BOARDS_DIR "../boards/"

class Board {
  public:
    int gridSize;
    std::vector<std::vector<char>> grid; // 2D grid to represent the board
    std::vector<Car> cars;               // List of cars on the board

    Board(std::string filename);
    Board(const Board &other) = default;

    bool canMove(const Car &car, MoveDirection dir, int steps) const;
    bool applyMove(const Move &move);
    std::vector<Move> generatePossibleMoves(Player player) const;
    bool isWon(Player player) const;
    void printBoard() const;
    void printCars() const;
    std::size_t hash() const;
    void updateGrid();
    bool legalPlace(int x, int y) const;
    Car getCarById(char id) const;
};

#endif // BOARD_H