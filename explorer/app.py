import os
import sys
sys.path.append("../src")

import json
import logging

import dash
from dash import dcc, html, ctx

from dash.dependencies import Input, Output

import dash_interactive_graphviz

from dataset import Dataset
from topology import Topology
from heuristic import Heuristic
from visualizer import Visualizer

from logger import DashLoggerHandler

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    update_title=None
)
app.title = "Decision Diagram Explorer"
server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            id="root-container",
            children=[
                html.Div(
                    id="left-sidebar-container",
                    className="sidebar",
                    children=[
                        dcc.Loading(id="loading-container", children=[html.Div(id="loading-output")], type="default"),
                        html.H1("Decision Diagrams"),
                        html.P("Explore constructive heuristics for decision diagrams."),
                        html.Div(
                            id="controls-container",
                            children=[
                                html.Div(
                                    style={"display":"flex","flex-direction":"row"},
                                    children=[
                                        html.Div(
                                            style={"flex":1,"margin-right":"20px"},
                                            children=[
                                                html.H3("Data set"),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="dataset-selector",
                                                            options=sorted([os.path.splitext(dataset)[0] for dataset in os.listdir('../datasets/processed')]),
                                                            value="iris"
                                                        )
                                                    ],
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            style={"width":"100px"},
                                            children=[
                                                html.H3("Seed"),
                                                html.Div(
                                                    children=[
                                                        dcc.Input(
                                                            id="seed-input",
                                                            type="number",
                                                            placeholder="Seed",
                                                            value=1,
                                                            style={"width":"100%"}
                                                        )
                                                    ],
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                                html.Div(style={"display":"flex","align-items":"baseline"},children=[
                                    html.H3("Alpha"),
                                    html.H3("0.1",style={"fontSize":"0.9em","marginLeft":"5px","color":"rgba(255,255,255,0.5)"},id="alpha-value")
                                ]),
                                html.Div(
                                    children=[
                                        dcc.Slider(0.0, 1.0, 0.01,
                                            value=0.1,
                                            marks={0 if v == 0 else 1 if v == 10 else v/10: str(v/10) for v in range(0,11)},
                                            id="alpha-slider"
                                        ),
                                    ],
                                ),
                                html.H3("Skeleton"),
                                html.Div(
                                    children=[
                                        dcc.RadioItems(
                                            ["1-2-4-8", "1-2-4-4-4", "1-2-3-3-3-3", "1-2-2-2-2-2-2-2"], 
                                            "1-2-4-4-4",
                                            inline=True, id="skeleton-selector"
                                        )
                                    ],
                                ),
                                html.H3("Feature subset ratio"),
                                html.Div(
                                    children=[
                                        dcc.Slider(0.5, 1.0, 0.1,
                                            value=0.6,
                                            id="feature-subset-ratio-slider"
                                        ),
                                    ],
                                ),
                                html.H3("Constructive improvements"),
                                html.Div(
                                    children=[
                                        dcc.Checklist(
                                            [
                                                { "label": "Randomize splits", "value": "randomize_splits" },
                                                { "label": "Bottom-up pruning", "value": "bottom_up_pruning" },
                                                { "label": "Pure split pruning", "value": "pure_split_pruning" },
                                            ],
                                            ["bottom_up_pruning","pure_split_pruning"],
                                            id="constructive-improvements-checklist"
                                        )
                                    ],
                                ),
                            ]
                        )
                    ],
                ),
                html.Div(
                    id="main-container",
                    children=[
                        html.Div(
                            style={"flex":"1","position":"relative"},
                            children=[dash_interactive_graphviz.DashInteractiveGraphviz(id="diagram")]
                        ),
                        html.Div(
                            id="steps-container",
                            children=[
                                dcc.Interval(
                                    id='steps-interval',
                                    interval=1*1000, # ms
                                    n_intervals=0
                                ),
                                html.Div(
                                    children=[
                                        dcc.Slider(-1, -1, 1,
                                            value=-1,
                                            id="steps-slider"
                                        ),
                                    ],
                                ),
                                html.Div(id="steps-controls-container", children=[
                                    html.Button("<<", id="steps-prev-button"),
                                    html.Button("▶", id="steps-play-button"),
                                    html.Button(">>", id="steps-next-button"),
                                ]),
                            ]
                        )
                    ],
                ),
                html.Div(
                    id="right-sidebar-container",
                    className="sidebar",
                    children=[
                        html.Div(id="metrics-container"),
                        html.Div(
                            id="steps-metadata-container",
                            children=[
                                html.Div(id="steps-metadata"),
                            ]
                        ),
                        html.Div(style={ 'flex': '1' }, children=[
                            dcc.Interval(id='logger-interval', interval=1 * 1000, n_intervals=0,disabled=True),
                            html.Div(children=[dcc.Checklist([{ "label": "Debugger", "value": "debugger" }],["debugger"],id="debugger-checklist")]),
                            html.Iframe(id='console-out', srcDoc='',style={
                                'width': '100%',
                                'height':'100%',
                                'background': 'rgba(0, 0, 0, 0.1)',
                                'border': '1px solid rgba(0,0,0,0.5)'
                            })
                        ])
                    ],
                ),
            ],
        )
    ]
)

partial_solutions = []
partial_solutions_metadata = []
empty_graph = "graph { bgcolor=\"transparent\" }"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
dashLoggerHandler = DashLoggerHandler()
logger.addHandler(dashLoggerHandler)

@app.callback(Output("steps-play-button", "children"), Input("steps-play-button", "n_clicks"))
def update_steps_play_button_state(n_clicks):
    n = 0 if n_clicks is None else n_clicks
    return "▶" if n % 2 == 0 else "■"

@app.callback(
    Output("steps-interval", "disabled"),
    Output("steps-interval", "n_intervals"),
    Input("steps-play-button", "n_clicks"),
    Input("steps-interval", "n_intervals")
)
def update_steps_playing(n_clicks, n_intervals):
    n = 0 if n_clicks is None else n_clicks
    disabled = n % 2 == 0
    intervals = -1 if disabled else n_intervals
    return (disabled, intervals)

@app.callback(
    Output("steps-slider", "value"),
    Input("steps-slider", "value"),
    Input("steps-interval", "n_intervals"),
    Input("steps-prev-button", "n_clicks"),
    Input("steps-next-button", "n_clicks")
)
def update_steps_slider_interval(value, n_intervals, prev_clicks, next_clicks):
    if ctx.triggered_id == "steps-interval":
        return min(n_intervals, len(partial_solutions)-1)
    elif ctx.triggered_id == "steps-prev-button":
        return max(value-1, 0)
    elif ctx.triggered_id == "steps-next-button":
        return min(value+1, len(partial_solutions)-1)
    else:
        return value

@app.callback(Output("steps-metadata", "children"), Input("steps-slider", "value"))
def update_steps_metadata(partial_solution):
    if len(partial_solutions_metadata) == 0: return "No step selected"
    metadata = partial_solutions_metadata[partial_solution]
    attributes = metadata["attributes"]
    if metadata["type"] == "split":
        return f"Decided to split node {attributes['node']} on feature {attributes['feature']} at value {attributes['threshold']:.3f}"
    elif metadata["type"] == "arc":
        decision = f"Decided to connect the {'positive' if attributes['side'] == '+' else 'negative'} arc of node {attributes['node_from']} to node {attributes['node_to']}"
        if attributes['pure_split_pruned']:
            decision += f", because at least {attributes['pure_split_threshold']*100:.1f}% of the samples were from class {attributes['predominant_class']}"
        return decision
    elif metadata["type"] == "bottom_up_prune":
        return f"Decided to prune node {attributes['node']}, because the accuracy cost ({attributes['accuracy_cost']:.2f}) was no larger than the pruning gain ({attributes['pruning_gain']:.2f})"
    elif metadata["type"] == "bottom_up_prune_skipped":
        return f"Decided not to prune node {attributes['node']}, because the accuracy cost ({attributes['accuracy_cost']:.4f}) was above the pruning gain ({attributes['pruning_gain']:.4f})"
    elif metadata["type"] == "no_split_prune":
        return f"Decided to prune node {attributes['node']}, because no possible split was found"
    else:
        return json.dumps(partial_solutions_metadata[partial_solution])

@app.callback(
    Output("diagram", "dot_source"),
    Output("steps-slider", "max"),
    Output("metrics-container", "children"),
    Output("loading-output", "children"),
    Input("dataset-selector", "value"),
    Input("seed-input", "value"),
    Input("alpha-slider", "value"),
    Input("skeleton-selector", "value"),
    Input("feature-subset-ratio-slider", "value"),
    Input("constructive-improvements-checklist", "value"),
    Input("steps-slider", "value"),
)
def update_diagram(dataset, seed, alpha, skeleton_value, feature_subset_ratio, constructive_improvements, 
                   partial_solution):
    global partial_solutions
    global partial_solutions_metadata
    
    if dataset is None:
        return (empty_graph, 0, metrics_component(None), None)

    bottom_up_pruning = "bottom_up_pruning" in constructive_improvements
    pure_split_pruning = "pure_split_pruning" in constructive_improvements
    randomize_splits = "randomize_splits" in constructive_improvements

    dataset = f"../datasets/processed/{dataset}.csv"
    data = Dataset(dataset, train_validation_test_split=[0.5, 0.25, 0.25], seed=seed)

    skeleton = [int(v) for v in skeleton_value.split("-")]
    topology = Topology(skeleton, data)

    if len(partial_solutions) != 0 and ctx.triggered_id == "steps-slider":
        solution = partial_solutions[partial_solution]
        visualizer = Visualizer(data, solution)
    else:
        heuristic = Heuristic(
            data, 
            topology,
            seed=seed,
            alpha=alpha, 
            randomize_splits=randomize_splits,
            feature_subset_ratio=min(1.0, max(0.0, feature_subset_ratio)),
            bottom_up_pruning=bottom_up_pruning, 
            pure_split_pruning=pure_split_pruning,
            keep_partial_solutions=True,
            verbose=False,
            logger=logger
        )
        solution = heuristic.solution
        partial_solutions = heuristic.partial_solutions
        partial_solutions_metadata = heuristic.partial_solutions_metadata
        visualizer = Visualizer(data, solution)

    final_solution = partial_solutions[-1]

    return (
        visualizer.view(filled=True, fragmentation_only=False).source,
        len(partial_solutions)-1,
        metrics_component(final_solution, alpha=alpha, topology=topology),
        None
    )

def metrics_component(solution, alpha=0.0, topology=None):
    if solution is None:
        objective_value_text = "--"
        training_accuracy_text = "--"
        validation_accuracy_text = "--"
        test_accuracy_text = "--"
    else:
        objective_value = solution.objective_value(alpha, len(topology.internal_nodes))
        objective_value_text = f"{objective_value:.3f}"
        training_accuracy = solution.training_accuracy()
        training_accuracy_text = f"{(training_accuracy*100):.1f}%"
        validation_accuracy = solution.validation_accuracy()
        validation_accuracy_text = f"{(validation_accuracy*100):.1f}%"
        test_accuracy = solution.test_accuracy()
        test_accuracy_text = f"{(test_accuracy*100):.1f}%"
    return html.Div(
        children=[
            html.Div(
                className="metric-panel first",
                children=[
                    html.H2(objective_value_text),
                    html.Span("Objective value"),
                ]
            ),
            html.Div(
                className="double",
                children=[
                    html.Div(
                        className="metric-panel",
                        children=[
                            html.H2(training_accuracy_text),
                            html.Span("Training accuracy"),
                        ]
                    ),
                    html.Div(
                        className="metric-panel",
                        children=[
                            html.H2(validation_accuracy_text),
                            html.Span("Validation accuracy"),
                        ]
                    ),
                ]
            ),
            html.Div(
                className="metric-panel",
                children=[
                    html.H2(test_accuracy_text),
                    html.Span("Test accuracy"),
                ]
            ),
        ]
    )

@app.callback(
    Output("alpha-value", "children"),
    Input("alpha-slider", "value")
)
def update_alpha_value(alpha):
    return alpha

@app.callback(Output("alpha-slider", "disabled"),Input("constructive-improvements-checklist", "value"))
def alpha_slider_status(constructive_improvements):
    return "bottom_up_pruning" not in constructive_improvements

@app.callback(Output("feature-subset-ratio-slider", "disabled"),Input("constructive-improvements-checklist", "value"))
def alpha_slider_status(constructive_improvements):
    return "randomize_splits" not in constructive_improvements

@app.callback(
    Output('console-out', 'srcDoc'),
    Input('logger-interval', 'n_intervals'),
    Input("debugger-checklist", "value"))
def update_output(_, checklist):
    disable = len(checklist) == 0
    if disable:
        return ""
    return "".join([f'<p style="font-family:monospace;color:rgba(255,255,255,0.5);margin:5px;">{line}</p>' for line in dashLoggerHandler.queue])

@app.callback(
    Output('logger-interval', 'disabled'),
    Input("debugger-checklist", "value"))
def update_output(value):
    disable = len(value) == 0
    return disable

if __name__ == "__main__":
    app.run_server(debug=True)
