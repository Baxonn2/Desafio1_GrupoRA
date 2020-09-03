from state import State
from copy import deepcopy as copy
import heapq


class Solver:

    """
    Solver is a class in charge to get a final state for a given state.
    Currently uses best first search to complete the task
    """

    def __init__(self, init_state: State):
        """
        Initialization of the solver. contains the initial and current state

        :param init_state: initial state given to the solver
        """
        self.init_state = copy(init_state)
        self.actual_state = copy(init_state)

    def best_first(self) -> State:
        """
        best first search method. uses a queue to find a final state. when a
        final state is found returns the state and saves it in the attributes.

        :return: State that is classified as final. if no state satisfies the
        condition and there are no more states available, returns none.
        """
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
