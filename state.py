from __future__ import annotations
from typing import List
from action import Action
from copy import deepcopy as copy
from _state import BaseState
import math


class State(BaseState):
    # pl = 0  # largo de las tablas
    # dims = []  # lista de dimensiones por cortar
    # planks = []  # lista de tabla (dimensión) restante por palo
    # cuts = []  # lista de cortes por palo [[100, 300, 400], [3000, 200], [500, 2700]]
    # bf = 0  # heuristica best fit: cada tabla que no tenga dimensión restante
    # # 					  suma 1 punto, de esta forma se minimiza el
    # #					  gasto por tabla, (mejor bf, mejor estado)
    # ub = 0  # upper bound

    def __init__(self, dims, planks_length):
        super().__init__(visited=False)
        self.dims = dims
        self.planks = []
        self.cuts = []
        self.pl = planks_length
        self.bf = 0
        self.ub = len(dims)

        self.__load_init(planks_length)

    def __load_init(self, planks_length):
        # todas las dimensiones mayores al largo de la plank serán truncadas
        for i in self.dims:
            if i > self.pl:
                self.dims.pop(self.dims.index(i))
                self.dims.append(self.pl)

        # set el lower bound. La cantidad mínima de tablas es la suma de
        # las dimensiones / largo tabla
        total_planks = math.ceil(sum(self.dims)/planks_length)
        self.planks = [planks_length] * total_planks

        for _, __ in enumerate(self.planks):
            self.cuts.append([])

    def is_valid(self) -> bool:
        """
        Comprueba si este estado es valido o no

        Returns:
            bool: Retorna True si es valido y False en caso contrario
        """
        # TODO: check if the only thing to test
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
        if len(self.dims) == 0:
            return True
        else:
            return False

    def get_actions(self) -> list:
        """
        Obtiene una lista de acciones que se pueden realizar a este estado

        Returns:
            List[State]: Retorna una lista de estados
        """
        actions = []
        for dim in self.dims:
            for plank, _ in enumerate(self.planks):
                action = Action(plank, dim)
                # TODO: use function of pseudo transition. Current function
                #   creates a new instance which takes time
                # new_state = self.transition(action)
                if self.is_valid_transition(action): # new_state.is_valid():
                    actions.append(action)

        if len(actions) > 0:
            return actions
        else:  # si no hay acciones validas se agrega una tabla
            self.planks.append(self.pl)
            self.cuts.append([])
            if len(self.planks) < self.ub:  # previene loop infinito
                return self.get_actions()
            else:
                return []

    def is_valid_transition(self, action: Action) -> bool:
        # Aplicando accion
        if self.planks[action.plank] <= action.cut:
            return True
        return False

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
            new_state.bf += 1

        return new_state

    def wf(self):
        w = 0
        for i in self.planks:
            sobra = (i / self.pl) * 100
            w += sobra ** 3
        return w / 10000

    # se define el operador '<' para los estados, donde un operador con mayor numero de best fits 
    # será menor que otro con menor número, está al revés por temas de la cola con prioridad, 
    # mayor bf, mayor prioridad
    def __lt__(self, other: State):
        # selfPriority = self.bf
        # otherPriority = other.bf
        # return selfPriority > otherPriority
        if len(self.planks) != len(other.planks):
            return len(self.planks) > len(other.planks)

        if self.bf != other.bf:
            return self.bf > other.bf

        return self.wf() < other.wf()
