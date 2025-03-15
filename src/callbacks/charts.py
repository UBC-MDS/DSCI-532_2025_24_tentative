from dash import Input, Output, callback
import altair as alt
import pandas as pd
import plotly.express as px
import time
from utils.cache import cache
from data.police_data import police_data

data = police_data

def filter_data(data, year, race, age, armed):
    """Filter the data based on global selections."""
    df = data.copy()
    if year:
        df = df[df['year'].isin(year)]
    if race:
        df = df[df['raceethnicity'].isin(race)]
    if age:
        df = df[df['age_group'].isin(age)]
    if armed:
        df = df[df['armed'].isin(armed)]
    return df

@cache.memoize()
def create_map(data, var):
    """Create the US Map with scatter points."""
    label = {
        'raceethnicity': 'Race/Ethnicity',
        'age_group': 'Age Group',
        'armed': 'Armed Status'
    }
    if var == 'raceethnicity':
        color_map = {
            'Black': '#1f77b4', 'White': '#ff7f0e', 'Hispanic/Latino': '#2ca02c', 'Asian/Pacific Islander': '#d62728',
            'Native American': '#9467bd', 'Arab-American': '#8c564b', 'Other': '#e377c2'
        }
    elif var == 'age_group':
        color_map = {
            'Under 19': '#1f77b4', '20-39': '#ff7f0e', '40-59': '#2ca02c', 'Above 60': '#d62728', 'Unknown': '#9467bd'
        }
    else:
        color_map = {
            'Unarmed': '#1f77b4', 'Firearm': '#2ca02c', 'Non-lethal firearm': '#d62728',
            'Knife': '#9467bd', 'Vehicle': '#8c564b', 'Disputed': '#e377c2', 'Other': '#ff7f0e'
        }
    map = px.scatter_map(
        data, 
        lat="latitude", 
        lon="longitude", 
        color=var,
        color_discrete_map=color_map, 
        labels=label,
        map_style='open-street-map', 
        custom_data=['name', 'city', 'state', 'date', 'raceethnicity', 'age', 'armed'],
        zoom=3,
        height=400,
        width=680
        )
    map.update_traces(
        hovertemplate = 
                "<b>%{customdata[0]}</b><br><br>" +
                "City: %{customdata[1]}, %{customdata[2]}<br>" +
                "Date of Death: %{customdata[3]|%Y-%m-%d}<br>" +
                "Race/Ethnicity: %{customdata[4]}<br>" +
                "Age: %{customdata[5]}<br>" +
                "Armed Status: %{customdata[6]}" +
                "<extra></extra>",
        marker={'sizemode': 'area', 'size': 9},
        mode='markers'
    )
    map.update_layout(
        margin=dict(t=0, l=0, b=0, r=0, pad=0),
        legend=dict(
            y=1, 
            yanchor="bottom", 
            orientation='h',
            font=dict(weight=250, size=13, family='Arial'),
            title=dict(
                side='top',
                font=dict(color='black', size=17, weight=900, family='Arial')
            )
        ),
    )
    return map.to_dict()

@cache.memoize()
def create_bar(data, var):
    """Create the race/ethnicity barplot."""
    if var == 'age_group':
        bar = alt.Chart(data).mark_bar().encode(
                x = alt.X(var, axis=alt.Axis(labelAngle=0), title=' '),
                y = 'count()',
                color = alt.Color(
                    'gender', title='Gender',
                    scale=alt.Scale(scheme="viridis"),
                    legend=alt.Legend(orient="top")
                    ),
                tooltip = 'count()'
            ).properties(
                height=350, 
                width=320
            ).configure_axis(
                labelFontSize=14,  
                titleFontSize=16
            ).configure_legend(
                labelFontSize=14, 
                titleFontSize=16
            ).to_dict()
        return bar
    else: 
        bar = alt.Chart(data).mark_bar().encode(
                x = 'count()',
                y = alt.Y(var,  title=' ').sort('-x'),
                color = alt.Color(
                    'gender', title='Gender',
                    scale=alt.Scale(scheme="viridis"),
                    legend=alt.Legend(orient="top")
                    ),
                tooltip = 'count()'
            ).properties(
                height=350, 
                width=280
            ).configure_axis(
                labelFontSize=14,  
                titleFontSize=16
            ).configure_legend(
                labelFontSize=14, 
                titleFontSize=16
            ).to_dict()
        return bar

def filter_states(data, top_state):
    """Filter the data based on the number of top states input."""
    states = data['state'].value_counts()[:top_state].index.to_list()
    df = data[data['state'].isin(states)]
    return df

@cache.memoize()
def create_state_time(data, top_state):
    """Create the combined plots of top states barplot and time-series line plot"""
    select_state = alt.selection_point(
        fields=['state']
        )
    top10 = alt.Chart(data).mark_bar(color='teal', cursor="pointer").encode(
            x=alt.X('count()', title='Number of Killings'),
            y=alt.Y('state', sort='-x', title=' '),
            tooltip = 'count()',
            opacity=alt.condition(select_state, alt.value(1), alt.value(0.2))
        ).add_params(
            select_state
        ).properties(
            title=f'Top {top_state} States by Police Killings',
            height=400,
            width=250
        )

    color_list = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
        "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173"
    ]
    time = alt.Chart(data).mark_line().encode(
            x=alt.X('yearmonth(date):O', title='Month of Year'),
            y=alt.Y('count()', title='Number of Killings'),
            color=alt.Color(
                'state',
                scale=alt.Scale(
                    domain=data['state'].unique(),
                    range=color_list[:len(data['state'].unique())]
                ),
                legend=None
            ),
            tooltip=['yearmonth(date):O', 'count()', 'state'],
            opacity=alt.condition(
                select_state, alt.value(0.8), alt.value(0.1)
            )
        ).properties(
            title='Police Killing Deaths by Months', 
            height=400, 
            width=680
        )
    top10_time = (top10 | time).configure_axis(
            labelFontSize=14,  
            titleFontSize=16   
        ).configure_title(
            fontSize=18  
        ).configure_legend(
            labelFontSize=14, 
            titleFontSize=16
        ).to_dict()
    return top10_time

# Server side callbacks/reactivity
@callback(
    Output('map', 'figure'),
    Output('race_bar', 'spec'),
    Output('top10_time', 'spec'),
    Input('year', 'value'),
    Input('race-dropdown', 'value'),
    Input('age-dropdown', 'value'), 
    Input('armed-dropdown', 'value'),
    Input('map_dropdown', 'value'), 
    Input('bar_dropdown', 'value'), 
    Input('top_state', 'value'), 
)
@cache.memoize()
def create_chart(year, race, age, armed, map_dropdown, bar_dropdown, top_state):
    data_filtered = filter_data(data, year, race, age, armed)
    
    time.sleep(1)
    map = create_map(data_filtered, map_dropdown)
    bar = create_bar(data_filtered, bar_dropdown)

    data_filtered = filter_states(data_filtered, top_state)
    top10_time = create_state_time(data_filtered, top_state)

    return map, bar, top10_time
