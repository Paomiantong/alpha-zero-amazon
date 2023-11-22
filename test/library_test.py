# -*- coding: utf-8 -*-
import os
import sys

sys.path.append('../src')
from library import Amazon, MCTS, NeuralNetwork
import numpy as np
import time
import concurrent.futures

os.environ['CUDA_VISIBLE_DEVICES'] = '1'

def test(nn):
    gomoku = Amazon(1)
    mcts = MCTS(nn, 4, 5, 400, 3, gomoku.get_action_size())
    while True:
        # time_start = time.time()
        res = mcts.get_action_probs(gomoku, 1)
        # time_end = time.time()
        # print('get_action_probs', time_end - time_start)

        # print(list(res))
        best_action = int(np.argmax(np.array(list(res))))
        # print(best_action, res[best_action])
        
        gomoku.execute_move(best_action)
        mcts.update_with_move(best_action)

        ended, winner = gomoku.get_game_status()
        if ended:
            print(f"Done, Winner: {winner}")
            mcts.update_with_move(-1)
            return winner
            # gomoku.reset()
    
if __name__ == "__main__":
    print("RUNNING")
    
    while True:
        nn = NeuralNetwork("./models/best_checkpoint.pt", True, 40)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(test, nn) for _ in
                       range(10)]
            for k, f in enumerate(futures):
                examples = f.result()
                print("Done: {}, Winner: {}".format(k + 1, examples))
        # test(nn)
        del nn
        time.sleep(5)