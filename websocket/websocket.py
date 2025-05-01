import threading
import time

import websocket
from config import TREE_NEWS_API_KEY, WS_URLS


def init_connections(on_message):
    threads = []
    for ws_url in WS_URLS:
        thread = threading.Thread(target=start_ws, args=(ws_url, on_message))
        thread.daemon = True
        thread.start()
        threads.append(thread)

def start_ws(url, on_message):
    while True:  # Reconnection loop
        ws = websocket.WebSocketApp(
            url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        print(f"Attempting to connect to {url}")
        try:
            ws.run_forever()
        except Exception as e:
            print(f"Unexpected error: {e}")
        print(f"Connection lost. Reconnecting to {url} in 5 seconds...")
        time.sleep(5)  # Wait before reconnecting

def on_open(ws):
    print(f"✅ Connected to WebSocket {ws.url}")
    auth_message = f"login {TREE_NEWS_API_KEY}"
    ws.send(auth_message)

def on_error(ws, error):
    print(f"WebSocket Error ({ws.url}): {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket Closed ({ws.url})")