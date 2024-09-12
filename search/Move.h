// Move.h
#ifndef MOVE_H
#define MOVE_H

#include "Player.h"
#include <string>

enum class MoveDirection { FORTH, BACK };

class Move {
  public:
    char carId;              // Identifier for the car
    MoveDirection direction; // Direction of the move (FORTH or BACK)
    int steps;               // Number of steps to move
    Player player;           // Player making the move

    Move(char carId, MoveDirection dir, int steps, Player player = Player::HORIZONTAL);
    Move() = default;
    std::string toString() const; // For debugging or logging moves

    bool operator==(const Move &other) const;
};

#endif // MOVE_H