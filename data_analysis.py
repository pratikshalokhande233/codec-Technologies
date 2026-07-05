import pandas as pd
import plotly.express as px

# CSV file read
df = pd.read_csv("data/ev_market.csv")

# Government Subsidy Pie Chart
fig = px.pie(
    df,
    names="Government_Subsidy",
    title="Government Subsidy Distribution"
)

fig.show()