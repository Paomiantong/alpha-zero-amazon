#include <amazon.h>
#include <iostream>
#include <vector>

int main() {
  Amazon gomoku(1);

  // test execute_move
  gomoku.execute_move(153 + 5184 * 0);
  //   gomoku.execute_move(9 + 5184 * 0); //
  //   gomoku.execute_move(3321 + 5184 * 2);
  //   gomoku.execute_move(9 + 5184 * 1); //
  //   gomoku.execute_move(3465 + 5184 * 3);
  //   gomoku.execute_move(9 + 5184 * 1); //
  //   gomoku.execute_move(153 + 5184 * 0);
  //   gomoku.execute_move(369 + 5184 * 2); //
  //   gomoku.execute_move(3249 + 5184 * 3);
  //   gomoku.execute_move(9 + 5184 * 2); //
  //   gomoku.execute_move(1989 + 5184 * 3);
  // test display
  gomoku.display();

  // test get_xxx
  std::cout << gomoku.get_action_size() << std::endl;
  std::cout << gomoku.get_current_color() << std::endl;

  std::cout << gomoku.get_last_move() << std::endl;

  int i, j;
  for (int k = gomoku.get_last_move(); k != 0; k >>= 8) {
    i = (k & 0xf0) >> 4;
    j = k & 0x0f;
    std::cout << i << "," << j << std::endl;
  }

  // test has_legal_moves
  std::cout << gomoku.has_legal_moves(1) << std::endl;

  // test get_legal_moves
  auto legal_moves = gomoku.get_legal_moves();
  //   for (unsigned int i = 0; i < legal_moves.size(); i++) {
  //     std::cout << legal_moves[i] << ", ";
  //   }
  std::cout << std::endl;

  // test get_game_status
  auto game_status = gomoku.get_game_status();
  std::cout << game_status[0] << ", " << game_status[1] << std::endl;

  gomoku.reset();
  legal_moves = gomoku.get_legal_moves();
  gomoku.display();
//   gomoku.execute_move(0);
  for (unsigned int i = 0; i < legal_moves.size(); i++) {
    if (legal_moves[i] == 1) {
      std::cout << i << ",";
      gomoku.execute_move(i);
      gomoku.reset();
    }
  }
}
