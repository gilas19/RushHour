// SearchAlgorithms.h
#ifndef SEARCHALGORITHMS_H
#define SEARCHALGORITHMS_H

#include "Board.h"
#include "Heuristics.h"
#include "Move.h"
#include "SearchResult.h"
#include <functional>
#include <limits>
#include <vector>

#define MOVES_LIMIT 2500

struct BoardState {
    Board board;
    std::vector<Move> moves; // Track moves leading to this state
    int g = 0;               // Cost to reach this state
    int h = 0;               // Heuristic estimate to goal

    BoardState(const Board &board, const std::vector<Move> &moves = {}, int g = 0, int h = 0)
        : board(board), moves(moves), g(g), h(h) {}

    int f() const { return g + h; }

    bool operator==(const BoardState &other) const { return board.hash() == other.board.hash(); }
};

struct MCTSNode {
    Board board;
    Move move;
    Player player;
    MCTSNode *parent;
    std::vector<MCTSNode *> children;
    int visits;
    double score;

    MCTSNode(Board b, Move m, Player p, MCTSNode *par = nullptr)
        : board(b), move(m), player(p), parent(par), visits(0), score(0.0) {}

    ~MCTSNode() {
        for (auto child : children) {
            delete child;
        }
    }

    bool isFullyExpanded() const { return children.size() == board.generatePossibleMoves(player).size(); }

    bool isTerminal() const { return board.isWon(Player::HORIZONTAL) || board.isWon(Player::VERTICAL); }
};

struct AdverserialPlayers {
    std::string Agent;
    HeuristicFunc AgentHeuristic;
    std::string Opponent;
    HeuristicFunc OpponentHeuristic;
};

namespace SearchAlgorithms {
std::vector<Move> Random(Board &board, Player player, SearchResult &result);                   // Random Search
std::vector<Move> BFS(Board &board, SearchResult &result, Player player = Player::HORIZONTAL); // Breadth-First Search
std::vector<Move> AStar(Board &board, HeuristicFunc heuristic, SearchResult &result,
                        Player player = Player::HORIZONTAL);                         // A* Search
Move RandomAdv(Board &board, Player player);                                         // Random Search
Move AlphaBeta(Board &board, Player player, HeuristicFunc heuristic, int depth = 2); // Single Move Alpha-Beta Pruning
std::vector<Move> AdverserialGame(Board &board, AdverserialPlayers players,
                                  SearchResult &result); // Full Game Alpha-Beta Pruning
Move MCTS(Board &board, Player player, int iterations = 200,
          double explorationParameter = 1.2); // Monte Carlo Tree Search
} // namespace SearchAlgorithms

#endif // SEARCHALGORITHMS_H