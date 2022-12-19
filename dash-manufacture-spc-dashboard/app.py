import os
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import pandas as pd


import platform
import subprocess
from libs.cpu import CPU
from libs.armazenamento import Armazenamento
from libs.processos import Processos
from libs.ram import RAM

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Dashboard - Sistemas Operacionais"
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "spc_data.csv")))

params = list(df)
max_length = 1800

suffix_row = "_row"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"

# ------------------- VARIAVEIS GLOBAIS --------------------
cpu = CPU()
storage = Armazenamento()
ram = RAM()
processos = Processos()
# ------------------- VARIAVEIS GLOBAIS --------------------

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Dashboard - Sistemas Operacionais"),
                    html.H6("Projeto Final - Disciplina Sistemas Operacionais 2022/2"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.A(
                        html.Button(children="Moodle da Disciplina"),
                        href="https://moodle.utfpr.edu.br/course/view.php?id=23306",
                    ),
                    html.Button(
                        id="learn-more-button", children="Sobre o Projeto", n_clicks=0
                    ),
                ],
            ),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Terminal",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Hardware e Processos",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


def init_df():
    ret = {}
    for col in list(df[1:]):
        data = df[col]
        stats = data.describe()

        std = stats["std"].tolist()
        ucl = (stats["mean"] + 3 * stats["std"]).tolist()
        lcl = (stats["mean"] - 3 * stats["std"]).tolist()
        usl = (stats["mean"] + stats["std"]).tolist()
        lsl = (stats["mean"] - stats["std"]).tolist()

        ret.update(
            {
                col: {
                    "count": stats["count"].tolist(),
                    "data": data,
                    "mean": stats["mean"].tolist(),
                    "std": std,
                    "ucl": round(ucl, 3),
                    "lcl": round(lcl, 3),
                    "usl": round(usl, 3),
                    "lsl": round(lsl, 3),
                    "min": stats["min"].tolist(),
                    "max": stats["max"].tolist(),
                    "ooc": populate_ooc(data, ucl, lcl),
                }
            }
        )

    return ret


def populate_ooc(data, ucl, lcl):
    ooc_count = 0
    ret = []
    for i in range(len(data)):
        if data[i] >= ucl or data[i] <= lcl:
            ooc_count += 1
            ret.append(ooc_count / (i + 1))
        else:
            ret.append(ooc_count / (i + 1))
    return ret


state_dict = init_df()


def init_value_setter_store():
    # Initialize store data
    state_dict = init_df()
    return state_dict


def build_tab_1():
    return [
        # Manually select metrics
        html.Div(
            id="set-specs-intro-container",
            # className='twelve columns',
            children=html.P(
                "Use historical control limits to establish a benchmark, or set new values."
            ),
        ),
        html.Div(
            id="settings-menu",
            children=[
                html.Div(
                    id="metric-select-menu",
                    # className='five columns',
                    children=[
                        html.Label(id="metric-select-title", children="Select Metrics"),
                        html.Br(),
                        dcc.Dropdown(
                            id="metric-select-dropdown",
                            options=list(
                                {"label": param, "value": param} for param in params[1:]
                            ),
                            value=params[1],
                        ),
                    ],
                ),
                html.Div(
                    id="value-setter-menu",
                    # className='six columns',
                    children=[
                        html.Div(id="value-setter-panel"),
                        html.Br(),
                        html.Div(
                            id="button-div",
                            children=[
                                html.Button("Update", id="value-setter-set-btn"),
                                html.Button(
                                    "View current setup",
                                    id="value-setter-view-btn",
                                    n_clicks=0,
                                ),
                            ],
                        ),
                        html.Div(
                            id="value-setter-view-output", className="output-datatable"
                        ),
                    ],
                ),
            ],
        ),
    ]


ud_usl_input = daq.NumericInput(
    id="ud_usl_input", className="setting-input", size=200, max=9999999
)
ud_lsl_input = daq.NumericInput(
    id="ud_lsl_input", className="setting-input", size=200, max=9999999
)
ud_ucl_input = daq.NumericInput(
    id="ud_ucl_input", className="setting-input", size=200, max=9999999
)
ud_lcl_input = daq.NumericInput(
    id="ud_lcl_input", className="setting-input", size=200, max=9999999
)


def build_value_setter_line(line_num, label, value, col3):
    return html.Div(
        id=line_num,
        children=[
            html.Label(label, className="four columns"),
            html.Label(value, className="four columns"),
            html.Div(col3, className="four columns"),
        ],
        className="row",
    )


def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### Sobre o Projeto

                        Este é um DashBoard para visualização de informações referentes ao sistema operacional da máquina.

                        ###### Quais informações são apresentadas

                        A aplicação contam com 5 botões principais:

                        - O primeiro demonstra informações sobre o sistema operacional instalado e informações de Hardware;
                        
                        - O segundo apresenta informações sobre as threads e processos do sistemas que estão ativos no momento;

                        - O terceiro conta com o sistema de arquivos do sistema, ou seja, a árvore de diretórios;

                        - O quarto mostra as informações referentes ao uso da memória no sistema;

                        - E por fim, o quinto e último botão, simula um terminal de comando Linux. 

                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )


# Informações do Sistema operacional
def info_Sistema_Operacional_system():
    variaveis_Sistema = platform.uname()
    return variaveis_Sistema.system

def info_Sistema_Operacional_node():
    variaveis_Sistema = platform.uname()
    return variaveis_Sistema.node

def info_Sistema_Operacional_release():
    variaveis_Sistema = platform.uname()
    return variaveis_Sistema.release

def info_Sistema_Operacional_version():
    variaveis_Sistema = platform.uname()
    return variaveis_Sistema.version

# Informações de arquitetura da máquina
def executa_comando_terminal(comando):
    comando_executado = subprocess.run(
        args=comando,
        shell=True,
        capture_output=True,
        universal_newlines=True
    )
    print(comando_executado.stdout)
    return comando_executado.stdout

def info_Hardware_Processador():
    comando = executa_comando_terminal("lshw -class CPU")
    comando = comando.split("cpu")
    comando = comando[1]
    comando = comando.split("fabricante")
    comando = comando[0]
    comando = comando.split(":")
    comando = comando[1]
    return comando

def info_Hardware_Ram():
    comando = executa_comando_terminal("grep MemTotal /proc/meminfo")
    comando = comando.split(":")
    return comando[1]

def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    generate_section_banner("-> Informações do Sistema: "),
                    html.P("Kernel: "+ info_Sistema_Operacional_system()),
                    html.P("Nome do Nó: "+ info_Sistema_Operacional_node()),
                    html.P("Versão: "+ info_Sistema_Operacional_release()),
                    html.P("Data de criação: "+ info_Sistema_Operacional_version()),
                ],
            ),
            html.Div(
                id="card-2",
                className="four columns",
                children=[
                    generate_section_banner("-> Informações do Hardware:"),
                    html.P("Processador: "+ info_Hardware_Processador()),
                    html.P("Memória RAM: "+ info_Hardware_Ram()),
                ],
            ),
            html.Div(
                id="utility-card",
                children=[daq.StopButton(id="stop-button", size=160, n_clicks=0)],
            ),
        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


def build_top_panel(stopped_interval):
    rows = []
    for x in range(cpu.qtd_cores):
        rows.append(generate_metric_row_helper(stopped_interval, x))

    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("CPU"),
                    html.Div(
                        id="metric-div",
                        children=[
                            generate_metric_list_header(),
                            html.Div(
                                id="metric-rows",
                                children=[x for x in rows],
                            ),
                        ],
                    ),
                ],
            ),
            # Piechart
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("Armazenamento"),
                    generate_piechart('piechart'),
                ],
            ),
        ],
    )


def generate_piechart(id):
    return dcc.Graph(
        id=id,
        figure={
            "data": [
                {
                    "labels": ['algo', 'algo2'],
                    "values": [30, 70],
                    "type": "pie",
                    "marker": {"line": {"color": "white", "width": 0.1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                }
            ],
            "layout": {
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
            },
        },
    )


# Build header
def generate_metric_list_header():
    return generate_metric_row(
        "metric_header",
        {"height": "3rem", "margin": "1rem 0", "textAlign": "center"},
        {"id": "m_header_1", "children": html.Div("CORE")},
        {"id": "m_header_3", "children": html.Div("% USO (30 seg.)")},
        {"id": "m_header_4", "children": html.Div("%")},
        {"id": "m_header_5", "children": html.Div("% BARRA")},
    )


def generate_metric_row_helper(stopped_interval, index):
    item = cpu.core_info[index][index]

    div_id = item + suffix_row
    sparkline_graph_id = item + suffix_sparkline_graph
    ooc_percentage_id = item + suffix_ooc_n
    ooc_graph_id = item + suffix_ooc_g

    return generate_metric_row(
        div_id,
        None,
        {
            "id": item,
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item + "_sparkline",
            "children": dcc.Graph(
                id=sparkline_graph_id,
                style={"width": "100%", "height": "95%"},
                config={
                    "staticPlot": False,
                    "editable": False,
                    "displayModeBar": False,
                },
                figure=go.Figure(
                    {
                        "data": [
                            {
                                "x": [x for x in range(1, stopped_interval+1)],
                                "y": list(cpu.core_info[index]['uso_anterior']),
                                "mode": "lines+markers",
                                "name": item,
                                "line": {"color": "#f4d44d"},
                            }
                        ],
                        "layout": {
                            "uirevision": True,
                            "margin": dict(l=0, r=0, t=4, b=4, pad=0),
                            "xaxis": dict(
                                showline=False,
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                            ),
                            "yaxis": dict(
                                showline=False,
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                            ),
                            "paper_bgcolor": "rgba(0,0,0,0)",
                            "plot_bgcolor": "rgba(0,0,0,0)",
                        },
                    }
                ),
            ),
        },
        {"id": ooc_percentage_id, "children": cpu.core_info[index]['uso_atual']},
        {
            "id": ooc_graph_id + "_container",
            "children": daq.GraduatedBar(
                id=ooc_graph_id,
                color={
                    "ranges": {
                        "#92e0d3": [0, 4],
                        "#f4d44d ": [4, 10],
                        "#f45060": [10, 15],
                    }
                },
                showCurrentValue=False,
                max=15,
                value=cpu.core_info[index]['uso_atual']*15/100,
            ),
        },
    )


def generate_metric_row(id, style, col1, col3, col4, col5):
    if style is None:
        style = {"height": "8rem", "width": "100%"}

    return html.Div(
        id=id,
        className="row metric-row",
        style=style,
        children=[
            html.Div(
                id=col1["id"],
                className="one column",
                style={"margin-right": "2.5rem", "minWidth": "50px"},
                children=col1["children"],
            ),
            html.Div(
                id=col3["id"],
                style={"height": "100%"},
                className="four columns",
                children=col3["children"],
            ),
            html.Div(
                id=col4["id"],
                style={},
                className="one column",
                children=col4["children"],
            ),
            html.Div(
                id=col5["id"],
                style={"height": "100%", "margin-top": "5rem"},
                className="three columns",
                children=col5["children"],
            ),
        ],
    )


def build_bottom_panel(stopped_interval):
    rows = []
    for x in range(cpu.qtd_cores):
        rows.append(generate_bottom_metric_row_helper(stopped_interval, x))

    return html.Div(
        id="bottom-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="bottom-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("Processos"),
                    html.Div(
                        id="bottom-metric-div",
                        children=[
                            generate_bottom_metric_list_header(),
                            html.Div(
                                id="bottom-metric-rows",
                                children=[x for x in rows],
                            ),
                        ],
                    ),
                ],
            ),
            # Piechart
            html.Div(
                id="bottom-piechart-div",
                className="four columns",
                children=[
                    generate_section_banner("RAM"),
                    generate_piechart('bottom-piechart'),
                ],
            ),
        ],
    )


# Build header
def generate_bottom_metric_list_header():
    return generate_bottom_metric_row(
        "bottom_header",
        {"height": "3rem", "margin": "1rem 0", "textAlign": "center"},
        {"id": "bottom_header_1", "children": html.Div("PID")},
        {"id": "bottom_header_2", "children": html.Div("User")},
        {"id": "bottom_header_3", "children": html.Div("PR")},
        {"id": "bottom_header_4", "children": html.Div("NI")},
        {"id": "bottom_header_5", "children": html.Div("VIRT")},
        {"id": "bottom_header_6", "children": html.Div("RES")},
        {"id": "bottom_header_7", "children": html.Div("SHR")},
        {"id": "bottom_header_8", "children": html.Div("%CPU")},
        {"id": "bottom_header_9", "children": html.Div("%MEM")},
        {"id": "bottom_header_10", "children": html.Div("TIME+")},
        {"id": "bottom_header_11", "children": html.Div("Command")},
    )


def generate_bottom_metric_row_helper(stopped_interval, index):
    item = cpu.core_info[index][index]

    div_id = item + suffix_row
    sparkline_graph_id = item + suffix_sparkline_graph
    ooc_percentage_id = item + suffix_ooc_n
    ooc_graph_id = item + suffix_ooc_g

    return generate_bottom_metric_row(
        div_id,
        None,
        {
            "id": item+'1',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'2',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'3',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'4',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'7',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'14',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'13',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'12',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'11',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'10',
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": item+'11',
            "className": "metric-row-button-text",
            "children": item,
        },
    )


def generate_bottom_metric_row(id, style, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11):
    if style is None:
        style = {"height": "2rem", "width": "100%"}

    return html.Div(
        id=id,
        className="bottom row metric-row",
        style=style,
        children=[
            html.Div(
                id=col1["id"],
                className="one column",
                style={"height": "25%"},
                children=col1["children"],
            ),
            html.Div(
                id=col2["id"],
                style={"height": "25%"},
                className="one column",
                children=col2["children"],
            ),
            html.Div(
                id=col3["id"],
                style={"height": "25%"},
                className="one column",
                children=col3["children"],
            ),
            html.Div(
                id=col4["id"],
                style={"height": "25%"},
                className="one column",
                children=col4["children"],
            ),
            html.Div(
                id=col5["id"],
                className="one column",
                style={"height": "25%"},
                children=col5["children"],
            ),
            html.Div(
                id=col6["id"],
                style={"height": "25%"},
                className="one column",
                children=col6["children"],
            ),
            html.Div(
                id=col7["id"],
                style={"height": "25%"},
                className="one column",
                children=col7["children"],
            ),
            html.Div(
                id=col8["id"],
                style={"height": "25%"},
                className="one column",
                children=col8["children"],
            ),
            html.Div(
                id=col9["id"],
                className="one column",
                style={"height": "25%"},
                children=col9["children"],
            ),
            html.Div(
                id=col10["id"],
                style={"height": "25%"},
                className="one column",
                children=col10["children"],
            ),
            html.Div(
                id=col11["id"],
                style={"height": "25%"},
                className="one column",
                children=col11["children"],
            ),
        ],
    )


# ------------------ DAQUI PRA BAIXO UPDATES ------------------
def update_sparkline(interval, index):
    x_array = [x for x in range(1, len(cpu.core_info[index]['uso_anterior'])+1)]
    y_array = cpu.core_info[index]['uso_anterior']

    if interval == 0:
        x_new = y_new = None

    else:
        x_new = x_array[:][-1]
        y_new = y_array[:][-1]

    return dict(x=[[x_new]], y=[[y_new]]), [0]


def update_count(interval, index, data):
    if interval == 0:
        return "0", "0.00%", 0.00001, "#92e0d3"

    if interval > 0:
        uso_atual = cpu.core_info[index]['uso_atual']
        uso_atual_str = "%.2f" % uso_atual + "%"

        if uso_atual == 0.0:
            uso_atual_barra = 0.00001
        else:
            uso_atual_barra = float(uso_atual*15/100)

    return uso_atual_str, uso_atual_barra


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval= 2*1000,  # in milliseconds
            n_intervals=0,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="value-setter-store", data=init_value_setter_store()),
        dcc.Store(id="n-interval-stage", data=30),
        generate_modal(),
    ],
)


@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return build_tab_1(), stopped_interval
    
    cpu.atualiza_info_cores()
    return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                html.Div(
                    id="graphs-container",
                    #children=[build_top_panel(stopped_interval), build_chart_panel()],
                    children=[build_top_panel(stopped_interval), build_bottom_panel(stopped_interval)],
                ),
            ],
        ),
        stopped_interval,
    )


# Update interval
@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
    [
        State("interval-component", "n_intervals"),
        State("interval-component", "disabled"),
        State("n-interval-stage", "data"),
    ],
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    return cur_stage


# Callbacks for stopping interval update
@app.callback(
    [Output("interval-component", "disabled"), Output("stop-button", "buttonText")],
    [Input("stop-button", "n_clicks")],
    [State("interval-component", "disabled")],
)
def stop_production(n_clicks, current):
    if n_clicks == 0:
        return True, "start"
    return not current, "stop" if current else "start"


# ======= Callbacks for modal popup =======
@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}


# ======= update progress gauge =========
@app.callback(
    output=Output("progress-gauge", "value"),
    inputs=[Input("interval-component", "n_intervals")],
)
def update_gauge(interval):
    if interval < max_length:
        total_count = interval
    else:
        total_count = max_length

    return int(total_count)


# ===== Callbacks to update values based on store data and dropdown selection =====
@app.callback(
    output=[
        Output("value-setter-panel", "children"),
        Output("ud_usl_input", "value"),
        Output("ud_lsl_input", "value"),
        Output("ud_ucl_input", "value"),
        Output("ud_lcl_input", "value"),
    ],
    inputs=[Input("metric-select-dropdown", "value")],
    state=[State("value-setter-store", "data")],
)
def build_value_setter_panel(dd_select, state_value):
    return (
        [
            build_value_setter_line(
                "value-setter-panel-header",
                "Specs",
                "Historical Value",
                "Set new value",
            ),
            build_value_setter_line(
                "value-setter-panel-usl",
                "Upper Specification limit",
                state_dict[dd_select]["usl"],
                ud_usl_input,
            ),
            build_value_setter_line(
                "value-setter-panel-lsl",
                "Lower Specification limit",
                state_dict[dd_select]["lsl"],
                ud_lsl_input,
            ),
            build_value_setter_line(
                "value-setter-panel-ucl",
                "Upper Control limit",
                state_dict[dd_select]["ucl"],
                ud_ucl_input,
            ),
            build_value_setter_line(
                "value-setter-panel-lcl",
                "Lower Control limit",
                state_dict[dd_select]["lcl"],
                ud_lcl_input,
            ),
        ],
        state_value[dd_select]["usl"],
        state_value[dd_select]["lsl"],
        state_value[dd_select]["ucl"],
        state_value[dd_select]["lcl"],
    )


# ====== Callbacks to update stored data via click =====
@app.callback(
    output=Output("value-setter-store", "data"),
    inputs=[Input("value-setter-set-btn", "n_clicks")],
    state=[
        State("metric-select-dropdown", "value"),
        State("value-setter-store", "data"),
        State("ud_usl_input", "value"),
        State("ud_lsl_input", "value"),
        State("ud_ucl_input", "value"),
        State("ud_lcl_input", "value"),
    ],
)
def set_value_setter_store(set_btn, param, data, usl, lsl, ucl, lcl):
    if set_btn is None:
        return data
    else:
        data[param]["usl"] = usl
        data[param]["lsl"] = lsl
        data[param]["ucl"] = ucl
        data[param]["lcl"] = lcl

        # Recalculate ooc in case of param updates
        data[param]["ooc"] = populate_ooc(df[param], ucl, lcl)
        return data


@app.callback(
    output=Output("value-setter-view-output", "children"),
    inputs=[
        Input("value-setter-view-btn", "n_clicks"),
        Input("metric-select-dropdown", "value"),
        Input("value-setter-store", "data"),
    ],
)
def show_current_specs(n_clicks, dd_select, store_data):
    if n_clicks > 0:
        curr_col_data = store_data[dd_select]
        new_df_dict = {
            "Specs": [
                "Upper Specification Limit",
                "Lower Specification Limit",
                "Upper Control Limit",
                "Lower Control Limit",
            ],
            "Current Setup": [
                curr_col_data["usl"],
                curr_col_data["lsl"],
                curr_col_data["ucl"],
                curr_col_data["lcl"],
            ],
        }
        new_df = pd.DataFrame.from_dict(new_df_dict)
        return dash_table.DataTable(
            style_header={"fontWeight": "bold", "color": "inherit"},
            style_as_list_view=True,
            fill_width=True,
            style_cell_conditional=[
                {"if": {"column_id": "Specs"}, "textAlign": "left"}
            ],
            style_cell={
                "backgroundColor": "#1e2130",
                "fontFamily": "Open Sans",
                "padding": "0 2rem",
                "color": "darkgray",
                "border": "none",
            },
            css=[
                {"selector": "tr:hover td", "rule": "color: #91dfd2 !important;"},
                {"selector": "td", "rule": "border: none !important;"},
                {
                    "selector": ".dash-cell.focused",
                    "rule": "background-color: #1e2130 !important;",
                },
                {"selector": "table", "rule": "--accent: #1e2130;"},
                {"selector": "tr", "rule": "background-color: transparent"},
            ],
            data=new_df.to_dict("rows"),
            columns=[{"id": c, "name": c} for c in ["Specs", "Current Setup"]],
        )


# decorator for list of output
def create_callback(index):
    def callback(interval, stored_data):
        cpu.atualiza_info_cores()
        uso_atual, uso_atual_barra = update_count(interval, index, stored_data)
        spark_line_data = update_sparkline(interval, index)
        return spark_line_data, uso_atual, uso_atual_barra

    return callback


for index in range(cpu.qtd_cores):
    update_param_row_function = create_callback(index)
    app.callback(
        output=[
            Output(cpu.core_info[index][index] + suffix_sparkline_graph, "extendData"),
            Output(cpu.core_info[index][index] + suffix_ooc_n, "children"),
            Output(cpu.core_info[index][index] + suffix_ooc_g, "value"),
        ],
        inputs=[Input("interval-component", "n_intervals")],
        state=[State("value-setter-store", "data")],
    )(update_param_row_function)


#  ======= button to choose/update figure based on click ============
@app.callback(
    output=Output("control-chart-live", "figure"),
    inputs=[
        Input("interval-component", "n_intervals"),
    ],
    state=[State("value-setter-store", "data"), State("control-chart-live", "figure")],
)
def update_control_chart(interval, data, cur_fig):
    # Find which one has been triggered
    ctx = dash.callback_context

    if not ctx.triggered:
        return generate_graph(interval, data, params[1])

    if ctx.triggered:
        # Get most recently triggered id and prop_type
        splitted = ctx.triggered[0]["prop_id"].split(".")
        prop_id = splitted[0]
        prop_type = splitted[1]

        if prop_type == "n_clicks":
            curr_id = cur_fig["data"][0]["name"]
            prop_id = prop_id[:-7]
            if curr_id == prop_id:
                return generate_graph(interval, data, curr_id)
            else:
                return generate_graph(interval, data, prop_id)

        if prop_type == "n_intervals" and cur_fig is not None:
            curr_id = cur_fig["data"][0]["name"]
            return generate_graph(interval, data, curr_id)


# Update piechart
@app.callback(
    output=Output("piechart", "figure"),
    inputs=[Input("interval-component", "n_intervals")],
)
def update_piechart(interval):
    if(interval == 0):
        return {
            "data": [],
            "layout": {
                "font": {"color": "white"},
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
            },
        }

    labels = []
    values = []
    colors = []
    for device in storage.device_info:
        labels.append(device['device'])
        values.append(device['ocupado'])
        colors.append('red')

    labels.append('Livre')
    values.append(round((storage.total - storage.ocupado), 2))
    colors.append("green")

    new_figure = {
        "data": [
            {
                "labels": labels,
                "values": values,
                "type": "pie",
                "marker": {"colors": colors, "line": dict(color="white", width=2)},
                "hoverinfo": "label",
                "textinfo": "label",
            }
        ],
        "layout": {
            "margin": dict(t=5, b=80),
            "uirevision": True,
            "font": {"color": "white"},
            "showlegend": False,
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "autosize": True,
        },
    }
    return new_figure


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8030)
