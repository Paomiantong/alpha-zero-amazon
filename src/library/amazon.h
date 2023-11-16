#pragma once

#include <tuple>
#include <vector>

constexpr static int moveDirects[8][2] = {
    {0, 1},  // 上
    {0, -1}, // 下
    {1, -1}, // 右上
    {1, 0},  // 右
    {1, 1},  // 右下
    {-1, 0}, // 左
    {-1, 1}, // 左下
    {-1, -1} // 左上
};

constexpr static int Multiplier[2][2] = {{648, 72}, {9, 1}};

#define THIS_POS_I __i
#define THIS_POS_J __j

#define DIVERT_DIRECT(i, j, idx)                                               \
  int THIS_POS_I = i + moveDirects[idx][0], THIS_POS_J = j + moveDirects[idx][1]

#define FORWARD(i)                                                             \
  THIS_POS_I += moveDirects[i][0];                                             \
  THIS_POS_J += moveDirects[i][1]

#define THIS_POS(chessBoard) (chessBoard[THIS_POS_I][THIS_POS_J])

class Amazon {
public:
  using move_type = int;
  using board_type = std::vector<std::vector<int>>;

  Amazon(int first_color);

  bool has_legal_moves(int color);
  std::vector<int> get_legal_moves();
  void execute_move(move_type move);
  std::vector<int> get_game_status();
  void display() const;
  void reset();

  inline unsigned int get_action_size() const { return 20736; }
  inline board_type get_board() const { return this->board; }
  inline move_type get_last_move() const { return this->last_move; }
  inline int get_current_color() const { return this->cur_color; }
  inline bool first_hand_now() const {
    return this->cur_color == this->first_hand;
  }

private:
  void resort_amazon_pos();

private:
  board_type board; // game borad
  // store the 4 amazoms positon
  unsigned char amazon_pos[2][4][2]{{{6, 0}, {6, 9}, {9, 3}, {9, 6}},
                                    {{0, 3}, {0, 6}, {3, 0}, {3, 9}}};
  int cur_color; // current player's color 1:Black and 2:White
  int first_hand;
  move_type last_move;    // last move
};
