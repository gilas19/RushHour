// Heuristics.h
#ifndef HEURISTICS_H
#define HEURISTICS_H

#include "Board.h"

typedef std::function<int(const Board&, const Player)> HeuristicFunc;

namespace Heuristics {
    // Factory function to create a heuristic function
    HeuristicFunc factory(const std::string& name);

    // null heuristic
    int nullHeuristic(const Board& board, const Player player);

    // the distance of player's car to the exit
    int distanceToExit(const Board& board, const Player player);

    // the number of cars blocking the path of player's car
    int blockersCount(const Board& board, const Player player);

    // the total size of cars blocking the path of player's car
    int blockersTotalSize(const Board& board, const Player player);

    // the number of steps to clear the path of player's car
    int stepsToClearPath(const Board& board, const Player player);

    // sum of the above heuristics
    int singlePlayer(const Board& board, const Player player);

    // sum of the above heuristics for adversarial players
    int twoPlayers(const Board& board, const Player player);
}

#endif // HEURISTICS_H