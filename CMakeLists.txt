cmake_minimum_required(VERSION 3.10)
project(RushHour)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add source files
set(SOURCES
    search/Board.cpp
    search/Car.cpp
    search/Move.cpp
    search/SearchAlgorithms.cpp
    search/Heuristics.cpp
)
include_directories(${PROJECT_SOURCE_DIR}/search)

# Create executable
add_executable(rushhour search/main.cpp ${SOURCES})

# Include directories
target_include_directories(rushhour PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})


# Add Python script execution
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/experiments.txt
    COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/generateExperiments.py
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/generateExperiments.py
    COMMENT "Generating experiments.txt"
)

# Add custom target to run experiments
add_custom_target(run_experiments
    COMMAND ./rushhour experiments.txt
    DEPENDS rushhour ${CMAKE_CURRENT_BINARY_DIR}/experiments.txt
    COMMENT "Running experiments"
)

# Google Test
include(FetchContent)
FetchContent_Declare(
  googletest URL https://github.com/google/googletest/archive/refs/tags/v1.15.2.zip
)
FetchContent_MakeAvailable(googletest)

# Add the test executable
add_executable(tests tests/tests.cpp ${SOURCES})
target_link_libraries(tests gtest_main)

enable_testing()
add_test(NAME unit_tests COMMAND tests)
