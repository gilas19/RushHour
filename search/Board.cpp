// Board.cpp

#include "Board.h"

Board::Board(std::string filename) {
    std::ifstream file(BOARDS_DIR + filename);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open board " << filename << std::endl;
        return;
    }

    file >> gridSize;
    grid = std::vector<std::vector<char>>(gridSize, std::vector<char>(gridSize, '.'));
    char id;
    for (int row = 0; row < gridSize; ++row) {
        for (int col = 0; col < gridSize; ++col) {
            file >> id;
            if (id != '.') {
                std::vector<Car>::iterator it =
                    std::find_if(cars.begin(), cars.end(), [id](Car car) { return car.id == id; });
                if (it == cars.end()) {
                    if (col + 1 < gridSize && file.peek() == id) {
                        cars.push_back(Car(id, {col, row}, true, 1));
                    } else {
                        cars.push_back(Car(id, {col, row}, false, 1));
                    }
                } else {
                    it->length++;
                }
            }
        }
    }
    updateGrid();
    // std::cout << "Board created" << std::endl;
}

void Board::updateGrid() {
    for (auto &row : grid)
        std::fill(row.begin(), row.end(), '.');
    for (const auto &car : cars) {
        for (int i = 0; i < car.length; i++) {
            int x = car.position.x + (car.isHorizontal ? i : 0);
            int y = car.position.y + (car.isHorizontal ? 0 : i);
            grid[y][x] = car.id;
        }
    }
}

void Board::printBoard() const {
    for (const auto &row : grid) {
        for (const auto &cell : row) {
            std::cout << cell << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void Board::printCars() const {
    for (const auto &car : cars) {
        std::cout << "Car " << car.id << " at (" << car.position.x << ", " << car.position.y << ") ";
        std::cout << (car.isHorizontal ? "horizontally" : "vertically") << " with length " << car.length << std::endl;
    }
}

bool Board::legalPlace(int x, int y) const {
    return x >= 0 && x < gridSize && y >= 0 && y < gridSize && grid[y][x] == '.';
}

bool Board::canMove(const Car &car, MoveDirection dir, int steps) const {
    if (car.isHorizontal) {
        if (dir == MoveDirection::FORTH) {
            for (int i = 0; i < steps; ++i) {
                if (!legalPlace(car.position.x + car.length + i, car.position.y)) {
                    return false;
                }
            }
        } else {
            for (int i = 0; i < steps; ++i) {
                if (!legalPlace(car.position.x - i - 1, car.position.y)) {
                    return false;
                }
            }
        }
    } else {
        if (dir == MoveDirection::FORTH) {
            for (int i = 0; i < steps; ++i) {
                if (!legalPlace(car.position.x, car.position.y + car.length + i)) {
                    return false;
                }
            }
        } else {
            for (int i = 0; i < steps; ++i) {
                if (!legalPlace(car.position.x, car.position.y - i - 1)) {
                    return false;
                }
            }
        }
    }
    return true;
}

bool Board::applyMove(const Move &move) {
    if (move.carId == '\0') {
        return false;
    }
    for (auto &car : cars) {
        if (car.id == move.carId) {
            if (canMove(car, move.direction, move.steps)) {
                int shift = (move.direction == MoveDirection::FORTH) ? move.steps : -move.steps;
                if (car.isHorizontal) {
                    car.position.x += shift;
                } else {
                    car.position.y += shift;
                }
                updateGrid();
                return true;
            }
            break;
        }
    }
    return false;
}

std::vector<Move> Board::generatePossibleMoves(Player player) const {
    std::vector<Move> possibleMoves;
    for (const auto &car : cars) {
        if ((player != Player::HORIZONTAL || car.id == 'Y') && (player != Player::VERTICAL || car.id == 'X')) {
            continue;
        }
        for (int steps = 1; steps <= 4; ++steps) { // Allow up to 4 steps
            if (canMove(car, MoveDirection::FORTH, steps)) {
                possibleMoves.push_back(Move(car.id, MoveDirection::FORTH, steps, player));
            }
            if (canMove(car, MoveDirection::BACK, steps)) {
                possibleMoves.push_back(Move(car.id, MoveDirection::BACK, steps, player));
            }
        }
    }

    std::shuffle(possibleMoves.begin(), possibleMoves.end(), std::mt19937(std::random_device()()));
    return possibleMoves;
}

bool Board::isWon(Player player) const {
    for (const auto &car : cars) {
        if (car.id == 'X' && player == Player::HORIZONTAL && car.position.x + car.length - 1 == gridSize - 1) {
            return true;
        }
        if (car.id == 'Y' && player == Player::VERTICAL && car.position.y + car.length - 1 == gridSize - 1) {
            return true;
        }
    }
    return false;
}

size_t Board::hash() const {
    size_t result = 0;
    for (const auto &row : grid) {
        for (char cell : row) {
            result ^= std::hash<char>{}(cell) + (result << 4) + (result >> 2);
        }
    }
    return result;
}

Car Board::getCarById(char id) const {
    for (const auto &car : cars) {
        if (car.id == id) {
            return car;
        }
    }
    return Car();
}