from Dots_and_Boxes import Dots_and_Boxes
from GameAction import GameAction


class CPU:
    """
    An interface for CPU player.
    """

    def get_action(self, game: Dots_and_Boxes) -> GameAction:
        """
        Returns action based on state.
        """
        raise NotImplementedError()
