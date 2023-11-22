#include <iostream>
#include <libtorch.h>
#include <mcts.h>
#include <unistd.h>

int main() {
  auto g = std::make_shared<Amazon>(1);
  //   g->execute_move(12);
  //   g->execute_move(13);
  //   g->execute_move(14);
  //   g->execute_move(15);
  //   g->execute_move(16);
  //   g->execute_move(17);
  //   g->execute_move(18);
  //   g->execute_move(19);
  g->display();

  NeuralNetwork nn("../models/best_checkpoint.pt", true, 40);

  MCTS *m = new MCTS(&nn, 4, 5, 400, 3, g->get_action_size());

  std::cout << "RUNNING" << std::endl;

  //   while (true) {
  auto res = m->get_action_probs(g.get(), 0.001);
  int best_move = find(res.begin(), res.end(), 1) - res.begin();
  g->execute_move(best_move);
  std::cout << best_move << std::endl;
  // std::for_each(res.begin(), res.end(),
  //               [](double x) { std::cout << x << ","; });
  // std::cout << std::endl;
  m->update_with_move(best_move);
  // g->display();
  // std::cout << "Cur color:" << g->get_current_color()
  //           << "\n lastmove:" << std::hex << g->get_last_move() <<
  //           std::endl;
  auto status = g->get_game_status();
  if (status[0]) {
    std::cout << "Done" << std::endl;
    g.reset(new Amazon(1));
    delete m;
    m = new MCTS(&nn, 4, 5, 1600, 3, g->get_action_size());
    sleep(2);
  }
  //   }

  return 0;
}
