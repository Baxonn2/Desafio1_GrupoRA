from state import State
from solver import Solver
import random

def main():
    dims = []
    MIN = 100
    RAD = 1000
    for i in range(30):
        dims.append(int(MIN + RAD * random.random()))
    state = State(dims, 3200)
    solver = Solver(state)
    bf = solver.best_first()
    print(bf.cuts)


if __name__ == "__main__":
    main()
