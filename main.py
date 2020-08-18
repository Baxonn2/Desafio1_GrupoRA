from typing import List, Dict
from copy import deepcopy as copy


class Plank:

    # Dimension de la tabla (En milimetros)
    dim: int

    # Lista de cortes
    cuts: List[int]

    # Dimension cortada
    dim_ripped: int

    def __init__(self, dim: int):
        self.dim = dim
        self.dim_ripped = 0
        self.cuts = []

    def add_cut(self, dim: int) -> bool:
        if dim + self.dim_ripped > self.dim:
            return False
        self.dim_ripped += dim
        self.cuts.append(dim)
        return True


class Action:

    # Identificador de la tabla
    id_plank: int

    # Dimension del corte
    dimension_cut: int

    def __init__(self, dimension_corte: int, id_plank: int):
        self.dimension_corte = dimension_corte
        self.id_plank = id_plank


class State:

    # Lista de cortes por hacer
    dimensions: List[int]

    # Lista de tables
    planks: Dict[int, Plank]

    def __init__(self):
        self.plank = []

    def transition(self, action: Action):

        pass


def get_actions(state: State) -> List[Action]:
    posibles_cortes = state.dimensions
    pass


def is_valid_action(state: State, action: Action) -> bool:
    st = copy(state)
    plank = st.planks[action.plank_id]
    return plank.add_cut(action.dimension_cut)


def is_final_state(state: State) -> bool:
    return len(state.dimensions) == 0


def main():
    state = State()
    pass


if __name__ == "__main__":
    main()
