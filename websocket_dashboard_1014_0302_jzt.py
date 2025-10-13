# 代码生成时间: 2025-10-14 03:02:23
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_websocket as dsw
import threading
import queue

# WebSocket客户端管理器
class WebSocketClientManager:
    def __init__(self):
        self.clients = []
        self.lock = threading.Lock()

    def register(self, client_id):
        with self.lock:
            self.clients.append(client_id)

    def unregister(self, client_id):
        with self.lock:
            self.clients.remove(client_id)

    def broadcast(self, message):
        with self.lock:
            for client in self.clients:
                yield client, message

    def size(self):
        with self.lock:
            return len(self.clients)

# 管理WebSocket客户端
client_manager = WebSocketClientManager()

# WebSocket的回调函数
@app.callback(
    Output('my-websocket', 'send'),
    [Input('send-button', 'n_clicks'),
     Input('my-websocket', 'message')],
    [State('input-message', 'value')]
)
def send_message(n_clicks, message, client_id):
    if n_clicks is None:
        return
    elif message is not None:
        message = message
    else:
        message = client_id
    client_manager.register(client_id)
    yield message
    client_manager.broadcast(message)
    client_manager.unregister(client_id)

# 处理接收到的消息
@app.callback(
    Output('output-data', 'children'),
    [Input('my-websocket', 'message')]
)
def display_message(message):
    if message is not None:
        return message['content']
    return 'No message yet'

# 定义Dash应用程序
app = dash.Dash(__name__)
server = app.server

# 添加WebSocket支持
dsw.WebSocket(app, server, websocket_route="/my-websocket")

# 设计界面布局
app.layout = html.Div([
    html.H1("WebSocket Dashboard"),
    dcc.Textarea(
        id='input-message',
        placeholder='Type a message...',
        debounce=True
    ),
    html.Button("Send", id="send-button"),
    dsw.WebSocket(
        id='my-websocket',
        type="websocket"
    ),
    html.Div(id='output-data')
])

if __name__ == '__main__':
    app.run_server(debug=True)