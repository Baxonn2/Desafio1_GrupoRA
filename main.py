from state import State
from solver import Solver
import random
from grapher import Grapher
import sys, getopt


def main(state):
    solver = Solver(state)
    final_state = solver.best_first()
    print(final_state.cuts)
    print(f"state info:\n {final_state.state_info()}")


def graphical_main(state):
    grapher = Grapher(state)
    grapher.run()

    print(grapher.solver.actual_state.cuts)
    print(f"Planks: {len(grapher.solver.actual_state.planks)}")
    print(f"state info:\n {grapher.solver.actual_state.state_info()}")


def main_wrapper(argv):
    seed = 1234567
    cuttings = 200
    graphic = False
    plank_length = 3200
    min_ = 100
    rad = 1000
    dims = []

    try:
        opts, args = getopt.getopt(argv, "ghs:pl:c:m:r:",
                                   ["seed=",
                                    "plank-length=",
                                    "cuttings=",
                                    "graphic",
                                    "min=",
                                    "rad="
                                    ])
    except getopt.GetoptError:
        print('main.py -s <seed> -pl <plank-length> -c <cuttings> -m <min-lenght> -r <rad>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -s <seed> -pl <plank-length> -c <cuttings>')
            sys.exit()
        elif opt in ("-s", "--seed"):
            seed = arg
        elif opt in ("-c", "--cuttings"):
            cuttings = arg
        elif opt in ("-pl", "--plank-length"):
            plank_length = arg
        elif opt in ("-m", "--min"):
            min_ = arg
        elif opt in ("-r", "--rad"):
            rad = arg
        elif opt in ("-g", "--graphic"):
            graphic = True

    random.seed(seed)

    for _ in range(cuttings):
        dims.append(int(min_ + rad * random.random()))
    initial_state = State(dims, plank_length)

    if graphic:
        graphical_main(initial_state)
    else:
        main(initial_state)


if __name__ == "__main__":
    main_wrapper(sys.argv[1:])
