import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from math import ceil
import plotly_express as px
import plotly.graph_objects as go

@st.cache_resource
def get_data():
    # read in
    scatter_url = 'https://drive.google.com/file/d/1PHSheaSfnMgZ03j76hSf9DU8lUjDZ3ka/view?usp=sharing'
    scatter_url ='https://drive.google.com/uc?id=' + scatter_url.split('/')[-2]
    df = pd.read_csv(scatter_url)
    return df

def stats(dataframe):
    st.header('Data Statistics')
    st.write(dataframe.describe())

def data_header(dataframe):
    st.header('Data Header')
    st.write(dataframe.head())

def interactive_race_plot(dataframe):
    st.write('The interactive scatterplot shows the relationship between two user-selected variables, aggregated by census tract. Each point represents a census tract in Washington state.')
    lock_race = st.checkbox('Lock the x- and y-axis races to be the same (recommended for comparison of traffic stop and tract population percentage for the same race; uncheck to compare different races for traffic stops and tract population)', value=True)
    if lock_race:
        race_options = ['White', 'Black', 'Hispanic', 'AAPI', 'Other', 'BIPOC']
        race_val = st.selectbox('Select race to plot on the x- and y-axes:', options=race_options)
        x_axis_val = 'TractPct' + race_val
        y_axis_val = 'StopsPct' + race_val
    else:
        race_options = ['White', 'Black', 'Hispanic', 'AAPI', 'Other', 'BIPOC']
        x_axis_race = st.selectbox('Select Tract % Race (x-axis)', options=race_options)
        y_axis_race = st.selectbox('Select Traffic Stops % Race (y-axis)', options=race_options)
        x_axis_val = 'TractPct' + x_axis_race
        y_axis_val = 'StopsPct' + y_axis_race
    col = st.color_picker('Select a color for the plot', '#039A3E')

    plot = px.scatter(dataframe, x=x_axis_val, y=y_axis_val, trendline='ols',
                      trendline_color_override='white',
                      custom_data=dataframe)
    
    plot.data[0]['hovertemplate'] = ('<b>Point Data:</b><br>' +
                                x_axis_val + ': %{x:.3f}<br>' + y_axis_val + ': %{y:.3f}<br>' +
                               '----------------------------<br>' +
                               '<b>Census Tract Data:</b><br>' +
                               'Tract ID: %{customdata[0]}<br>' + 
                               'County: %{customdata[20]}<br>' +
                               'Population: %{customdata[21]}<br>' +
                               'Median Age: %{customdata[22]}<br>' +
                               'Median Income: $%{customdata[23]:,}/yr<br>' +
                               'Number of Police Stops: %{customdata[1]}<br>' +
                               '<br>'
                               '% Below Poverty Line: %{customdata[2]:.1f}%<br>' +
                               '% Bachelors Degree: %{customdata[25]:.1f}%<br>' +
                               '% Male: %{customdata[19]:.1f}%<br>' +
                               '<br>' +
                               '% White: %{customdata[13]:.1f}%<br>' + 
                               '% Black: %{customdata[14]:.1f}%<br>' + 
                               '% Hispanic: %{customdata[15]:.1f}%<br>' + 
                               '% Asian: %{customdata[16]:.1f}%<br>' + 
                               '% Other: %{customdata[17]:.1f}%<br>' +
                               '% BIPOC: %{customdata[18]:.1f}%<br><extra></extra>'
                               )
    plot.update_traces(marker=dict(color=col))
    plot.update_xaxes(tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], showgrid=True, gridcolor='rgb(60,60,60)', gridwidth=1)

    results = px.get_trendline_results(plot)
    
    # show the plot
    st.plotly_chart(plot)
    
    # show the trendline equation
    gradient = results.px_fit_results.iloc[0].params[1]
    intercept = results.px_fit_results.iloc[0].params[0]
    rsquared = results.px_fit_results.iloc[0].rsquared
    st.write('The equation of the trendline is:')
    st.latex(f'y = {gradient:.3f}x + {intercept:.3f}')

    if gradient < 1.0:
        st.write('''The expected gradient for exact proportionality is 1. Since the gradient is less than 1, this suggests that the overall percentage of traffic stops in
                  Washington state for the selected race is less than expected percentage for exact proportionality, given the percentage of population for the selected race.''')
    elif gradient > 1.0:
        st.write('''The expected gradient for exact proportionality is 1. Since the gradient is greater than 1, this suggests that the overall percentage of traffic stops in
                  Washington state for the selected race is greater than expected percentage for exact proportionality, given the percentage of population for the selected race.''')
    else:
        st.write('''The gradient is 1, which suggests that the overall percentage of traffic stops in Washington state for the selected race is equal to the
                    expected percentage for exact proportionality, given the percentage of population for the selected race.''')
    st.write('Note that for equality of outcome, the trendline gradients for all races should be roughly equal, which is not the case here. This suggests that there is still a racial disparity in stop occurrence.')
    st.subheader('Insights')
    st.write('''The interactive plot (by race) shows the percentage of population of each race compared to the percentage of traffic stops of subjects of that race. Each scatter plot is overlaid with the trendline for the data, and a gray dashed line showing perfect proportionality between population race percentage and traffic stops race percentage. The trendline having a lower gradient than the line of perfect proportionality suggests there are proportionally less traffic stops for all races compared to the percentage of population in that census tract of the same race.
''')
    st.write('''Despite all gradients in the interactive plot (by race) being less than 1, the variation in gradients suggests that there is still a racial disparity in traffic stop occurrence, with increasingly Black census tracts experiencing unequally increasing numbers of traffic stops for Black subjects, compared to other races. The extremely low gradient for the “Other” race category is also a notable result. One possible explanation for the lower gradient is that the race category predominantly comprises “Two or more races” and “Native American”. The trendline may be strongly influenced by census tracts with high Native American population percentage, which are located near or in tribal reservations, on which state patrols may not hold the same jurisdictional powers compared to tribal police departments.

''')
def interactive_stops_plot(dataframe):
    st.write('The interactive scatterplot shows the relationship between two user-selected variables, aggregated by census tract. Each point represents a census tract in Washington state.')
    x_options = ['White', 'Black', 'Hispanic', 'AAPI', 'Other', 'BIPOC']
    y_options = ['Searched', 'Frisked', 'ContrabandFound', 'Citation', 'Warning']
    x_axis_race = st.selectbox('Select Tract % Race (x-axis)', options=x_options)
    y_axis_activity = st.selectbox('Select Traffic Stop Activity Type (y-axis)', options=y_options)
    x_axis_val = 'TractPct' + x_axis_race
    y_axis_val = 'StopsPct' + y_axis_activity
    col = st.color_picker('Select a color for the plot', '#1AA5E0')

    plot = px.scatter(dataframe, x=x_axis_val, y=y_axis_val, trendline='ols',
                      trendline_color_override='white',
                      custom_data=dataframe)
    
    plot.data[0]['hovertemplate'] = ('<b>Point Data:</b><br>' +
                                x_axis_val + ': %{x:.3f}<br>' + y_axis_val + ': %{y:.3f}<br>' +
                               '----------------------------<br>' +
                               '<b>Census Tract Data:</b><br>' +
                               'Tract ID: %{customdata[0]}<br>' + 
                               'County: %{customdata[20]}<br>' +
                               'Population: %{customdata[21]}<br>' +
                               'Median Age: %{customdata[22]}<br>' +
                               'Median Income: $%{customdata[23]:,}/yr<br>' +
                               'Number of Police Stops: %{customdata[1]}<br>' +
                               '<br>'
                               '% Below Poverty Line: %{customdata[2]:.1f}%<br>' +
                               '% Bachelors Degree: %{customdata[25]:.1f}%<br>' +
                               '% Male: %{customdata[19]:.1f}%<br>' +
                               '<br>' +
                               '% White: %{customdata[13]:.1f}%<br>' + 
                               '% Black: %{customdata[14]:.1f}%<br>' + 
                               '% Hispanic: %{customdata[15]:.1f}%<br>' + 
                               '% Asian: %{customdata[16]:.1f}%<br>' + 
                               '% Other: %{customdata[17]:.1f}%<br>' +
                               '% BIPOC: %{customdata[18]:.1f}%<br><extra></extra>'
                               )
    plot.update_traces(marker=dict(color=col))
    plot.update_xaxes(tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], showgrid=True, gridcolor='rgb(60,60,60)', gridwidth=1)

    results = px.get_trendline_results(plot)
    
    # show the plot
    st.plotly_chart(plot)
    
    # show the trendline equation
    gradient = results.px_fit_results.iloc[0].params[1]
    intercept = results.px_fit_results.iloc[0].params[0]

    st.write(f'The equation of the trendline is:')
    st.latex(f'y = {gradient:.5f}x + {intercept:.5f}')

    if gradient < -0.005:
        st.write('''The expected gradient for equality of stop activity is 0. Since the gradient is negative, this suggests that the overall percentage of stop activity in Washington state
                  reduced with the percentage of population for the selected race.''')
    elif gradient > 0.005:
        st.write('''The expected gradient for equality of stop activity is 0. Since the gradient is negative, this suggests that the overall percentage of stop activity in Washington state
                  increased with the percentage of population for the selected race.''')
    elif 0 < gradient <= 0.005:
        st.write('The gradient is positive, and very close to zero, which suggests that there is a very weak relationship between the percentage of traffic stops and the percentage of population for the selected race.')
    elif -0.005 <= gradient < 0:
        st.write('The gradient is negative, and very close to zero, which suggests that there is a very weak relationship between the percentage of traffic stops and the percentage of population for the selected race.')
    else:
        st.write('The gradient is zero, which suggests that there is no relationship between the percentage of traffic stops and the percentage of population for the selected race.')
    st.write('''Note that for equality of outcome across all races, the trendline gradients for all races should be roughly equal, which is not the case here 
                 (e.g. some gradients are in different orders of magnitude). This suggests that there is still a racial disparity in stop activity.''')
    st.subheader('Insights')
    st.write('''A second type of scatter plot is presented on the interactive plot (by stop activity) section, where the tract population percentage by race is plotted against the percentage of five different stop activities: a search being conducted, a frisk being performed, contraband being found, a citation being issued, and a warning being issued. For equality of outcome, one would expect the trendline gradient to be zero (i.e., no impact of increasing percentage of population of a particular race on traffic stop activity). This is largely the case; gradients are very close to zero for all races and all stop activities, though there are some situations where gradients for the same activity type still differ between two races by an order of magnitude. This means that some amount of racial disparity still exists in whether particular types of activities occur during a traffic stop.
''')

def interactive_all_plot(dataframe):
    st.write('The interactive scatterplot shows the relationship between two user-selected variables, aggregated by census tract. Each point represents a census tract in Washington state.')
    options_list = list(dataframe.columns.values)
    options_list.remove('TractID')
    options_list.remove('geometry')
    options_list.remove('County')
    
    x_options = options_list
    y_options = options_list
    x_axis_val = st.selectbox('Select X-Axis Variable', options=x_options)
    y_axis_val = st.selectbox('Select Y-Axis Variable', options=y_options)
    col = st.color_picker('Select a color for the plot', '#E4C41C')

    plot = px.scatter(dataframe, x=x_axis_val, y=y_axis_val, trendline='ols',
                      trendline_color_override='white',
                      custom_data=dataframe)
    
    plot.data[0]['hovertemplate'] = ('<b>Point Data:</b><br>' +
                                x_axis_val + ': %{x:.3f}<br>' + y_axis_val + ': %{y:.3f}<br>' +
                               '----------------------------<br>' +
                               '<b>Census Tract Data:</b><br>' +
                               'Tract ID: %{customdata[0]}<br>' + 
                               'County: %{customdata[20]}<br>' +
                               'Population: %{customdata[21]}<br>' +
                               'Median Age: %{customdata[22]}<br>' +
                               'Median Income: $%{customdata[23]:,}/yr<br>' +
                               'Number of Police Stops: %{customdata[1]}<br>' +
                               '<br>'
                               '% Below Poverty Line: %{customdata[2]:.1f}%<br>' +
                               '% Bachelors Degree: %{customdata[25]:.1f}%<br>' +
                               '% Male: %{customdata[19]:.1f}%<br>' +
                               '<br>' +
                               '% White: %{customdata[13]:.1f}%<br>' + 
                               '% Black: %{customdata[14]:.1f}%<br>' + 
                               '% Hispanic: %{customdata[15]:.1f}%<br>' + 
                               '% Asian: %{customdata[16]:.1f}%<br>' + 
                               '% Other: %{customdata[17]:.1f}%<br>' +
                               '% BIPOC: %{customdata[18]:.1f}%<br><extra></extra>'
                               )
    plot.update_traces(marker=dict(color=col))
    plot.update_xaxes(showgrid=True, gridcolor='rgb(60,60,60)', gridwidth=1)

    results = px.get_trendline_results(plot)
    
    # show the plot
    st.plotly_chart(plot)
    
    # show the trendline equation
    gradient = results.px_fit_results.iloc[0].params[1]
    intercept = results.px_fit_results.iloc[0].params[0]

    st.write(f'The equation of the trendline is:')
    st.latex(f'y = {gradient:.5f}x + {intercept:.5f}')

# Page begins here
        
df = get_data()

st.title('Tract-level Aggregate Analysis')
st.subheader('Correlation Between Traffic Stop Subject and Location')

st.write('''
The correlation between traffic stop subject and location was analyzed using a scatter plot and ordinary least squares regression. The traffic stops data that was aggregated by census tract was plotted against characteristics of the census tract itself, and is presented on the StopScatterPlot page of this app.
''')
st.sidebar.title('Navigation')

options = st.sidebar.radio('Page Options', options=[
'Home', 
'Data Statistics', 
'Data Header', 
'Interactive Plot (by Race)',
'Interactive Plot (by Stop Activity)',
'Interactive Plot (All)'
])

if options == 'Data Statistics':
    stats(df)
elif options == 'Data Header':
    data_header(df)
elif options == 'Interactive Plot (by Race)':
    interactive_race_plot(df)
elif options == 'Interactive Plot (by Stop Activity)':
    interactive_stops_plot(df)
elif options == 'Interactive Plot (All)':
    interactive_all_plot(df)