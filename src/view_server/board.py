import numpy as np


class Board(object):
    """board for the game"""

    def __init__(self):
        self.last_move = None
        self.current_player = None
        # board states,
        self.states = np.array([[0 for _ in range(10)] for _ in range(10)])
        self.history = []
        self.turns = 0
        self.players = [1, 2]  # player1(black) and player2(white)
        self.first_hand = 0
        self.view_only = True

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
        self.history.clear()

    def do_move(self, move):
        k = move
        ctr = 0
        move_array = []  # arrow,to,from
        while ctr < 3:
            i = (k & 0xF0) >> 4
            j = k & 0x0F
            move_array.append((i, j))
            k >>= 8
            ctr += 1

        self.states[move_array[1]] = self.states[move_array[2]]
        self.states[move_array[2]] = 0
        self.states[move_array[0]] = 3

        self.last_move = move_array
        self.current_player = (
            self.players[0]
            if self.current_player == self.players[1]
            else self.players[1]
        )
        self.turns += 1
        self.history.append(move_array)
        pass

    @property
    def draw_seq(self):
        seq = ""
        for i in range(10):
            for j in range(10):
                seq += str(self.states[i, j])
        return seq
