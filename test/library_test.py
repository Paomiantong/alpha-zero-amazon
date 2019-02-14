# coding: utf-8
import os
import sys
sys.path.append('../build')

from library import Gomoku, MCTS
import numpy as np
import time


if __name__ == "__main__":
    gomoku = Gomoku(10, 5, 1)
    gomoku.execute_move(0)
    gomoku.execute_move(99)
    gomoku.execute_move(1)
    gomoku.execute_move(98)
    gomoku.execute_move(2)
    gomoku.execute_move(97)
    gomoku.execute_move(3)
    gomoku.execute_move(96)

    gomoku.display()

    mcts = MCTS("./models/checkpoint.pt", 4, 1.5, 1600, 0.5, 100, True)

    print("RUNNING")
    while True:
        time_start=time.time()
        res = mcts.get_action_probs(gomoku, 1)
        time_end=time.time()
        print('get_action_probs', time_end - time_start)

        print(list(res))
        best_action = int(np.argmax(np.array(list(res))))
        print(best_action)

        mcts.update_with_move(-1)
