import pathlib
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_daq as daq


from modules.cpu import CPU
from modules.ram import RAM
from modules.info_sistema import InfoSistema
from modules.processos import Processos
from modules.armazenamento import Armazenamento

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Dashboard - Sistemas Operacionais"
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

max_length = 1800

suffix_row = "_row"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"

sufixo_div_bottom_row = 'div-bottom-row'
sufixo_pid = 'pid'
sufixo_name = 'name'
sufixo_username = 'username'
sufixo_nice = 'nice'
sufixo_memory = 'memory_percent'
sufixo_status = 'status_id'

# ---------------------------------------
cpu = CPU()
ram = RAM()
processos = Processos()
storage = Armazenamento()
info_sistema = InfoSistema()
# ---------------------------------------

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
                html.H5("Dashboard - Sistemas Operacionais"),
                html.H6("Projeto Final - Disciplina Sistemas Operacionais 2022/2"),
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


def build_tab_1():
    return [
        html.Div(
    [
        html.Div(
            [
                html.Hr(),
                html.Center(
                    html.H1('Terminal'),
                ),
                html.Hr(),
            ],
            className='div-terminal-titulo',
        ),
        html.Div(
            [
                html.Div(
                    dcc.Input(
                        id='input-comando',
                        value='',
                        type='text',
                        debounce=True,
                        autoFocus=True,
                        className='terminal-textArea',
                    ),
                    className='terminal-div-input',
                ),
                html.Div(
                    children = [
                        html.Button(
                            'Executar',
                            id='execute-button',
                            className='terminal-botao-executar',
                        ),
                    ],
                    className='terminal-div-botao-executar',
                ),
            ],
        ),
        html.Div(
            [
                dcc.Textarea(
                    id='text-area-retorno',
                    value='',
                    disabled='true',
                    className='terminal-area-retorno',
                ),
                
            ],
            className='terminal-div-retorno',
        )
    ],
    className='terminal-div-viewport'
)]



@app.callback(
    [
        Output('text-area-retorno', 'value'),
        Output('input-comando', 'value')
    ],
    [Input('input-comando', 'value')]
)
def on_click(comando):
    if (not comando == ''):
        return info_sistema.executa_comando_terminal(comando), ''
    return '', ''


def build_infos_sistema_hardware():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    generate_section_banner("-> Informações do Sistema: "),
                    html.P("Kernel: "+ info_sistema.get_info_system()),
                    html.P("Nome do Nó: "+ info_sistema.get_info_node()),
                    html.P("Versão: "+ info_sistema.get_info_release()),
                    html.P("Data de criação: "+ info_sistema.get_info_version()),
                ],
            ),
            html.Div(
                id="card-2",
                className="four columns",
                children=[
                    generate_section_banner("-> Informações do Hardware:"),
                    html.P("Processador: "+ info_sistema.get_info_processador()),
                    html.P("Memória RAM: "+ info_sistema.get_info_ram()),
                ],
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
                            html.Div(
                                id="utility-card",
                                children=[daq.StopButton(id="stop-button", size=100, n_clicks=0)],
                            ),
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
                    "labels": [],
                    "values": [],
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
        {"id": "m_header_3", "children": html.Div("% USO (anterior)")},
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
                                "line": {"color": "#33C3F0"},
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
                        "green": [0, 4],
                        "yellow ": [4, 10],
                        "red": [10, 15],
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


def build_bottom_panel():
    rows = []
    for x in range(processos.qtd_processos):
        rows.append(generate_bottom_metric_row_helper(x))

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
        {"id": "bottom_header_2", "children": html.Div("Nome")},
        {"id": "bottom_header_3", "children": html.Div("User")},
        {"id": "bottom_header_4", "children": html.Div("NI")},
        {"id": "bottom_header_5", "children": html.Div("%MEM")},
        {"id": "bottom_header_6", "children": html.Div("Status")},
    )


def generate_bottom_metric_row_helper(index):
    item = str(index)

    div_id = item + sufixo_div_bottom_row
    pid_id = item + sufixo_pid
    name_id = item + sufixo_name
    username_id = item + sufixo_username
    nice_id = item + sufixo_nice
    memory_percent_id = item + sufixo_memory
    status_id = item + sufixo_status

    return generate_bottom_metric_row(
        div_id,
        None,
        {
            "id": pid_id,
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": name_id,
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": username_id,
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": nice_id,
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": memory_percent_id,
            "className": "metric-row-button-text",
            "children": item,
        },
        {
            "id": status_id,
            "className": "metric-row-button-text",
            "children": item,
        },
    )


def generate_bottom_metric_row(id, style, col1, col2, col3, col4, col5, col6):
    if style is None:
        style = {"height": "5rem", "width": "100%"}

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


def update_count(interval, index):
    if interval == 0:
        return "0.00%", 0.00001

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
            interval= 5*1000,  # in milliseconds
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
        dcc.Store(id="n-interval-stage", data=30),
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
                build_infos_sistema_hardware(),
                html.Div(
                    id="graphs-container",
                    children=[build_bottom_panel(), build_top_panel(stopped_interval)],
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
        return True, "Iniciar"
    return not current, "Parar" if current else "Iniciar"


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


# decorator for list of output
def create_callback_bottom(index):
    def callback(interval):
        processos.atualiza_info_processos()
        return processos.get_infos_processo(index)

    return callback


for index in range(processos.qtd_processos):
    update_param_row_function = create_callback_bottom(index)
    app.callback(
        output=[
            Output(str(index)+sufixo_pid, "children"),
            Output(str(index)+sufixo_name, "children"),
            Output(str(index)+sufixo_username, "children"),
            Output(str(index)+sufixo_nice, "children"),
            Output(str(index)+sufixo_memory, "children"),
            Output(str(index)+sufixo_status, "children"),
        ],
        inputs=[Input("interval-component", "n_intervals")],
    )(update_param_row_function)


# decorator for list of output
def create_callback(index):
    def callback(interval):
        cpu.atualiza_info_cores()
        uso_atual, uso_atual_barra = update_count(interval, index)
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
    )(update_param_row_function)


# Atualiza o piechart do Armazenamento
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
        colors.append(device['cor'])

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
                "hoverinfo": "labels",
                "textinfo": "labels",
            }
        ],
        "layout": {
            "margin": dict(t=5, b=80),
            "uirevision": True,
            "font": {"color": "white"},
            "showlegend": True,
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "autosize": True,
        },
    }
    return new_figure


# Atualiza o piechart da RAM
@app.callback(
    output=Output("bottom-piechart", "figure"),
    inputs=[Input("interval-component", "n_intervals")],
)
def update_ram_piechart(interval):
    ram.atualiza_info_ram()
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
    for info in ram.ram_info:
        labels.append(info)
        values.append(ram.ram_info[info])
        colors.append('green')

    labels.append('Em uso')
    values.append(ram.get_ram_em_uso())
    colors.append("red")

    new_figure = {
        "data": [
            {
                "labels": labels,
                "values": values,
                "type": "pie",
                "marker": {"colors": colors, "line": dict(color="white", width=2)},
                "hoverinfo": "label",
                "textinfo": "values",
            }
        ],
        "layout": {
            "margin": dict(t=5, b=80),
            "uirevision": True,
            "font": {"color": "white"},
            "showlegend": True,
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "autosize": True,
        },
    }
    return new_figure


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8030)
