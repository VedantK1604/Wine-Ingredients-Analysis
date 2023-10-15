import dash
import pandas as pd
import plotly.express as px
from sklearn.datasets import load_wine
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

"""Load Wine data from sklearn_dataset"""


def load_data():
    wine = load_wine()
    wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
    wine_df['WineType'] = [wine.target_names[t] for t in wine.target]
    return wine_df


wine_df = load_data()
ingredients = wine_df.drop(columns=["WineType"]).columns
avg_wine_df = wine_df.groupby('WineType').mean().reset_index()


"""Creating Scatter Chart"""


def create_scatter_chart(x_axis='alcohol', y_axis='malic_acid', color_encode=False):
    scatter_fig = px.scatter(wine_df, x=x_axis, y=y_axis, color='WineType' if color_encode else None,
                             title="{} vs {} ".format(x_axis.capitalize(), y_axis.capitalize()))
    #     scatter_fig.update_layout(height=400)
    return scatter_fig


"""Creating Bar Chart"""

def create_bar_chart(ingredients=['alcohol','malic_acid', 'ash']):
    bar_fig = px.bar(avg_wine_df, x="WineType", y=ingredients, title='Avg.Ingredients per wine type')
    bar_fig.update_layout(height=600)
    return bar_fig

"""Creating Widgets"""

x_axis = dcc.Dropdown(id='x_axis', options=ingredients, value='alcohol', clearable=False,style={'display':'inline-block', 'width':'49%'})
y_axis = dcc.Dropdown(id='y_axis', options=ingredients, value='malic_acid', clearable=False,style={'display':'inline-block', 'width':'49%'})
color_encode = dcc.Checklist(id='color_encode', options=['color-Encode'])

multiselect = dcc.Dropdown(id='multiselect', options=ingredients, value=['alcohol','malic_acid', 'ash'], multi=True)

"""Creating webpage layout"""

app = dash.Dash(title="Wine Analysis")

app.layout = html.Div(
    children=[
        html.H1("Wine Analysis Dataset", style={'text-align':'center'}),
        html.Div("Explore relationship between various ingredients used in creation of three different types of"
               "wine (class_0, class_1, class_2).",style={'text-align':'center'}),
        html.Br(),
        html.Div(
            children=[
                x_axis,y_axis,color_encode,
                dcc.Graph(id='scatter_chart', figure=create_scatter_chart())
            ],
            style={'display':'inline-block', 'width':'49%'}
        ),
        html.Div(
            children=[
                multiselect,html.Br(),
                dcc.Graph(id='bar_chart', figure=create_bar_chart())
            ],
            style={'display': 'inline-block', 'width': '49%'}
        )
    ],
    style={'padding':'0px'}
)

"""Callbacks"""

@callback(Output('scatter_chart','figure'),[Input('x_axis','value'),Input('y_axis','value'),Input('color_encode','value')])
def update_scatter_chart(x_axis, y_axis, color_encode):
    return create_scatter_chart(x_axis, y_axis, color_encode)

@callback(Output('bar_chart','figure'),[Input('multiselect','value')])
def update_bar_chart(ingredients):
    return create_bar_chart(ingredients)

if __name__ == '__main__':
    app.run_server()
# debug=True