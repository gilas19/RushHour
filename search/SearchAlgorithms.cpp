// SearchAlgorithms.cpp

#include "SearchAlgorithms.h"
#include "Move.h"
#include <algorithm>
#include <queue>
#include <unordered_set>

std::vector<Move> SearchAlgorithms::Random(Board &board, Player player, SearchResult &result) {
    std::clock_t startTime = clock();
    std::vector<Move> solution;
    std::vector<Move> possibleMoves = board.generatePossibleMoves(player);

    while (!board.isWon(player)) {
        if (solution.size() == MOVES_LIMIT) {
            std::cout << "Solution limit reached" << std::endl;
            result.updateSolution(solution, startTime, Player::NULLPLAYER);
            return solution;
        }
        Move move = possibleMoves.front();
        solution.push_back(move);
        board.applyMove(move);
        possibleMoves = board.generatePossibleMoves(player);
    }

    result.updateSolution(solution, startTime, player);
    return solution;
}

std::vector<Move> SearchAlgorithms::BFS(Board &board, SearchResult &result, Player player) {
    std::clock_t startTime = clock();
    std::queue<BoardState> frontier;
    std::unordered_set<std::size_t> visited;
    int expandedNodes = 0;

    frontier.push({board, {}});
    visited.insert(board.hash());

    while (!frontier.empty()) {
        BoardState current = frontier.front();
        frontier.pop();
        expandedNodes++;

        if (current.board.isWon(player)) {
            result.updateSolution(current.moves, startTime, player);
            result.expandedNodes = expandedNodes;
            return current.moves;
        }

        for (const Move &move : current.board.generatePossibleMoves(player)) {
            Board newBoard = Board(current.board);
            newBoard.applyMove(move);
            if (visited.find(newBoard.hash()) == visited.end()) {
                std::vector<Move> newMoves = current.moves;
                newMoves.push_back(move);
                frontier.push({newBoard, newMoves});
                visited.insert(newBoard.hash());
            }
        }
    }
    result.updateSolution({}, startTime, Player::NULLPLAYER);
    return {};
}

struct CompareBoardState {
    bool operator()(const BoardState &a, const BoardState &b) { return a.f() > b.f(); }
};

std::vector<Move> SearchAlgorithms::AStar(Board &board, HeuristicFunc heuristic, SearchResult &result, Player player) {
    std::clock_t startTime = clock();
    std::priority_queue<BoardState, std::vector<BoardState>, CompareBoardState> frontier;
    std::unordered_set<std::size_t> visited;
    int expandedNodes = 0;

    frontier.push({board, {}, 0, heuristic(board, player)});
    visited.insert(board.hash());

    while (!frontier.empty()) {
        BoardState current = frontier.top();
        frontier.pop();
        expandedNodes++;

        if (current.board.isWon(player)) {
            result.updateSolution(current.moves, startTime, player);
            result.expandedNodes = expandedNodes;
            return current.moves;
        }

        for (const Move &move : current.board.generatePossibleMoves(player)) {
            Board newBoard = Board(current.board);
            newBoard.applyMove(move);
            if (visited.find(newBoard.hash()) == visited.end()) {
                std::vector<Move> newMoves = current.moves;
                newMoves.push_back(move);
                frontier.push({newBoard, newMoves, current.g + 1, heuristic(newBoard, player)});
                visited.insert(newBoard.hash());
            }
        }
    }
    result.updateSolution({}, startTime, Player::NULLPLAYER);
    return {};
}

Move SearchAlgorithms::RandomAdv(Board &board, Player player) { return board.generatePossibleMoves(player).front(); }

int minimax(Board &board, int depth, int alpha, int beta, bool isMaximizingPlayer, Player currentPlayer,
            HeuristicFunc evaluate) {
    Player opponent = (currentPlayer == Player::HORIZONTAL) ? Player::VERTICAL : Player::HORIZONTAL;

    if (depth == 0 || board.isWon(currentPlayer) || board.isWon(opponent)) {
        return evaluate(board, currentPlayer);
    }

    if (isMaximizingPlayer) {
        int maxEval = std::numeric_limits<int>::min();
        for (const auto &move : board.generatePossibleMoves(currentPlayer)) {
            Board tempBoard(board);
            tempBoard.applyMove(move);
            int eval = minimax(tempBoard, depth - 1, alpha, beta, false, currentPlayer, evaluate);
            maxEval = std::max(maxEval, eval);
            alpha = std::max(alpha, eval);
            if (beta <= alpha)
                break;
        }
        return maxEval;
    } else {
        int minEval = std::numeric_limits<int>::max();
        for (const auto &move : board.generatePossibleMoves(opponent)) {
            Board tempBoard(board);
            tempBoard.applyMove(move);
            int eval = minimax(tempBoard, depth, alpha, beta, true, currentPlayer, evaluate);
            minEval = std::min(minEval, eval);
            beta = std::min(beta, eval);
            if (beta <= alpha)
                break;
        }
        return minEval;
    }
}

Move SearchAlgorithms::AlphaBeta(Board &board, Player player, HeuristicFunc heuristic, int depth) {
    int bestValue = std::numeric_limits<int>::min();
    Move bestMove;
    Board tempBoard(board);

    for (const auto &move : board.generatePossibleMoves(player)) {
        tempBoard = Board(board);
        tempBoard.applyMove(move);
        int moveValue = minimax(tempBoard, depth - 1, std::numeric_limits<int>::min(), std::numeric_limits<int>::max(),
                                false, player, heuristic);

        if (moveValue > bestValue) {
            bestValue = moveValue;
            bestMove = move;
        }
    }
    return bestMove;
}

MCTSNode *expand(MCTSNode *node) {
    std::vector<Move> possibleMoves = node->board.generatePossibleMoves(node->player);
    for (const auto &move : possibleMoves) {
        if (std::find_if(node->children.begin(), node->children.end(),
                         [&move](const MCTSNode *child) { return child->move == move; }) == node->children.end()) {
            Board newBoard = node->board;
            newBoard.applyMove(move);
            Player nextPlayer = (node->player == Player::HORIZONTAL) ? Player::VERTICAL : Player::HORIZONTAL;
            MCTSNode *newNode = new MCTSNode(newBoard, move, nextPlayer, node);
            node->children.push_back(newNode);
            return newNode;
        }
    }
    return nullptr;
}

MCTSNode *getBestChild(MCTSNode *node, double explorationParameter) {
    return *std::max_element(
        node->children.begin(), node->children.end(),
        [explorationParameter, node](const MCTSNode *a, const MCTSNode *b) {
            double uctA = a->score / a->visits + explorationParameter * std::sqrt(std::log(node->visits) / a->visits);
            double uctB = b->score / b->visits + explorationParameter * std::sqrt(std::log(node->visits) / b->visits);
            return uctA < uctB;
        });
}

MCTSNode *select(MCTSNode *node, double explorationParameter) {
    while (!node->isTerminal()) {
        if (!node->isFullyExpanded()) {
            return expand(node);
        }
        node = getBestChild(node, explorationParameter);
    }
    return node;
}

double simulate(MCTSNode *node) {
    Board tempBoard = node->board;
    Player currentPlayer = node->player;

    while (!tempBoard.isWon(Player::HORIZONTAL) && !tempBoard.isWon(Player::VERTICAL)) {
        std::vector<Move> possibleMoves = tempBoard.generatePossibleMoves(currentPlayer);
        if (possibleMoves.empty())
            break;

        Move randomMove = possibleMoves[rand() % possibleMoves.size()];
        tempBoard.applyMove(randomMove);
        currentPlayer = (currentPlayer == Player::HORIZONTAL) ? Player::VERTICAL : Player::HORIZONTAL;
    }

    if (tempBoard.isWon(Player::HORIZONTAL))
        return 1.0;
    if (tempBoard.isWon(Player::VERTICAL))
        return 0.0;
    return 0.5; // draw
}

void backpropagate(MCTSNode *node, double score) {
    while (node != nullptr) {
        node->visits++;
        node->score += score;
        node = node->parent;
        score = 1.0 - score; // flip the score for the opponent
    }
}

Move SearchAlgorithms::MCTS(Board &board, Player player, int numIterations, double explorationParameter) {
    MCTSNode root(board, Move(), player);

    for (int i = 0; i < numIterations; ++i) {
        MCTSNode *node = select(&root, explorationParameter);
        double score = simulate(node);
        backpropagate(node, score);
    }

    MCTSNode *bestChild = *std::max_element(root.children.begin(), root.children.end(),
                                            [](const MCTSNode *a, const MCTSNode *b) { return a->visits < b->visits; });

    if (bestChild->move.carId == '\0') {
        return Move();
    }
    return bestChild->move;
}

std::vector<Move> SearchAlgorithms::AdverserialGame(Board &board, AdverserialPlayers players, SearchResult &result) {
    std::clock_t startTime = clock();
    std::vector<Move> moves;
    Player currentPlayer = Player::HORIZONTAL;
    Move move;
    while ((!board.isWon(Player::HORIZONTAL) && !board.isWon(Player::VERTICAL))) {
        std::cout << moves.size() << std::endl;
        if (moves.size() == MOVES_LIMIT) {
            std::cout << "Moves limit reached" << std::endl;
            result.updateSolution(moves, startTime, Player::NULLPLAYER);
            return moves;
        }
        if (currentPlayer == Player::HORIZONTAL) {
            if (players.Agent == "random") {
                move = RandomAdv(board, currentPlayer);
            } else if (players.Agent == "mcts") {
                move = MCTS(board, currentPlayer);
            } else {
                move = AlphaBeta(board, currentPlayer, players.AgentHeuristic);
            }
        } else {
            if (players.Opponent == "random") {
                move = RandomAdv(board, currentPlayer);
            } else if (players.Opponent == "mcts") {
                move = MCTS(board, currentPlayer);
            } else {
                move = AlphaBeta(board, currentPlayer, players.OpponentHeuristic);
            }
        }
        moves.push_back(move);
        board.applyMove(move);
        currentPlayer = (currentPlayer == Player::HORIZONTAL) ? Player::VERTICAL : Player::HORIZONTAL;
    }
    result.updateSolution(moves, startTime, (board.isWon(Player::HORIZONTAL)) ? Player::HORIZONTAL : Player::VERTICAL);
    return moves;
}