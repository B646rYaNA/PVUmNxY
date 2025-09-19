# 代码生成时间: 2025-09-19 08:43:34
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate

# 定义一个函数用于格式化API响应
def format_response(response_data, status_code):
    # 检查状态码是否为200（成功）
    if status_code == 200:
        # 返回成功消息和数据
        return {
            "status": "success",
            "message": "Request successful",
            "data": response_data
        }
    else:
        # 返回错误消息
        return {
            "status": "error",
            "message": f"Request failed with status code {status_code}"
        }

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义应用布局
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("API Response Formatter"),
                md=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(id="api-input", placeholder="Enter API response data..."),
                md=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Format Response", id="submit-button", n_clicks=0),
                md=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Textarea(id="formatted-response", placeholder="Formatted response will appear here..."),
                md=12,
            )
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("formatted-response", "value"),
    [Input("submit-button", "n_clicks")],
    [State("api-input", "value")],
)
def format_api_response(n_clicks, api_input):
    # 如果按钮没有被点击，阻止更新
    if n_clicks <= 0:
        raise PreventUpdate
    
    try:
        # 将输入解析为JSON对象
        response_data = json.loads(api_input)
        # 模拟状态码为200
        status_code = 200
        # 格式化API响应
        formatted_response = json.dumps(format_response(response_data, status_code), indent=4)
    except json.JSONDecodeError as e:
        # 如果输入不是有效的JSON，返回错误消息
        formatted_response = f"Invalid JSON: {str(e)}"
    return formatted_response

if __name__ == "__main__":
    app.run_server(debug=True)