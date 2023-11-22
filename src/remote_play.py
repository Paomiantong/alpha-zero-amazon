import asyncio
from datetime import datetime
import websockets


async def handler(websocket):
    async for message in websocket:
        reply = f'Data received as "{message}".  time: {datetime.now()}'
        print(reply)
        await websocket.send(reply)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
