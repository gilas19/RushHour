// Move.cpp

#include "Move.h"

Move::Move(char carId, MoveDirection dir, int steps, Player player)
    : carId(carId), direction(dir), steps(steps), player(player) {}

std::string Move::toString() const {
    std::string dirStr = (direction == MoveDirection::FORTH) ? "FORTH" : "BACK";
    return "Move " + std::string(1, carId) + " " + dirStr + " by " + std::to_string(steps) + " step(s)";
}

bool Move::operator==(const Move &other) const {
    return carId == other.carId && direction == other.direction && steps == other.steps && player == other.player;
}