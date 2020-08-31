from copy import deepcopy as copy
import heapq
import random
from grapher import Grapher
from state import State
from action import Action
from solver import Solver


def best_first(init_state: State) -> State:
    q = []
    heapq.heappush(q, init_state)
    while len(q) > 0:
        actual_state = heapq.heappop(q)

        if actual_state.is_visited():
            continue
        else:
            actual_state.visit()

        if actual_state.is_final():
            return actual_state

        actions = actual_state.get_actions()
        for action in actions:
            new_state = actual_state.transition(action)
            if not new_state.is_visited():
                heapq.heappush(q, new_state)


if __name__ == "__main__":
    #state = State([100, 200, 32200, 400, 500, 3000, 2700, 1601, 1601, 1601, 1599, 
    #            1601, 1601, 1601, 1601, 1601, 1601, 39, 39, 39], 3200)
    dims = []
    MIN = 100
    RAD = 1000
    for _ in range(30):
        dims.append(int(MIN + RAD * random.random()))
    state = State(dims, 3200)
    #solver = Solver(state)
    #best = solver.best_first()

    grapher = Grapher(state)
    grapher.run()
    
    #print(len(best.planks))
    print(grapher.solver.actual_state.cuts)

    #grapher = Grapher(state)
    #grapher.set_state(best)
    #grapher.run()
    #grapher.wait()

