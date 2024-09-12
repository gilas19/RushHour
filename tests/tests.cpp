#include <gtest/gtest.h>
#include "Board.h"
#include "Car.h"
#include "Move.h"
#include "SearchAlgorithms.h"
#include "Heuristics.h"

#include <cstdio>
#include <string>
#include <fstream>

class CarTest : public ::testing::Test {
protected:
    Car* car;

    void SetUp() override {
        car = new Car('A', {1, 2}, true, 3);
    }

    void TearDown() override {
        delete car;
    }
};

TEST_F(CarTest, Constructor) {
    EXPECT_EQ(car->id, 'A');
    EXPECT_EQ(car->position.x, 1);
    EXPECT_EQ(car->position.y, 2);
    EXPECT_TRUE(car->isHorizontal);
    EXPECT_EQ(car->length, 3);
}

class MoveTest : public ::testing::Test {
protected:
    Move* move;

    void SetUp() override {
        move = new Move('B', MoveDirection::FORTH, 2, Player::HORIZONTAL);
    }

    void TearDown() override {
        delete move;
    }
};

TEST_F(MoveTest, Constructor) {
    EXPECT_EQ(move->carId, 'B');
    EXPECT_EQ(move->direction, MoveDirection::FORTH);
    EXPECT_EQ(move->steps, 2);
    EXPECT_EQ(move->player, Player::HORIZONTAL);
}

TEST_F(MoveTest, ToString) {
    EXPECT_EQ(move->toString(), "Move B FORTH by 2 step(s)");
}

class BoardTest : public ::testing::Test {
protected:
    Board* board;

    void SetUp() override {
        // Assuming you have a test board file named "test_board.txt"
        board = new Board("test_board.txt");
    }

    void TearDown() override {
        delete board;
    }
};

TEST_F(BoardTest, Constructor) {
    EXPECT_GT(board->gridSize, 0);
    EXPECT_FALSE(board->grid.empty());
    EXPECT_FALSE(board->cars.empty());
}

TEST_F(BoardTest, CanMove) {
    // Assuming 'X' is the target car and starts at (1,2) horizontally
    EXPECT_TRUE(board->canMove(Car('X', {1, 2}, true, 2), MoveDirection::FORTH, 1));
    EXPECT_FALSE(board->canMove(Car('Y', {4, 0}, false, 2), MoveDirection::BACK, 1));
}

TEST_F(BoardTest, ApplyMove) {
    Move move('X', MoveDirection::FORTH, 1, Player::HORIZONTAL);
    bool moved = board->applyMove(move);
    EXPECT_TRUE(moved);
    // Check if the car has actually moved
    auto it = std::find_if(board->cars.begin(), board->cars.end(), [](const Car& c) { return c.id == 'X'; });
    EXPECT_EQ(it->position.x, 2);  // Assuming it started at x=1
}

TEST_F(BoardTest, GeneratePossibleMoves) {
    std::vector<Move> moves = board->generatePossibleMoves(Player::HORIZONTAL);
    EXPECT_FALSE(moves.empty());
}

TEST_F(BoardTest, IsWon) {
    // Move the 'X' car to the rightmost position
    while (board->applyMove(Move('X', MoveDirection::FORTH, 1, Player::HORIZONTAL))) {}
    EXPECT_TRUE(board->isWon(Player::HORIZONTAL));
}

class SearchAlgorithmsTest : public ::testing::Test {
protected:
    Board* board;

    void SetUp() override {
        board = new Board("test_board.txt");
    }

    void TearDown() override {
        delete board;
    }
};

TEST_F(SearchAlgorithmsTest, Random) {
    SearchResult result("test_board.txt", "random");
    std::vector<Move> solution = SearchAlgorithms::Random(*board, Player::HORIZONTAL, result);
    EXPECT_FALSE(solution.empty());
}

TEST_F(SearchAlgorithmsTest, BFS) {
    SearchResult result("test_board.txt", "bfs");
    std::vector<Move> solution = SearchAlgorithms::BFS(*board, result);
    EXPECT_FALSE(solution.empty());
}

TEST_F(SearchAlgorithmsTest, AStar) {
    SearchResult result("test_board.txt", "astar", "distanceToExit");
    std::vector<Move> solution = SearchAlgorithms::AStar(*board, Heuristics::distanceToExit, result);
    EXPECT_FALSE(solution.empty());
}

TEST_F(SearchAlgorithmsTest, AlphaBeta) {
    Move move = SearchAlgorithms::AlphaBeta(*board, Player::HORIZONTAL, Heuristics::distanceToExit);
    EXPECT_NE(move.carId, '\0');
}

TEST_F(SearchAlgorithmsTest, MCTS) {
    Move move = SearchAlgorithms::MCTS(*board, Player::HORIZONTAL);
    EXPECT_NE(move.carId, '\0');
}

class MainTest : public ::testing::Test {
protected:
    void SetUp() override {
        old_stdout = dup(fileno(stdout));
        freopen("output.txt", "w", stdout);
    }

    // Restore stdout
    void TearDown() override {
        fflush(stdout);
        dup2(old_stdout, fileno(stdout));
        close(old_stdout);
        remove("output.txt");
    }

    std::string getCapturedOutput() {
        std::ifstream ifs("output.txt");
        return std::string((std::istreambuf_iterator<char>(ifs)),
                           (std::istreambuf_iterator<char>()));
    }

    int old_stdout;
};

TEST_F(MainTest, RunWithBFS) {
    const std::string cmd = "./rushhour sample1.txt bfs";
    system(cmd.c_str());
    
    std::string output = getCapturedOutput();
    EXPECT_FALSE(output.empty());
    EXPECT_TRUE(output.find("Board: sample1	Algorithm: bfs	") != std::string::npos);
    EXPECT_TRUE(output.find("Player HORIZONTAL wins!") != std::string::npos);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}