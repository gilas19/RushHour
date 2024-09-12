// Car.h
#ifndef CAR_H
#define CAR_H

struct Position {
    int x, y;
};

class Car {
public:
    char id;           // Unique identifier for the car
    Position position; // Starting position of the car
    bool isHorizontal; // Orientation of the car
    int length;        // Length of the car

    Car(char id, Position pos, bool hor, int len);
    Car() = default;
};

#endif // CAR_H