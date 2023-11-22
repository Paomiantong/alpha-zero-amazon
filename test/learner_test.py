# coding: utf-8
import sys
import traceback

sys.path.append('..')
sys.path.append('../src')

import learner
from message import push
import config

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["train", "play"]:
        print("[USAGE] python leaner_test.py train|play")
        exit(1)

    alpha_zero = learner.Leaner(config.config)

    if sys.argv[1] == "train":
        push('Start', 'Train start')
        try:
            alpha_zero.learn()
        except:
            exc = traceback.format_exc()
            print(exc)
            push('Error', exc)
        push('End', 'Train end')
    elif sys.argv[1] == "play":
        for i in range(10):
            print("GAME: {}".format(i + 1))
            alpha_zero.play_with_human(human_first=i % 2)
