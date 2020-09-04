from __future__ import annotations
from typing import List
from action import Action
from copy import deepcopy as copy
from _state import BaseState
import math


class State(BaseState):

    """
    State function to the problem of cutting planks. contains the necessary cuts
    to do, planks needed and the cuts done in every plank. If receives
    lengths greater than the size of planks it will be cropped to the max
    possible size.
    """

    def __init__(self, dims, planks_length):
        """
        Class initialization method.

        :param dims: list of lengths of the cuts to do in the planks. once
        received is sorted in descending order.

        :param planks_length: Length of the planks to be used.
        """
        super().__init__(visited=False)
        self.dims = dims  # lista de dimensiones por cortar
        self.dims.sort(reverse=True)
        self.planks = []  # lista con espacios para cortar en una tabla
        self.cuts = []  # Lista con cortes diferentes cortes por cada table
        self.plank_length = planks_length  # Largo default de la tabla
        self.filled_planks = 0  # planks that has been completely filled
        self.upper_bound = len(dims)  # upper bound of planks. where the quantity of planks
        # is equal to the number of cuts

        self.__load_init(planks_length)

    def __load_init(self, planks_length):
        """
        Realiza el procesamiento de la información para establecer los datos del
        estado

        :param planks_length: largo de las tablas sin cortar
        """
        # todas las dimensiones mayores al largo de la plank serán truncadas
        for i in self.dims:
            if i > self.plank_length:
                self.dims.pop(self.dims.index(i))
                self.dims.append(self.plank_length)

        # set el lower bound. La cantidad mínima de tablas es la suma de
        # las dimensiones / largo tabla
        total_planks = math.ceil(sum(self.dims) / planks_length)
        self.planks = [planks_length] * total_planks

        # Creates emtpy list of cuts per table
        self.cuts = [[] for _ in self.planks]

    def is_valid(self) -> bool:
        """
        Comprueba si este estado es valido o no

        Returns:
            bool: Retorna True si es valido y False en caso contrario
        """
        for plank in self.planks:
            if plank < 0:
                return False
        return True

    def is_final(self) -> bool:
        """
        Comprueba si este estado es un estado final

        Returns:
            bool: Retorna True si es un estado final y False en caso contrario
        """
        return len(self.dims) == 0

    def get_actions(self) -> list:
        """
        Obtiene una lista de acciones que se pueden realizar a este estado

        Returns:
            List[State]: Retorna una lista de estados
        """
        actions = []

        for plank, _ in enumerate(self.planks):
            action = Action(plank, self.dims[0])

            if self.is_valid_transition(action):  # new_state.is_valid():
                actions.append(action)

        if len(actions) > 0:
            return actions
        else:  # si no hay acciones validas se agrega una tabla
            self.planks.append(self.plank_length)
            self.cuts.append([])
            if len(self.planks) <= self.upper_bound:  # previene loop infinito
                return self.get_actions()
            else:
                return []

    def is_valid_transition(self, action: Action) -> bool:
        """
        Quick check to test a new action in the state

        :param action: Action to check in the current state
        :return: True if is a valid state, False otherwise
        """
        # Aplicando accion
        return self.planks[action.plank] >= action.cut

    def transition(self, action: Action) -> State:
        """
        Realiza una accion al estado actual y retorna un nuevo estado

        Args:
            action (Action): Accion que se le va a realizar al estado

        Returns:
            State: Retorna un nuevo estado
        """
        new_state = copy(self)
        new_state.visited = False
        new_state.planks[action.plank] -= action.cut
        new_state.cuts[action.plank].append(action.cut)
        new_state.dims.remove(action.cut)
        # si la acción hizo un perfect fit (largo restante = 0 )
        if new_state.planks[action.plank] == 0:
            new_state.filled_planks += 1

        return new_state

    def wf(self):
        """
        Weight method to evaluate the quality of the state using the free
        remaining spaces in planks.

        :return: number between 0 and -length of plank * qty of planks
        """
        w = 0
        for i in self.planks:
            sobra = i - self.plank_length
            w += sobra ** 3
        return w

    def state_info(self, string: bool = True):
        """
        information of the current state related to the total available space
        in the boards.

        :param string: boolean value, by default set as true

        :return: the total planks existing in the state, total free space
        available, biggest and smallest gap in the set of boards, mean free
        space available and standard deviation of the free space. When string
        set as True, returns the information as a string. When False, returns a
        python dictionary
        """
        free_space = sum(self.planks)
        mean = free_space / len(self.planks)
        sd = 0

        for plank in self.planks:
            sd += (plank - mean) ** 2
        sd = math.sqrt(sd / (len(self.planks) - 1))

        if string:
            return f'Planks: {len(self.planks)}\n' \
                   f'Free space\n' \
                   f'  total: {free_space}\n' \
                   f'  max: {max(self.planks)}\tmin: {min(self.planks)}\n' \
                   f'  mean: {mean}\n' \
                   f'  sd: {sd}'
        return {
            'Planks': len(self.planks),
            'total': free_space,
            'max': max(self.planks),
            'min': min(self.planks),
            'mean': mean,
            'sd': sd,
        }

    def __lt__(self, other: State):
        """
        overwriting lower than (<) operator. Checks if the value of the state is
        lower than other according to a priority. The state with better value
        is the lower.

        :param other: State class.

        :return: True if the current state is lower than the other
        """

        # Check which state has more planks
        if len(self.planks) != len(other.planks):
            return len(self.planks) > len(other.planks)

        # Check if the current state has more filled planks
        if self.filled_planks != other.filled_planks:
            return self.filled_planks > other.filled_planks

        # comparison according to a weight function that evaluates the total
        # free space in the state
        return self.wf() < other.wf()
