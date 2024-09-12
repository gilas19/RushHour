cmake_minimum_required(VERSION 3.10)
project(RushHour)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add source files
set(SOURCES
    src/Board.cpp
    src/Car.cpp
    src/Move.cpp
    src/SearchAlgorithms.cpp
    src/Heuristics.cpp
)

include_directories(${PROJECT_SOURCE_DIR}/src)

# Create executable
add_executable(rushhour src/main.cpp ${SOURCES})

# Include directories
target_include_directories(rushhour PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Google Test
include(FetchContent)
FetchContent_Declare(
  googletest
#   URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
    URL https://github.com/google/googletest/archive/refs/tags/v1.15.2.zip
)
FetchContent_MakeAvailable(googletest)

# Add the test executable
add_executable(tests tests/tests.cpp ${SOURCES})
target_link_libraries(tests gtest_main)

enable_testing()
add_test(NAME unit_tests COMMAND tests)
