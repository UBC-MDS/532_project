import dash
import dash_core_components as dcc
import dash_html_components as html
import altair as alt
import vega_datasets as vega
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True
server = app.server

app.title = 'Dash app with pure Altair HTML'

df = vega.data.jobs()
def mds_special():
    
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "middle",
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 50, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

# register the custom theme under a chosen name
alt.themes.register('mds_special', mds_special)

# enable the newly registered theme
alt.themes.enable('mds_special')

# plotting the ratio bar chart
def ratio():
    """
    Wrangles the data and make the interactive bar plot.

    returns:
    an altair bar chart.
    """
    gap_df = df.groupby(['year', 'sex']).sum().reset_index()
    p5 = alt.Chart(gap_df).mark_bar().encode(
        alt.X("year:O", title = "Year"),
        alt.Y("perc:Q", title = "Percentage"),
        alt.Tooltip(['year','count', 'sex', 'perc']),
        alt.Color("sex:N", title = "Sex", scale=alt.Scale(
        domain=['women', 'men'],
        range=['pink', 'steelblue']))
    ).properties(
        width=600,
        height=300,
        title = "Employement Gender Gap Over The Years"
    )
    return p5


# plotting the trend line chart

def trend(job_to_choose = 'Janitor'):
    """
    Plots a line plot for a selected job.

    Arguments:
    job_to_choose; str
        the job to be displayed in the plot.
    Returns:
    an altair line plot
    """
    chart = alt.Chart(df.query('job == @job_to_choose')).mark_line().encode(
            alt.X("year:O", title = "Year"),
            alt.Y("count:Q", title = "Count"),
            alt.Color("sex:N", scale=alt.Scale(
            domain=['women', 'men'],
            range=['pink', 'steelblue'])),
            alt.Tooltip(['year','count', 'sex']),
            alt.OpacityValue(0.7)
            
            ).properties(
            width=600,
            height=300,
            title = job_to_choose + " Number Change Over the Years ")
    points = alt.Chart(df.query('job == @job_to_choose')).mark_point().encode(
            alt.X("year:O", title = "Year"),
            alt.Y("count:Q", title = "Count"),
            alt.Color('sex')
            )
    return chart + points

# Plotting the heatmap and the first tab bar chart
def heat_map():
    """
    plots a heatmap.

    Returns:
    an altair heatmap.
    """
    df = vega.data.jobs()
    men_fav = df[df["sex"] == "men"].groupby('job').sum()
    men_fav = men_fav.sort_values(by = "count", ascending=False)

    x = men_fav.index[0:10].to_numpy()
    men_fav_df = df[df['job'].isin(x)]
    men_fav_df = men_fav_df.groupby(['job', 'year']).sum().reset_index()
    df_men = df[df['job'].isin(x)]
    brush = alt.selection(type='interval')
    plot = alt.Chart(men_fav_df).mark_rect().encode(
                alt.X('year:O', title = "Year"),
                alt.Y('job:O', title= None),
                color=alt.Color('count', title = "Employment Count", scale=alt.Scale(scheme="reds")),
                tooltip = ['year:O', 'job:O', 'count:Q']
            ).properties(width=500, height = 300, title = "Total employments over the Years").add_selection(
            brush
            )
    bars = alt.Chart(df_men).mark_bar().encode(
        alt.X("sex:N", axis=None),
        alt.Y("count:Q", title = "Total Count"),
        alt.Color("sex:N", scale=alt.Scale(
        domain=['women', 'men'],
        range=['pink', 'steelblue']))
    ).properties(
        width=70,
        height=300
    ).transform_filter(
        brush
    )
    final = plot | bars
    return final

# creating tab-3 header
gender_ratio_header = dbc.Row([
    dbc.Col(width = 2),
    dbc.Col(dbc.Jumbotron(
    [
        dbc.Container(
            [
                
                html.P(
                       "This is a graph showing the change in the labour force gender gap over time for all the jobs in the jobs dataset. Interact with this "
                        "graph by hovering over a bar to get the details of the actual percentage of the selected year and "
                        "gender.",
                    className="lead"
                ),
            ],
            fluid=True,
            style={'max-height': '50px', 'min-height' : '10px', 'margin-top': '-5%'}
        )
    ],
    fluid=True,
), width=8)
])

# Creating tab 1 header
heat_map_tab_header = dbc.Row([
    dbc.Col(width = 2),
    dbc.Col(dbc.Jumbotron(
    [
        dbc.Container(
            [
                
                html.P(
                    "This is a heatmap showing the change of the employment total count over the years."
                    " Interact with this map by hovering over a point to get more details."
                    " A comparison between men and women is possible by "
                    "dragging over a region on the heatmap shown in the bar chart. "
                    " Only 10 jobs out of the 250 jobs that are in the dataset are selected for the purpose of the comparison"
                    "     ",
                    className="lead",
                    
                ),
            ],
            fluid=True,
            style={'max-height': '60px', 'min-height' : '10px', 'margin-top': '-5%'}
        )
    ],
    fluid=True,
), width=8, style={'max-height': '300px'}
)])

# Create tab 2 header 
job_trend_tab_header = dbc.Row([
    dbc.Col(),
    dbc.Col(dbc.Jumbotron(
    [
        dbc.Container(
            [
                
                html.P(
                       "This is a graph showing the trend of total count for a particular job for both sexes."
                    " Interact with this graph by selecting a specific job from the 10 jobs in the dropdown menu.",
                    className="lead",
                ),
            ],
            fluid=True,
            style={'max-height': '50px', 'min-height' : '10px', 'margin-top': '-5%'}
        )
    ],
    fluid=True,
), width=8),
    dbc.Col()
])

# Add App Header
header = dbc.Row([
    dbc.Col(dbc.Jumbotron(
    [
        dbc.Container(
            [   html.H1(),
                html.H1("JOB ANALYZER", style={'margin-left': '40%'}),
                html.P(
                       "This is an interactive dashboard analyzing the job market and comparing the changes between the two genders; males and females."
                    " This app used vega job dataset. From 1850 till 2000 the data was collected for each decade (Except for 1890-1990).",
                    className="lead", style={'margin-left': '10%', 'margin-right': '10%'}
                ),
            ],
            fluid=True,
            style={'max-height': '50px', 'min-height' : '10px', 'margin-top': '-5%'}
        )
    ],
    fluid=True,
))
])

app.layout = html.Div([

    header,
    dcc.Tabs(id='tabs', value='tab-1', children=[
    dcc.Tab(label='Jobs Count', value='tab-1'),
    dcc.Tab(label='Jobs Trend', value='tab-2'),
    dcc.Tab(label='Gender Ratio', value='tab-3'), 
    ]),
    html.Div(id='tabs-content-example')
])

# App callback for selecting the tabs
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):

    if tab == 'tab-1':
        return html.Div([
             heat_map_tab_header,

            html.Iframe(
                    sandbox='allow-scripts',
                    id='plot',
                    height='600',
                    width='1200',
                    
                    style={'border-width': '0', 'margin-left': '10%'},
                    srcDoc = heat_map().to_html()
                    ),
                    
        ])
    elif tab == 'tab-2':
        return html.Div([
            job_trend_tab_header,
            dcc.Dropdown(
        id='dd-chart1',
        options=[
        {'label': 'Clerical Worker', 'value': 'Clerical Worker'},
        {'label': 'Farm Laborer', 'value': 'Farm Laborer'},
        {'label': 'Farmer', 'value': 'Farmer'},
        {'label': 'Janitor', 'value': 'Janitor'},
        {'label': 'Laborer', 'value': 'Laborer'},
        {'label': 'Manager / Owner', 'value': 'Manager / Owner'},
        {'label': 'Operative', 'value': 'Operative'},
        {'label': 'Professional - Misc', 'value': 'Professional - Misc'},
        {'label': 'Salesman', 'value': 'Salesman'},
        {'label': 'Truck / Tractor Driver', 'value': 'Truck / Tractor Driver'},
        ],
        value='Janitor',
        style={ 'margin-left': '10%', 'width' : '45%', 'verticalAlign' : 'middle'}
                ),

        html.Iframe(
                sandbox='allow-scripts',
                id='plot1',
                height='600',
                width='1700',
                
                style={'border-width': '0', 'margin-left': '20%'},
                srcDoc = trend().to_html()
                ),
                    
        ], )
    
    elif tab == 'tab-3':
        return html.Div([
            gender_ratio_header,
            html.Iframe(
                    sandbox='allow-scripts',
                    id='plot',
                    height='600',
                    width='1700',
                    style={'border-width': '0', 'margin-left': '20%'},
                    srcDoc = ratio().to_html()
                    ),
        ])
    else:
        return html.Div([
             jumbotron1,

            html.Iframe(
                    sandbox='allow-scripts',
                    id='plot',
                    height='500',
                    width='1200',
                    style={'border-width': '0', 'margin-left': '10%'},
                    srcDoc = heat_map().to_html()
                    ),
                    
        ])

# app callback for selecting the jobs from the dropdown menu

@app.callback(
dash.dependencies.Output('plot1', 'srcDoc'),
[dash.dependencies.Input('dd-chart1', 'value')])

# selecting the job and call the trend function
def select_job(job):
    '''
    Takes a job selected using the dropdown menu and update the trend plot correspondingly
    '''
    updated_plot = trend(job_to_choose=job).to_html()
    return updated_plot

    
if __name__ == '__main__':
    app.run_server(debug=True)
