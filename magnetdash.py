import datetime
import numpy as np
import pandas as pd
import argparse
import os, re

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly
import plotly.subplots
import plotly.graph_objects as go


odir = "log"
ofname = "log"
directions = ["x", "y", "z"]
nsamples = 1000

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
external_stylesheets = [dbc.themes.BOOTSTRAP]

div_graphs = list()
div_graphs.append(html.Div(
    className = "row",
    children = [
        html.H1(
            children="Magnetic field monitor",
            style = {
                "margin": ".5em 1em"
            }),
        dbc.Card([
            dbc.CardBody([
                html.H4("Field components", className="card-title"),
                dcc.Graph(id=f"b-components-graph")
            ])],
            style = {
                "width": "45%",
                "margin-left": "2.5%",
                "margin-right": "0%",
                # "height": "100%",
                "float": "left"
            }
        ),
        dbc.Card([
            dbc.CardBody([
                html.H4("Field direction", className="card-title"),
                dcc.Graph(id=f"b-arrow-graph")
            ])],
            style = {
                "width": "45%",
                "margin-left": "2%",
                "margin-right": "1%",
                # "height": "100%",
                "float": "left"
            }
        )
        # html.Div(
        #     children = [
        #         dcc.Graph(
        #             id=f"b-components-graph",
        #             style = {
        #                 "width": "50%",
        #                 "height": "100%",
        #                 "float": "left"
        #             }),
        #         dcc.Graph(
        #             id=f"b-arrow-graph",
        #             style = {
        #                 "width": "50%",
        #                 "height": "100%",
        #                 "float": "left"
        #             }),
        #     ]
        # )
    ]
))
callback_outputs = list()
callback_outputs.append(Output(f"b-components-graph", "figure"))
callback_outputs.append(Output(f"b-arrow-graph", "figure"))
div_graphs.append(
    dcc.Interval(
        id="interval-component",
        interval=1000,
        n_intervals=0
    )
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(html.Div(div_graphs))

@app.callback(*callback_outputs, Input("interval-component", "n_intervals"))
def update_graphs(n):
    logfiles = os.listdir(odir)
    logfiles = sorted([ f for f in logfiles if re.match(f"{ofname}-\d+.csv", f) ])
    logfile = f"{odir}/{logfiles[-1]}"

    df = pd.read_csv(logfile, sep=";")
    data_time = np.array(df["time"])[-nsamples:]
    data_time -= data_time[0]
    data_components = dict()
    for direction in directions:
        data_components[direction] = list(df[direction])[-nsamples:]

    fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.1)
    fig["layout"]["title"] = {
        "x": .1, "y": .9,
    }
    fig["layout"]["margin"] = {
        "l": 20, "r": 10, "b": 0, "t": 10
    }
    fig["layout"]["legend"] = {"x": 0, "y": 1, "xanchor": "left"}

    for direction in directions:
        fig.append_trace({
            "x": data_time,
            "y": data_components[direction],
            "name": f"B{direction}",
            "mode": "lines",
            "type": "scatter",
        }, 1, 1)
    fig.update_xaxes(title_text="time", row=1, col=1)
    fig.update_yaxes(title_text="B field", row=1, col=1)
    #fig.update_traces(line={"color":y_column["color"]})
    
    b_vector = [data_components[direction][-1] for direction in directions]
    b_module = np.sqrt(sum([ b**2 for b in b_vector ]))
    b_vector = [b/b_module for b in b_vector]
    arrow = go.Figure(data=go.Cone(u=[b_vector[0]], v=[b_vector[1]], w=[b_vector[2]], x=[0], y=[0], z=[0]))
    arrow.update_layout(scene_camera_eye=dict(x=0.76, y=1.8, z=0.92))

    return [fig, arrow]

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)