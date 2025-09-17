# 代码生成时间: 2025-09-17 09:20:28
import psutil
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# 创建Dash应用
app = dash.Dash(__name__)

# 定义Dash应用布局
app.layout = html.Div([
    html.H1("系统性能监控"),
    dcc.Graph(id='cpu-usage-graph'),
    dcc.Graph(id='memory-usage-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # 刷新间隔 1000 毫秒（1 秒）
        n_intervals=0
    ),
])

# 回调函数，更新CPU使用率图
@app.callback(
    Output('cpu-usage-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_cpu_usage(n):
    # 获取CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    # 创建图形
    fig = {'data': [{'x': [1], 'y': [cpu_usage], 'type': 'bar', 'name': 'CPU Usage'}],
           'layout': {'title': 'CPU使用率'}}
    return fig

# 回调函数，更新内存使用率图
@app.callback(
    Output('memory-usage-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_memory_usage(n):
    # 获取内存使用率
    memory_usage = psutil.virtual_memory().percent
    # 创建图形
    fig = {'data': [{'x': [1], 'y': [memory_usage], 'type': 'bar', 'name': 'Memory Usage'}],
           'layout': {'title': '内存使用率'}}
    return fig

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)