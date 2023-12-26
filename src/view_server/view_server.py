import asyncio
import json
from queue import Queue

import websockets

from view_server.board import Board
import view_server.event as vs_event


class ViewServer:
    loop: asyncio.AbstractEventLoop
    cond: asyncio.Condition
    stop_future: asyncio.Future
    move_queue: Queue
    event_queue: asyncio.Queue

    def __init__(self):
        super().__init__()
        self.board = Board()
        self.board.init_board()
        self.move_queue = Queue()
        self.running = False

    async def event_loop(self):
        while self.running:
            try:
                event = await asyncio.wait_for(self.event_queue.get(), 5)
            except asyncio.TimeoutError:
                event = (vs_event.BoardDrawEvent, (self.board,))
            finally:
                async with self.cond:
                    self.event = event
                    self.cond.notify_all()

    async def send(self, websocket):
        while True:
            async with self.cond:
                await self.cond.wait()
                try:
                    event_type, event_args = self.event
                    await websocket.send(event_type(*event_args))
                except websockets.ConnectionClosed:
                    break
                except Exception as e:
                    # 其他异常的处理
                    print(f"Error in sending message: {e}")
                    await websocket.send(
                        vs_event.NotificationEvent(f"Error in sending message: {e}")
                    )

    async def recv(self, websocket):
        while True:
            try:
                # 接收消息
                message = await websocket.recv()
                # 处理接收到的消息
                obj = json.loads(message)
                vs_event.handle_request(obj, self)
            except websockets.ConnectionClosed:
                break

    async def handle_connection(self, websocket, path):
        await websocket.send(vs_event.BoardDrawEvent(self.board))
        # 创建send()和recv()的任务
        send_task = asyncio.create_task(self.send(websocket))
        recv_task = asyncio.create_task(self.recv(websocket))
        # 等待这两个任务完成
        await asyncio.gather(send_task, recv_task)

    async def start_server(self):
        self.stop_future = asyncio.Future()
        print("Server Start")
        self.running = True
        async with websockets.serve(self.handle_connection, "0.0.0.0", 8888):
            await self.stop_future
        print("Server Stop")

    def run(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.event_queue = asyncio.Queue()
        self.cond = asyncio.Condition()
        # 启动服务器
        self.loop.run_until_complete(
            asyncio.gather(self.start_server(), self.event_loop())
        )
        self.loop.close()

    def stop(self):
        self.running = False
        self.stop_future.set_result(True)
        try:
            asyncio.run_coroutine_threadsafe(self.notify(), self.loop)
        except Exception as e:
            print(f"Server Stop Failed: {e}")

    async def notify(self):
        async with self.cond:
            self.cond.notify_all()

    def dispatch_event(self, event, *args):
        packed_event = (event, args)
        asyncio.run_coroutine_threadsafe(self.event_queue.put(packed_event), self.loop)

    def execute_move(self, move):
        self.board.do_move(move)
        self.dispatch_event(vs_event.BoardDrawEvent, self.board)

    def reset_status(self, first_hand):
        self.board.init_board(first_hand - 1)
        self.dispatch_event(vs_event.BoardDrawEvent, self.board)

    def notification(self, message, type):
        self.dispatch_event(vs_event.NotificationEvent, message, type)

    def notify_human(self):
        self.board.view_only = False
        self.dispatch_event(vs_event.BoardDrawEvent, self.board)

    def get_human_move(self):
        return self.move_queue.get()
