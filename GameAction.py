from typing import NamedTuple, Literal, Tuple


class GameAction(NamedTuple):
    """
    action_type: "row" or "col"
    position: (x: int, y: int)

    action_ype == "row" means a horizonal line needs to be marked,
    vertical for otherwise.
    """

    action_type: Literal["row", "col"]
    position: Tuple[int, int]
