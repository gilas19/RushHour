# RushHour-AI

RushHour-AI is a project that implements various AI algorithms to solve the Rush Hour puzzle game. It includes both a regular game solver and an adversarial game simulator. The project uses C++ for the core implementation and Python for the GraphPlan algorithm.

Key features:
1. Regular game solver with multiple search algorithms and heuristics
2. GraphPlan implementation for solving Rush Hour puzzles
3. Adversarial game simulator for competitive play

This project demonstrates the application of AI techniques to solve and analyze the Rush Hour puzzle game, providing a platform for comparing different algorithms and heuristics.


## How to Run

Clone the repository
```
git clone https://github.com/gilas19/RushHour.git
```

Build the project
```
mkdir build && cd build && cmake .. && make
```

* if using docker, run the following commands to build the project and run the container:
```
docker build -t rushhour .
docker run -it rushhour
```

## Regular Game Solver
### Search Algorithm
To solve a regular game, run the following command:
```
./build/RushHour <board> <algo> <heuristic>
```
where `<board>` is the board file, `<algo>` is the search algorithm, and `<heuristic>` is the heuristic function.

### GraphPlan
To solve a regular game using GraphPlan, run the following command:
```
python3 graphplan.py <board>
```
where `<board>` is the board file.

### Availavle Components
#### Boards
Boards numbered from 1 to 40 are available in the `boards` folder.

#### Algorithms
- `random`: Random Search
- `bfs`: Breadth-First Search
- `astar`: A* Search

#### Heuristics
- `nullHeuristic`: Null Heuristic
- `distanceToExit`: Distance to Exit
- `blockersCount`: Blockers Count
- `blockersTotalSize`: Blockers Total Size
- `stepsToClearPath`: Steps to Clear Path
- `singlePlayer`: Sum of the above heuristics for single player

## Adverserial Game Simulator

To simulate an adverserial game, run the following command:
```
./build/RushHour <board> <player-algo> <player-heruistic> <opponent> <opponent-heruistic>
```
where `<board>` is the board file, `<player-algo>` is the search algorithm for the player, `<player-heruistic>` is the heuristic function for the player, `<opponent>` is the search algorithm for the opponent, and `<opponent-heruistic>` is the heuristic function for the opponent.

### Availavle Components
#### Available Algorithms
- `random`: Random Search
- `alphabet`: Alphabet Search
- `mcts`: Monte Carlo Tree Search

#### Available Heuristics
All heristics for regular game solver, plus:
- `twoPlayers`: singlePlayer Heuristic minus Opponent singlePlayer Heuristic

## Run All Experiments

To run all experiments, run the following command:
```
./build/RushHour experiments.txt
```

## Results

All results will be saved in the `results` folder.
- `results/results.csv`: tabluar of all experiments
- `results/solutions`: folder containing solutions of the games
- `results/figures`: folder containing animations of the gameplays

## Generate Gameplay Animations

To generate gameplay animations, run the following command:
```
python3 display.py <solution-filename>
```