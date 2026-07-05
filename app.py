from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Dark theme
pio.templates.default = "plotly_dark"

# Load data
df = pd.read_csv("data/ev_market.csv")

# KPI values
total_sales = df["EV_Sales"].sum()
total_countries = df["Country"].nunique()
total_years = df["Year"].nunique()
total_stations = df["Charging_Stations"].sum()

# App
app = Dash(__name__)

# Layout
app.layout = html.Div([

    # Title
    html.H1(
        "🚗 EV Market Forecast Dashboard",
        style={"textAlign": "center", "color": "white", "padding": "20px"}
    ),

    # KPI Cards
    html.Div([

        html.Div([
            html.H4("🚗 Total EV Sales"),
            html.H2(f"{total_sales:,}")
        ], style={"background": "rgba(255,255,255,0.08)",
                  "color": "white",
                  "padding": "20px",
                  "borderRadius": "15px",
                  "width": "22%",
                  "display": "inline-block",
                  "textAlign": "center",
                  "margin": "10px"}),

        html.Div([
            html.H4("🌍 Countries"),
            html.H2(total_countries)
        ], style={"background": "rgba(255,255,255,0.08)",
                  "color": "white",
                  "padding": "20px",
                  "borderRadius": "15px",
                  "width": "22%",
                  "display": "inline-block",
                  "textAlign": "center",
                  "margin": "10px"}),

        html.Div([
            html.H4("📅 Years"),
            html.H2(total_years)
        ], style={"background": "rgba(255,255,255,0.08)",
                  "color": "white",
                  "padding": "20px",
                  "borderRadius": "15px",
                  "width": "22%",
                  "display": "inline-block",
                  "textAlign": "center",
                  "margin": "10px"}),

        html.Div([
            html.H4("⚡ Charging Stations"),
            html.H2(f"{total_stations:,}")
        ], style={"background": "rgba(255,255,255,0.08)",
                  "color": "white",
                  "padding": "20px",
                  "borderRadius": "15px",
                  "width": "22%",
                  "display": "inline-block",
                  "textAlign": "center",
                  "margin": "10px"})

    ], style={"textAlign": "center"}),

    html.Br(),

    # Country Dropdown (MULTI SELECT)
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in df["Country"].unique()],
        value=list(df["Country"].unique()),
        multi=True,
        clearable=False,
        style={"width": "50%", "margin": "20px auto"}
    ),

    html.Br(),

    # 🔥 YEAR RANGE SLIDER (MAIN ADDITION)
    dcc.RangeSlider(
        id="year-range",
        min=df["Year"].min(),
        max=df["Year"].max(),
        value=[df["Year"].min(), df["Year"].max()],
        marks={str(y): str(y) for y in sorted(df["Year"].unique())},
        step=None
    ),

    html.Br(),

    # Graphs
    dcc.Graph(id="line-chart"),
    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="pie-chart")

], style={
    "background": "linear-gradient(135deg, #0f172a, #1e293b)",
    "minHeight": "100vh",
    "padding": "20px"
})


# Callback
@app.callback(
    Output("line-chart", "figure"),
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Input("country-dropdown", "value"),
    Input("year-range", "value")
)
def update_graph(selected_countries, year_range):

    # Filter data
    filtered_df = df[
        (df["Country"].isin(selected_countries)) &
        (df["Year"] >= year_range[0]) &
        (df["Year"] <= year_range[1])
    ]

    # Line chart
    line_fig = px.line(
        filtered_df,
        x="Year",
        y="EV_Sales",
        color="Country",
        markers=True,
        title="EV Sales Trend (Multi Country)"
    )

    # Bar chart
    bar_fig = px.bar(
        filtered_df,
        x="Country",
        y="EV_Sales",
        color="Country",
        title="EV Sales Comparison"
    )

    # Pie chart
    pie_fig = px.pie(
        filtered_df,
        names="Country",
        values="EV_Sales",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title="Market Share"
    )

    # Styling
    for fig in [line_fig, bar_fig, pie_fig]:
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

    return line_fig, bar_fig, pie_fig


# Run app
if __name__ == "__main__":
    app.run(debug=True)