class StateMenuBase:
    """Base class to manage states and transitions for different menus."""

    def __init__(self):
        self._states = []
        self._transitions = []

    @property
    def states(self):
        """
        Returns the list of all states for the menu.
        """
        return self._states

    @property
    def transitions(self):
        """
        Returns the list of all transitions for the menu.
        """
        return self._transitions
