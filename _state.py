from abc import ABC, abstractmethod


class BaseState(ABC):

    """
    Base class to create new states. Defines the methods
    transition, get_actions, is_valid and is_final as
    required methods to implement in the child classes.
    """

    def __init__(self, visited: bool = False):
        self.visited = visited

    def visit(self):
        """
        Sets the status of visited to True for a state.

        :return: None
        """
        self.visited = True

    def is_visited(self):
        """
        Check if the status of visited is true for the current
        state

        :return: True if the state was visited, False in other case
        """
        return self.visited

    @abstractmethod
    def transition(self, action):
        """
        Creates a new states from the current state and an action

        :return: New instance of the parent state.
        """
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Check if the current state is valid according to the restrictions given.

        :return: True if the restrictions are satisfied.
        """
        pass

    @abstractmethod
    def get_actions(self) -> list:
        """
        Returns an ensemble of possible actions to create a new state based on
        the current one

        :return: iterable of
        """
        pass

    @abstractmethod
    def is_final(self) -> bool:
        """
        Check if the current state is final.

        :return: True if the state is final.
        """
        pass

