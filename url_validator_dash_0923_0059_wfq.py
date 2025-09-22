# 代码生成时间: 2025-09-23 00:59:49
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import pandas as pd
from urllib.parse import urlparse

# URL Validator Dash Application
app = dash.Dash(__name__)

# Define layout of the application
app.layout = html.Div(children=[
    html.H1(children='URL Validator'),
    dcc.Input(id='url-input', type='text', placeholder='Enter a URL'),
    html.Button('Validate', id='validate-button', n_clicks=0),
    html.Div(id='output-container'),
])

# Callback to validate URL
@app.callback(
    Output('output-container', 'children'),
    [Input('validate-button', 'n_clicks')],
    [State('url-input', 'value')]
)
def validate_url(n_clicks, url_input):
    if n_clicks > 0:  # Check if button has been clicked
        try:
            # Check if URL is valid
            result = check_url_validity(url_input)
            return f'Valid: {result}'
        except Exception as e:
            return f'Error: {str(e)}'
    return ''

# Function to validate URL
def check_url_validity(url):
    try:
        # Parse URL to check if it's well-formed
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return False
        # Attempt to make a HEAD request to the URL
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        return False

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)