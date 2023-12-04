import numpy as np

from view_server.move_map import MOVE_MAP


class Board(object):
    """board for the game"""

    def __init__(self):
        self.last_move = None
        self.current_player = None
        # board states,
        self.states = np.array([[0 for _ in range(10)] for _ in range(10)])
        self.turns = 0
        self.players = [1, 2]  # player1(black) and player2(white)
        self.first_hand = 0

    def init_board(self, start_player=0):
        self.states[:, :] = 0
        self.turns = 0
        # 白
        self.states[3, 0] = 2
        self.states[0, 3] = 2
        self.states[0, 6] = 2
        self.states[3, 9] = 2
        # 黑
        self.states[6, 0] = 1
        self.states[9, 3] = 1
        self.states[9, 6] = 1
        self.states[6, 9] = 1

        self.current_player = self.players[start_player]  # start player
        self.first_hand = self.current_player
        self.last_move = None

    def do_move(self, move):
        ind = move // 5184
        act = MOVE_MAP[move % 5184]
        ctr = 0
        for i in range(10):
            for j in range(10):
                if self.states[i, j] == self.current_player:
                    if ctr == ind:
                        t_i = i + act[0][0]
                        t_j = j + act[0][1]
                        s_i = t_i + act[1][0]
                        s_j = t_j + act[1][1]
                        self.states[t_i, t_j] = self.states[i, j]
                        self.states[i, j] = 0
                        self.states[s_i, s_j] = 3

                        self.last_move = ((i, j), (t_i, t_j), (s_i, s_j))
                        self.current_player = (
                                self.players[0] if self.current_player == self.players[1]
                                else self.players[1])
                        self.turns += 1
                        return
                    ctr += 1
        pass

    @property
    def draw_seq(self):
        seq = ''
        for i in range(10):
            for j in range(10):
                seq += str(self.states[i, j])
        return seq
