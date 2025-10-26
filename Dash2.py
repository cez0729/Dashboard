from plotly.data import gapminder
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# External stylesheets for Bootstrap and custom CSS
css = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
    {
        "href": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap",
        "rel": "stylesheet"
    }
]

app = Dash(name="Gapminder Dashboard", external_stylesheets=css)

# Custom CSS for additional styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f8f9fa;
            }
            .header {
                background-color: #ffffff;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
            }
            .sidebar {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 15px;
                height: calc(100vh - 120px);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .content {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 20px;
                height: calc(100vh - 120px);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                overflow-y: auto;
            }
            .dropdown-container {
                display: flex;
                gap: 15px;
                align-items: center;
                margin-bottom: 20px;
            }
            .dropdown-label {
                font-weight: 500;
                color: #333;
            }
            .dcc-dropdown {
                min-width: 150px;
            }
            .nav-tabs .nav-link {
                color: #495057;
                font-weight: 500;
                border-radius: 6px;
                margin-bottom: 5px;
            }
            .nav-tabs .nav-link.active {
                background-color: #0d6efd;
                color: white;
                font-weight: 700;
            }
            .nav-tabs .nav-link:hover {
                background-color: #e9ecef;
            }
            .graph-container {
                border-radius: 8px;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

################### DATASET ####################################
gapminder_df = gapminder()
gapminder_df["Year"] = gapminder_df.year

#################### CHARTS #####################################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=gapminder_df.columns,
            align='left',
            fill_color='#0d6efd',
            font=dict(color='white', size=12),
            line_color='white'
        ),
        cells=dict(
            values=gapminder_df.values.T,
            align='left',
            fill_color='#f8f9fa',
            font=dict(color='#333', size=11),
            line_color='white'
        ))
    ])
    fig.update_layout(
        paper_bgcolor="#ffffff",
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
        height=600
    )
    return fig

def create_population_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.continent == continent) & (gapminder_df.Year == year)]
    filtered_df = filtered_df.sort_values(by="pop", ascending=False).head(15)

    fig = px.bar(
        filtered_df,
        x="country",
        y="pop",
        color="country",
        title=f"Top 15 Countries by Population in {continent} ({year})",
        text_auto='.2s',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        height=500,
        margin={"t": 50, "b": 50},
        title_font=dict(size=18, color='#333'),
        font=dict(color='#333'),
        xaxis_title="Country",
        yaxis_title="Population",
        showlegend=False
    )
    fig.update_traces(textfont=dict(color='#333'))
    return fig

def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.continent == continent) & (gapminder_df.Year == year)]
    filtered_df = filtered_df.sort_values(by="gdpPercap", ascending=False).head(15)

    fig = px.bar(
        filtered_df,
        x="country",
        y="gdpPercap",
        color="country",
        title=f"Top 15 Countries by GDP per Capita in {continent} ({year})",
        text_auto='.2f',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        height=500,
        margin={"t": 50, "b": 50},
        title_font=dict(size=18, color='#333'),
        font=dict(color='#333'),
        xaxis_title="Country",
        yaxis_title="GDP per Capita",
        showlegend=False
    )
    fig.update_traces(textfont=dict(color='#333'))
    return fig

def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.continent == continent) & (gapminder_df.Year == year)]
    filtered_df = filtered_df.sort_values(by="lifeExp", ascending=False).head(15)

    fig = px.bar(
        filtered_df,
        x="country",
        y="lifeExp",
        color="country",
        title=f"Top 15 Countries by Life Expectancy in {continent} ({year})",
        text_auto='.2f',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        height=500,
        margin={"t": 50, "b": 50},
        title_font=dict(size=18, color='#333'),
        font=dict(color='#333'),
        xaxis_title="Country",
        yaxis_title="Life Expectancy",
        showlegend=False
    )
    fig.update_traces(textfont=dict(color='#333'))
    return fig

def create_choropleth_map(variable, year):
    filtered_df = gapminder_df[gapminder_df.Year == year]
    variable_name = {"pop": "Population", "gdpPercap": "GDP per Capita", "lifeExp": "Life Expectancy"}.get(variable, variable)

    fig = px.choropleth(
        filtered_df,
        color=variable,
        locations="iso_alpha",
        locationmode="ISO-3",
        color_continuous_scale="RdYlBu",
        hover_data=["country", variable],
        title=f"{variable_name} Choropleth Map ({year})"
    )
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        height=500,
        margin={"t": 50, "l": 0, "r": 0, "b": 0},
        title_font=dict(size=18, color='#333'),
        font=dict(color='#333'),
        geo=dict(bgcolor='#ffffff')
    )
    return fig

##################### WIDGETS ####################################
continents = gapminder_df.continent.unique()
years = gapminder_df.Year.unique()

cont_population = dcc.Dropdown(id="cont_pop", options=continents, value="Asia", clearable=False, className="dcc-dropdown")
year_population = dcc.Dropdown(id="year_pop", options=years, value=1952, clearable=False, className="dcc-dropdown")

cont_gdp = dcc.Dropdown(id="cont_gdp", options=continents, value="Asia", clearable=False, className="dcc-dropdown")
year_gdp = dcc.Dropdown(id="year_gdp", options=years, value=1952, clearable=False, className="dcc-dropdown")

cont_life_exp = dcc.Dropdown(id="cont_life_exp", options=continents, value="Asia", clearable=False, className="dcc-dropdown")
year_life_exp = dcc.Dropdown(id="year_life_exp", options=years, value=1952, clearable=False, className="dcc-dropdown")

year_map = dcc.Dropdown(id="year_map", options=years, value=1952, clearable=False, className="dcc-dropdown")
var_map = dcc.Dropdown(
    id="var_map",
    options=[
        {"label": "Population", "value": "pop"},
        {"label": "GDP per Capita", "value": "gdpPercap"},
        {"label": "Life Expectancy", "value": "lifeExp"}
    ],
    value="lifeExp",
    clearable=False,
    className="dcc-dropdown"
)

##################### APP LAYOUT ####################################
app.layout = html.Div([
    html.Div([
        html.H1("Gapminder Dataset Analysis", className="text-center fw-bold"),
    ], className="header"),
    html.Div([
        html.Div([
            dcc.Tabs(
                id="tabs",
                vertical=True,
                value="tab-dataset",
                className="nav nav-tabs",
                children=[
                    dcc.Tab(label="Dataset", value="tab-dataset", className="nav-link"),
                    dcc.Tab(label="Population", value="tab-population", className="nav-link"),
                    dcc.Tab(label="GDP Per Capita", value="tab-gdp", className="nav-link"),
                    dcc.Tab(label="Life Expectancy", value="tab-life-exp", className="nav-link"),
                    dcc.Tab(label="Choropleth Map", value="tab-choropleth", className="nav-link"),
                ]
            )
        ], className="col-2 sidebar"),
        html.Div([
            html.Div(id="tab-content-dataset", style={"display": "block"}, children=[
                dcc.Graph(id="dataset", figure=create_table(), className="graph-container")
            ]),
            html.Div(id="tab-content-population", style={"display": "none"}, children=[
                html.Div([
                    html.Span("Continent:", className="dropdown-label"),
                    cont_population,
                    html.Span("Year:", className="dropdown-label"),
                    year_population
                ], className="dropdown-container"),
                dcc.Graph(id="population", figure=create_population_chart(), className="graph-container")
            ]),
            html.Div(id="tab-content-gdp", style={"display": "none"}, children=[
                html.Div([
                    html.Span("Continent:", className="dropdown-label"),
                    cont_gdp,
                    html.Span("Year:", className="dropdown-label"),
                    year_gdp
                ], className="dropdown-container"),
                dcc.Graph(id="gdp", figure=create_gdp_chart(), className="graph-container")
            ]),
            html.Div(id="tab-content-life-exp", style={"display": "none"}, children=[
                html.Div([
                    html.Span("Continent:", className="dropdown-label"),
                    cont_life_exp,
                    html.Span("Year:", className="dropdown-label"),
                    year_life_exp
                ], className="dropdown-container"),
                dcc.Graph(id="life_expectancy", figure=create_life_exp_chart(), className="graph-container")
            ]),
            html.Div(id="tab-content-choropleth", style={"display": "none"}, children=[
                html.Div([
                    html.Span("Variable:", className="dropdown-label"),
                    var_map,
                    html.Span("Year:", className="dropdown-label"),
                    year_map
                ], className="dropdown-container"),
                dcc.Graph(id="choropleth_map", figure=create_choropleth_map("lifeExp", 1952), className="graph-container")
            ]),
        ], className="col-10 content")
    ], className="row mx-0")
], style={"background-color": "#f8f9fa", "min-height": "100vh"})

##################### CALLBACKS ####################################
@callback(
    [Output("tab-content-dataset", "style"),
     Output("tab-content-population", "style"),
     Output("tab-content-gdp", "style"),
     Output("tab-content-life-exp", "style"),
     Output("tab-content-choropleth", "style")],
    Input("tabs", "value")
)
def update_tab_visibility(tab):
    base_style = {"display": "none"}
    visible_style = {"display": "block"}
    if tab == "tab-dataset":
        return visible_style, base_style, base_style, base_style, base_style
    elif tab == "tab-population":
        return base_style, visible_style, base_style, base_style, base_style
    elif tab == "tab-gdp":
        return base_style, base_style, visible_style, base_style, base_style
    elif tab == "tab-life-exp":
        return base_style, base_style, base_style, visible_style, base_style
    elif tab == "tab-choropleth":
        return base_style, base_style, base_style, base_style, visible_style
    return base_style, base_style, base_style, base_style, base_style

@callback(
    Output("population", "figure"),
    [Input("cont_pop", "value"), Input("year_pop", "value")]
)
def update_population_chart(continent, year):
    return create_population_chart(continent, year)

@callback(
    Output("gdp", "figure"),
    [Input("cont_gdp", "value"), Input("year_gdp", "value")]
)
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)

@callback(
    Output("life_expectancy", "figure"),
    [Input("cont_life_exp", "value"), Input("year_life_exp", "value")]
)
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)

@callback(
    Output("choropleth_map", "figure"),
    [Input("var_map", "value"), Input("year_map", "value")]
)
def update_map(var_map, year):
    return create_choropleth_map(var_map, year)

if __name__ == "__main__":
    app.run(debug=True)