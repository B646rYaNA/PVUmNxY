# 代码生成时间: 2025-09-29 00:03:23
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DATA_LAKE_PATH = os.getenv('DATA_LAKE_PATH')
if not DATA_LAKE_PATH:
    raise EnvironmentError('DATA_LAKE_PATH must be set in .env file')

# Create application instance
app = dash.Dash(__name__)
server = app.server

# Define application layout
app.layout = html.Div([
    html.H1('Data Lake Management Tool'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'}
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='file-contents-graph'),
])

# Callback to update output when file is uploaded
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')]
)
def update_output(contents):
    if contents is not None:
        # Save file to data lake
        file_name = contents.filename
        file_path = os.path.join(DATA_LAKE_PATH, file_name)
        with open(file_path, 'wb') as file:
            file.write(contents)
            logger.info(f'File {file_name} uploaded to data lake')
        
        # Read file and return its contents
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return 'No file uploaded'

# Callback to generate a graph when file is uploaded
@app.callback(
    Output('file-contents-graph', 'figure'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')])
def update_graph(contents, filename):
    if contents is not None:
        # Save file to data lake
        file_path = os.path.join(DATA_LAKE_PATH, filename)
        with open(file_path, 'wb') as file:
            file.write(contents)
            logger.info(f'File {filename} uploaded to data lake')
        
        # Check if file is a CSV and generate a graph
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
            fig = px.histogram(df, x=df.columns[0])
            return fig
        else:
            return {'data': [{'x': [], 'y': [], 'type': 'scatter', 'name': 'No Data'}]}
    else:
        return {'data': [{'x': [], 'y': [], 'type': 'scatter', 'name': 'No File Uploaded'}]}

# Run app
def run_app():
    app.run_server(debug=True)

if __name__ == '__main__':
    run_app()