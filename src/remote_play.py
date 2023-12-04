import asyncio
import numpy as np
import websockets

from library import MCTS, Amazon, NeuralNetwork
from convert import fix_hex, hex_to_move


class GameManager:
    amazon: Amazon
    player: MCTS
    nn: NeuralNetwork
    first_hand: int

    def __init__(self, model_path: str) -> None:
        self.actions = [self.new_game, self.execute_move, self.first]
        self.model_path = model_path
        self.nn = NeuralNetwork(model_path, True, 12)
        pass

    def new_game(self, f: int) -> None:
        self.first_hand = f
        self.amazon = Amazon(f)
        self.player = MCTS(self.nn, 12, 5, 9600, 3, 20736)

    def execute_move(self, move: int) -> int:
        request_move = hex_to_move(self.amazon, move)
        self.amazon.execute_move(request_move)
        self.player.update_with_move(request_move)
        print(f"{move:6x}", request_move)
        self.amazon.display()
        print("=" * 20)

        prob = self.player.get_action_probs(self.amazon)
        best_move = int(np.argmax(np.array(list(prob))))
        self.amazon.execute_move(best_move)
        self.player.update_with_move(best_move)
        response_move = fix_hex(self.amazon.get_last_move())
        print(f"{response_move}")
        self.amazon.display()
        print("=" * 20)

        return f"01{response_move}"

    def first(self, _: int):
        prob = self.player.get_action_probs(self.amazon)
        best_move = int(np.argmax(np.array(list(prob))))
        self.amazon.execute_move(best_move)
        self.player.update_with_move(best_move)
        response_move = fix_hex(self.amazon.get_last_move())
        print(f"{response_move}")
        self.amazon.display()
        print("=" * 20)

        return f"01{response_move}"

    def execute(self, cmd: str) -> None:
        if len(cmd) < 3:
            return None
        action = self.actions[int(cmd[:2])]
        return action(int(cmd[2:]))


async def handler(websocket):
    mgr = GameManager("../test/models/best_checkpoint.pt")
    while True:
        try:
            cmd = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        print(f"CMD:{cmd}")
        ret = mgr.execute(cmd)
        if ret is not None:
            await websocket.send(ret)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
