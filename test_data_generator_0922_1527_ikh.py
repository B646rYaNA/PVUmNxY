# 代码生成时间: 2025-09-22 15:27:55
import random
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

# 测试数据生成器 Dash 应用
class TestDataGenerator:
    def __init__(self):
        # 初始化 Dash 应用
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.layout = self.create_layout()

    def create_layout(self):
        # 创建 Dash 应用的布局
        layout = dbc.Container(
            style={"padding": "2%"},
            children=[
                dbc.Row(
                    dbc.Col(html.H1("测试数据生成器"), md=12)
                ),
                dbc.Row(
                    dbc.Col(
                        dcc.Input(id="input-num-rows", type="number", min=1, placeholder="请输入行数"),
                        md=4,
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dcc.Button("生成测试数据", id="generate-button"),
                        md=4,
                    )
                ),
                dbc.Row(
                    dbc.Col(id="output-container", md=12),
                ),
            ]
        )
        return layout

    def generate_test_data(self, num_rows):
        # 生成测试数据的函数
        if num_rows <= 0:
            raise ValueError("行数必须大于0")
        data = {
            "id": list(range(1, num_rows + 1)),
            "name": [f"姓名{i}" for i in range(num_rows)],
            "age": [random.randint(18, 60) for _ in range(num_rows)],
            "city": ["城市A", "城市B", "城市C"] * ((num_rows // 3) + 1),
        }
        data["city"] = data["city"][:num_rows]  # 确保城市列长度正确
        return pd.DataFrame(data)

    def callback(self):
        # 回调函数，生成测试数据
        @self.app.callback(
            Output("output-container", "children"),
            [Input("generate-button", "n_clicks")],
            [State("input-num-rows", "value")],
        )
def output_container(n_clicks, num_rows):
            if n_clicks is None or num_rows is None:
                return None
            try:
                df = self.generate_test_data(int(num_rows))
                return dcc.Download(dcc.Table(
                    style_cell={"textAlign": "center", "padding": "5px"},
                    style_data_conditional=[{
                        "if": {"column_id": i},
                        "textAlign": "center"
                    } for i in df.columns],
                    children=[
                        html.Tr([html.Th(col) for col in df.columns]),
                        *[html.Tr(
                            [html.Td(df.iloc[i][col]) for col in df.columns]
                        ) for i in range(num_rows)]
                    ]
                ))
            except Exception as e:
                return html.Div(f"发生错误：{str(e)}")

    def run(self):
        # 运行 Dash 应用
        self.callback()
        self.app.run_server(debug=True)

# 程序入口
def main():
    generator = TestDataGenerator()
    generator.run()

if __name__ == "__main__":
    main()