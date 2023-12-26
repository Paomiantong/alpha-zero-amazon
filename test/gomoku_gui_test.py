# -*- coding: utf-8 -*-
import sys

import numpy as np
import threading
import time

sys.path.append("../src")
from view_server import view_server
import library

if __name__ == "__main__":
    gomoku_gui = view_server.ViewServer()
    t = threading.Thread(target=gomoku_gui.run)
    t.start()
    time.sleep(2)

    amz = library.Amazon(1)
    amz.execute_move(153 + 5184 * 0)
    amz.display()
    # test
    gomoku_gui.execute_move(amz.get_last_move())
    # while True:
    #     gomoku_gui.notification("haha", "warn")
    #     time.sleep(2)
    # gomoku_gui.stop()
