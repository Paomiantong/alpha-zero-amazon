import asyncio
import json
import threading
import time

import websockets

from view_server.board import Board


class ViewServer:
    loop: asyncio.AbstractEventLoop
    cond: asyncio.Condition

    def __init__(self):
        super().__init__()
        self.board = Board()
        self.board.init_board()

    async def send(self, websocket):
        while True:
            async with self.cond:
                try:
                    await asyncio.wait_for(self.cond.wait(), 5)
                except asyncio.exceptions.TimeoutError:
                    print("Send draw event")
                finally:
                    try:
                        await websocket.send(
                            json.dumps(
                                {"event": "board/draw", "data": self.board.draw_seq}
                            )
                        )
                    except websockets.ConnectionClosed:
                        break

    async def recv(self, websocket):
        while True:
            try:
                # 接收消息
                message = await websocket.recv()
                # 处理接收到的消息
                obj = json.loads(message)
            except websockets.ConnectionClosed:
                break

    async def main(self, websocket, path):
        await websocket.send(
            json.dumps({"event": "board/draw", "data": self.board.draw_seq})
        )
        # 创建send()和recv()的任务
        send_task = asyncio.create_task(self.send(websocket))
        recv_task = asyncio.create_task(self.recv(websocket))
        # 等待这两个任务完成
        await asyncio.gather(send_task, recv_task)

    def run(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.cond = asyncio.Condition()
        # 启动服务器
        start_server = websockets.serve(self.main, "0.0.0.0", 8888)
        print("Server Start")
        # 启动事件循环
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()

    def stop(self):
        try:
            self.loop.stop()
        except:
            print("Server Stop")

    async def notify(self):
        async with self.cond:
            self.cond.notify_all()

    def execute_move(self, move):
        self.board.do_move(move)
        asyncio.run_coroutine_threadsafe(self.notify(), self.loop)

    def reset_status(self, first_hand):
        self.board.init_board(first_hand - 1)
        asyncio.run_coroutine_threadsafe(self.notify(), self.loop)


if __name__ == "__main__":
    server = ViewServer()
    t = threading.Thread(target=server.run)
    t.start()
    time.sleep(3)
    ctr = 0
    while ctr < 3:
        for i in range(5):
            server.execute_move(1)
            time.sleep(2)
        server.reset_status(1)
        ctr += 1
    server.stop()
