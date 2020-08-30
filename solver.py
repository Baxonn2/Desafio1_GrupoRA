from state import State
from copy import deepcopy as copy
import heapq

class Solver:

    init_state: State
    actual_state: State

    def __init__(self, init_state: State):
        self.init_state = copy(init_state)
        self.actual_state = copy(init_state)

    def best_first(self) -> State:
        q = []
        heapq.heappush(q, self.init_state)
        while len(q) > 0:
            self.actual_state = heapq.heappop(q)

            if self.actual_state.is_visited():
                continue
            else:
                self.actual_state.visit()

            if self.actual_state.is_final():
                return self.actual_state

            actions = self.actual_state.get_actions()
            for action in actions:
                new_state = self.actual_state.transition(action)
                if not new_state.is_visited():
                    heapq.heappush(q, new_state)