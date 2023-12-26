import json
from datetime import datetime

EVENT_DIC = {}


def response(event_type):
    def decorator(func):
        def wrapper(*arg, **kvarg):
            event_data = func(*arg, **kvarg)
            return json.dumps({"event": event_type, "data": event_data})

        return wrapper

    return decorator


def requset(event_type):
    def decorator(func):
        EVENT_DIC[event_type] = func

    return decorator


def handle_request(event_obj, server):
    try:
        EVENT_DIC[event_obj["event"]](event_obj["data"], server)
    except Exception as e:
        print(e)


@response("board/update")
def BoardDrawEvent(board):
    return {
        "board": board.draw_seq,
        "last_move": board.last_move,
        "history": board.history,
        "view_only": board.view_only,
        "current_color": board.current_player,
        "turns": board.turns,
        "time": datetime.now().timestamp(),
    }


@response("notify")
def NotificationEvent(msg, type="info"):
    print(msg, type)
    return {"message": msg, "type": type}


@requset("board/execute")
def BoardExecuteEvent(data, server):
    server.board.view_only = True
    server.move_queue.put(data)
