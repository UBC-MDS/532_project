import dash
import dash_core_components as dcc
import dash_html_components as html
import altair as alt
import vega_datasets as vega
from dash.dependencies import Input, Output

app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True
server = app.server

app.title = 'Dash app with pure Altair HTML'

df = vega.data.jobs()


def make_plot():
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
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
                    "titlePadding": 10, # guessing, not specified in styleguide
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
    #alt.themes.enable('none') # to return to default
    

    # Create a plot of the Displacement and the Horsepower of the cars dataset
def ratio():
    gap_df = df.groupby(['year', 'sex']).sum().reset_index()
    p5 = alt.Chart(gap_df).mark_bar().encode(
        alt.X("year:O", title = "Year"),
        alt.Y("perc:Q", title = "Percentage"),
        alt.Color("sex:N", title = "Sex", scale=alt.Scale(
        domain=['women', 'men'],
        range=['pink', 'steelblue']))
    ).properties(
        width=1000,
        height=400,
        title = "Employement Gender Gap Over The Years"
    )
    return p5


def trend(job_to_choose = 'Janitor'):
    chart = alt.Chart(df.query('job == @job_to_choose')).mark_line().encode(
            alt.X("year:O", title = "Year"),
            alt.Y("count:Q", title = "Count"),
            alt.Color("sex:N", scale=alt.Scale(
            domain=['women', 'men'],
            range=['pink', 'steelblue'])),
            alt.Tooltip(['year','count', 'sex']),
            alt.OpacityValue(0.7)
            
            ).properties(
            width=1000,
            height=400,
            title = job_to_choose + " Number Change Over the Years ")
    points = alt.Chart(df.query('job == @job_to_choose')).mark_point().encode(
            alt.X("year:O", title = "Year"),
            alt.Y("count:Q", title = "Count"),
            alt.Color('sex')
            )
    return chart + points


def heat_map():

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
                color=alt.Color('count', title = "Count"),
                tooltip = ['year:O', 'job:O', 'count:Q']
            ).properties(width=800, height = 500, title = "Total employments over the Years").add_selection(
            brush
            )
    bars = alt.Chart(df_men).mark_bar().encode(
        alt.X("sex:N", axis=None),
        alt.Y("count:Q", title = "Total Count"),
        alt.Color("sex:N", title = "Sex", scale=alt.Scale(
        domain=['women', 'men'],
        range=['pink', 'steelblue']))
    ).properties(
        width=90,
        height=400
    ).transform_filter(
        brush
    )
    final = plot | bars
    return final

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab1', children=[
    dcc.Tab(label='Jobs Count', value='tab-1'),
    dcc.Tab(label='Jobs Trend', value='tab-2'),
    dcc.Tab(label='Gender Ratio', value='tab-3'), 
    ]),
    html.Div(id='tabs-content-example')
    
    ### ADD CONTENT HERE like: html.H1('text'),
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):



    if tab == 'tab-1':
        return html.Div([
            html.Iframe(
                    sandbox='allow-scripts',
                    id='plot',
                    height='1000',
                    width='1500',
                    style={'border-width': '0'},
                    ################ The magic happens here
                    srcDoc = heat_map().to_html()
                    ################ The magic happens here
                    ),
        ])
    elif tab == 'tab-2':
        return html.Div([
            #Insert code for tab2 plot here
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
        # Missing option here
        ],
        value='Janitor',
        style=dict(width='45%',
                verticalAlign="middle")
                ),

        html.Iframe(
                sandbox='allow-scripts',
                id='plot1',
                height='1000',
                width='1500',
                style={'border-width': '0'},
                ################ The magic happens here
                srcDoc = trend().to_html()
                ################ The magic happens here
                ),

        ])

        
    elif tab == 'tab-3':
        return html.Div([
            html.Iframe(
                    sandbox='allow-scripts',
                    id='plot',
                    height='1000',
                    width='1500',
                    style={'border-width': '0'},
                    ################ The magic happens here
                    srcDoc = ratio().to_html()
                    ################ The magic happens here
                    ),
            
            #Insert code for tab2 plot here
        ])

@app.callback(
dash.dependencies.Output('plot1', 'srcDoc'),
[dash.dependencies.Input('dd-chart1', 'value')])

def update_plot(job):
    '''
    Takes in an job_to_choose and calls make_plot to update our Altair figure
    '''
    updated_plot = trend(job_to_choose=job).to_html()
    return updated_plot

    
if __name__ == '__main__':
    app.run_server(debug=True)