from Dots_and_Boxes import *
from RandomCPU import RandomCPU


if __name__ == "__main__":
    """
    Change game_instance initialization below to change game mode
    PvP mode: game_instance = Dots_and_Boxes(None, None)
    PvB mode: game_instance = Dots_and_Boxes(None, cpuName()) or game_instance = Dots_and_Boxes(cpuName(), None)
    BvB mode: game_instance = Dots_and_Boxes(cpuName(), cpuName())
    """
    game_instance = Dots_and_Boxes(MinMaxCPU(), MinMaxCPU())
    game_instance.mainloop()
