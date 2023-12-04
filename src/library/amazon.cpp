#include <algorithm>
#include <cstring>
#include <iostream>
#include <math.h>
#include <queue>

#include "move_map.h"
#include <amazon.h>

Amazon::Amazon(int first_color)
    : cur_color(first_color), first_hand(first_color), last_move(-1) {
  this->board = std::vector<std::vector<int>>(10, std::vector<int>(10, 0));
  // 黑
  this->board[6][0] = 1;
  this->board[9][3] = 1;
  this->board[9][6] = 1;
  this->board[6][9] = 1;
  // 白
  this->board[3][0] = 2;
  this->board[0][3] = 2;
  this->board[0][6] = 2;
  this->board[3][9] = 2;
}

// Done: 获取合法走法
std::vector<int> Amazon::get_legal_moves() {
  int depth = 0;
  int ctr = 0;
  //   int mov_ctr = 0;
  std::queue<std::pair<int, int>> que;
  std::vector<int> legal_moves(this->get_action_size(), 0);
  // 找到4个棋子
  for (unsigned int k = 0; k < 4; k++) {
    auto pos = amazon_pos[cur_color - 1][k];
    que.push({pos[0] * 10 + pos[1] + k * 518400, (pos[0] << 4) + pos[1]});
  }
  // 寻找所有合法走法
  que.push({-1, 0});
  while (!que.empty()) {
    const auto &front = que.front();
    const int id = front.first, mv = front.second;
    que.pop();
    // 计算深度
    if (id == -1) {
      depth++;
      if (!que.empty())
        que.push({-1, 0});
      continue;
    }
    // 解析
    const int start = id / 100;
    const int pos = id % 100;
    const int i = pos / 10, j = pos % 10;
    // 模拟走步
    if (depth == 1) {
      int f_i = (mv & 0xf000) >> 12, f_j = (mv & 0x0f00) >> 8;
      this->board[i][j] = this->board[f_i][f_j];
      this->board[f_i][f_j] = 0;
    }
    // 记录
    if (depth == 2) {
      //   mov_ctr++;
      legal_moves[start] = 1;
      continue;
    }
    // 遍历8个方向
    for (int t = 0; t < 8; ++t) {
      DIVERT_DIRECT(i, j, t);
      if (THIS_POS_I < 0 || THIS_POS_I > 9 || THIS_POS_J < 0 || THIS_POS_J > 9)
        continue;

      ctr = 0;
      while (THIS_POS(this->board) == 0) {
        int _idx =
            start + t * Multiplier[depth][0] + ctr * Multiplier[depth][1];
        int new_value = THIS_POS_I * 10 + THIS_POS_J + _idx * 100;
        que.push({new_value, (mv << 8) + (THIS_POS_I << 4) + THIS_POS_J});
        FORWARD(t);
        ctr++;
        if (THIS_POS_I < 0 || THIS_POS_I > 9 || THIS_POS_J < 0 ||
            THIS_POS_J > 9)
          break;
      }
    }
    // 撤销走步
    if (depth == 1) {
      int f_i = (mv & 0xf000) >> 12, f_j = (mv & 0x0f00) >> 8;
      this->board[f_i][f_j] = this->board[i][j];
      this->board[i][j] = 0;
    }
  }
  //   std::cout << mov_ctr << std::endl;
  return legal_moves;
}

// Done: 是否有合法走法
bool Amazon::has_legal_moves(int color) {
  for (unsigned int k = 0; k < 4; k++) {
    auto pos = amazon_pos[color - 1][k];
    // 遍历8个方向
    for (int t = 0; t < 8; ++t) {
      DIVERT_DIRECT(pos[0], pos[1], t);
      if (THIS_POS_I < 0 || THIS_POS_I > 9 || THIS_POS_J < 0 || THIS_POS_J > 9)
        continue;
      if (THIS_POS(this->board) == 0)
        return true;
    }
  }
  return false;
}

void Amazon::resort_amazon_pos() {
  auto amzs = amazon_pos[cur_color - 1];
  unsigned char tmp_i, tmp_j;
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3 - i; j++) {
      if (((amzs[j][0] - amzs[j + 1][0]) * 10 + (amzs[j][1] - amzs[j + 1][1])) >
          0) {
        tmp_i = amzs[j][0];
        tmp_j = amzs[j][1];
        amzs[j][0] = amzs[j + 1][0];
        amzs[j][1] = amzs[j + 1][1];
        amzs[j + 1][0] = tmp_i;
        amzs[j + 1][1] = tmp_j;
      }
    }
  }
}

// Done: 执行走法
void Amazon::execute_move(move_type move) {
  auto amz = amazon_pos[cur_color - 1][move / 5184];
  auto act = move_map[move % 5184];
  // calc pos
  int i = amz[0], j = amz[1];
  int t_i = i + act[0][0], t_j = j + act[0][1];
  int s_i = t_i + act[1][0], s_j = t_j + act[1][1];
  // execute move
  board[t_i][t_j] = board[i][j];
  board[i][j] = 0;
  board[s_i][s_j] = 3;
  // -update amazon pos
  amz[0] = t_i;
  amz[1] = t_j;
  resort_amazon_pos();
  // save last move
  this->last_move =
      (i << 20) | (j << 16) | (t_i << 12) | (t_j << 8) | (s_i << 4) | s_j;
  // change player
  this->cur_color = this->cur_color % 2 + 1;
}

// Done: 获取游戏状态
std::vector<int> Amazon::get_game_status() {
  // return (is ended, winner)
  if (!this->has_legal_moves(1)) {
    return {1, 2};
  } else if (!this->has_legal_moves(2)) {
    return {1, 1};
  } else {
    return {0, 0};
  }
}

static inline char number2char(int num) {
  switch (num) {
  case 1:
    return 'X';
  case 2:
    return 'O';
  case 3:
    return '#';
  default:
    return '-';
  }
}

void Amazon::display() const {
  for (unsigned int i = 0; i < 10; i++) {
    for (unsigned int j = 0; j < 10; j++) {
      std::cout << number2char(this->board[i][j]) << ", ";
    }
    std::cout << std::endl;
  }
}

void Amazon::reset() {
  unsigned char tmp[2][4][2]{{{6, 0}, {6, 9}, {9, 3}, {9, 6}},
                             {{0, 3}, {0, 6}, {3, 0}, {3, 9}}};
  memcpy(this->amazon_pos, tmp, sizeof(tmp));
  cur_color = first_hand;
  last_move = -1;
  this->board = std::vector<std::vector<int>>(10, std::vector<int>(10, 0));
  // 黑
  this->board[6][0] = 1;
  this->board[9][3] = 1;
  this->board[9][6] = 1;
  this->board[6][9] = 1;
  // 白
  this->board[3][0] = 2;
  this->board[0][3] = 2;
  this->board[0][6] = 2;
  this->board[3][9] = 2;
}

int Amazon::get_amazon_ind(int i, int j) {
  auto amzs = amazon_pos[cur_color - 1];
  for (int ind = 0; ind < 4; ind++) {
    if (i == amzs[ind][0] && j == amzs[ind][1])
      return ind;
  }
  return -1;
}