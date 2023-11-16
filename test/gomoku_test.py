import sys
sys.path.append('../src')
import library

amz = library.Amazon(1)
amz.execute_move(153 + 5184 * 0)
amz.execute_move(9 + 5184 * 1)
amz.execute_move(3321 + 5184 * 1)
amz.execute_move(9 + 5184 * 1)
amz.execute_move(3465 + 5184 * 2)
amz.execute_move(9 + 5184 * 1)
amz.execute_move(153 + 5184 * 3)
amz.execute_move(369 + 5184 * 1)
amz.execute_move(3249 + 5184 * 3)
amz.execute_move(9 + 5184 * 2)
amz.execute_move(1989 + 5184 * 3)
amz.display()
print(amz.get_game_status())