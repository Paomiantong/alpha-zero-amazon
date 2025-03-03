#pragma once

#include <atomic>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

#include <amazon.h>
#include <libtorch.h>
#include <thread_pool.h>

class TreeNode {
public:
  // friend class can access private variables
  friend class MCTS;

  TreeNode();
  TreeNode(const TreeNode &node);
  TreeNode(TreeNode *parent, double p_sa);

  TreeNode &operator=(const TreeNode &p);

  unsigned int select(double c_puct, double c_virtual_loss);
  void expand(const std::vector<double> &action_priors);
  void backup(double leaf_value);

  double get_value(double c_puct, double c_virtual_loss,
                   unsigned int sum_n_visited) const;
  inline bool get_is_leaf() const { return this->is_leaf; }

private:
  // store tree
  TreeNode *parent;
  std::unordered_map<unsigned int, TreeNode *> children;
  bool is_leaf;
  std::mutex lock;

  std::atomic<unsigned int> n_visited;
  double p_sa;
  double q_sa;
  std::atomic<int> virtual_loss;
};

class MCTS {
public:
  MCTS(NeuralNetwork *neural_network, unsigned int thread_num, double c_puct,
       unsigned int num_mcts_sims, double c_virtual_loss,
       unsigned int action_size);
  std::vector<double> get_action_probs(Amazon *amazon, double temp = 1e-3);
  void update_with_move(int last_move);

private:
  void simulate(std::shared_ptr<Amazon> game);
  static void tree_deleter(TreeNode *t);

  // variables
  std::unique_ptr<TreeNode, decltype(MCTS::tree_deleter) *> root;
  std::unique_ptr<ThreadPool> thread_pool;
  NeuralNetwork *neural_network;

  unsigned int action_size;
  unsigned int num_mcts_sims;
  double c_puct;
  double c_virtual_loss;
};
