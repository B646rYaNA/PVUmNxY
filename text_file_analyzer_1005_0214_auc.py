# 代码生成时间: 2025-10-05 02:14:30
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
from dash.dependencies import Input, Output, State\
import plotly.express as px\
import pandas as pd\
from dash.exceptions import PreventUpdate\
import base64\
import io\
import os\
from pdfminer.high_level import extract_text\

# Define the app layout\
app = dash.Dash(__name__)\
app.layout = html.Div([
    html.H1("Text File Content Analyzer"),\
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={"width": "100%", "height": "60px", "lineHeight": "60px","borderWidth": "1px", "borderStyle": "dashed", "borderRadius": "5px", "textAlign": "center", "margin": "10px"},
        # Allow multiple files to be uploaded\
        multiple=True
    ),\
    html.Div(id='output-data-upload'),\
    dcc.Graph(id='word-count-graph'),\
    dcc.Graph(id='character-count-graph')
])\

# Define a function to extract text from a pdf file
def extract_pdf_text(pdf_file):
    # Initialize an empty string to store the text
    text = ""
    # Use pdfminer to extract text from the pdf file
    with open(pdf_file, 'rb') as f:
        text = extract_text(f)
    return text

# Define a function to analyze the content of a text file
def analyze_text_file(file_content):
    # Initialize dictionaries to store word and character counts
    word_counts = {}
    character_counts = {}
    # Split the file content into words and characters
    words = file_content.split()
    characters = list(file_content)
    # Count the occurrences of each word and character
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    for character in characters:
        character_counts[character] = character_counts.get(character, 0) + 1
    return word_counts, character_counts

# Define a callback to handle file uploads\@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(uploaded_files, filename, last_modified):
    # Check if any files were uploaded
    if uploaded_files is None:
        raise PreventUpdate
    # Initialize an empty string to store the file content
    file_content = ""
    # Check the file type and process accordingly
    if filename[-3:] == 'pdf':
        # Extract text from the pdf file
        file_content = extract_pdf_text(uploaded_files)
    elif filename[-3:] == 'txt':
        # Read the text file directly
        file_content = uploaded_files.decode('utf-8')
    else:
        # Return an error message if the file type is not supported
        return html.Div([
            html.H5("Unsupported file type"),
            "Please upload a text or PDF file."
        ])
    # Analyze the file content
    word_counts, character_counts = analyze_text_file(file_content)
    # Update the word count graph
    word_count_df = pd.DataFrame(list(word_counts.items()), columns=['Word', 'Count'])
    fig_word_count = px.bar(word_count_df, x='Word', y='Count', title='Word Count')
    app.callback(
        Output('word-count-graph', 'figure'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename'),
         State('upload-data', 'last_modified')]
    ).trigger_if_evaluated(fig_word_count)
    # Update the character count graph
    character_count_df = pd.DataFrame(list(character_counts.items()), columns=['Character', 'Count'])
    fig_character_count = px.bar(character_count_df, x='Character', y='Count', title='Character Count')
    app.callback(
        Output('character-count-graph', 'figure'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename'),
         State('upload-data', 'last_modified')]
    ).trigger_if_evaluated(fig_character_count)
    # Return a success message
    return html.Div([
        html.H5("File uploaded successfully"),
        f"File name: {filename}",
        f"Last modified: {last_modified}"
    ])\

# Start the server\
if __name__ == '__main__':
    app.run_server(debug=True)