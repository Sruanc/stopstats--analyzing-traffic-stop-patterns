import branca
import folium
import geopandas as gpd
import pandas as pd
from shapely import wkt
import streamlit as st
from folium.features import GeoJsonPopup, GeoJsonTooltip
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

@st.cache_resource
def get_data():
    '''
    read and format data
    input: none
    output: census_data, stop_data geodataframes
    '''
    # read in
    census_url = 'https://drive.google.com/file/d/1kt7EPrEK5T22ryGcmanxRY67AIr9Gyjq/view?usp=sharing'
    census_url='https://drive.google.com/uc?id=' + census_url.split('/')[-2]
    census_data = pd.read_csv(census_url)

    stop_url = 'https://drive.google.com/file/d/1nK5givbyegb7w9rSNLbEr-hdmXxKEnFb/view?usp=sharing'
    stop_url='https://drive.google.com/uc?id=' + stop_url.split('/')[-2]
    stop_data = pd.read_csv(stop_url)
    
    # convert to gdf
    census_data["geometry"] = census_data["geometry"].apply(wkt.loads)
    stop_data["geometry"] = stop_data["geometry"].apply(wkt.loads)
    census_data = gpd.GeoDataFrame(census_data, geometry=census_data.geometry, crs='EPSG:4326')
    stop_data = gpd.GeoDataFrame(stop_data, geometry=stop_data.geometry, crs='EPSG:4326')
    
    # turn timestamp into string to be json compatible
    stop_data['date_time'] = stop_data['date_time'].astype(str)

    # simplify geometry
    census_data['geometry'] = census_data['geometry'].simplify(0.0001)

    return census_data, stop_data

@st.cache_resource(experimental_allow_widgets=True)
def generate_map_for_race(_census_gdf, _stop_gdf, _demographic_var):
    '''
    generate map with base layer of demographic census data, with police stop cluster marker layer for a specific race.
    input: census_data, stop_data geodataframes, demographic variable, race
    output: folium map
    '''
    m = folium.Map(location=[47.4405, -121.8836], zoom_start=9, prefer_canvas=True)

    colormap = branca.colormap.LinearColormap(
    vmin=_census_gdf[_demographic_var].quantile(0.05),
    vmax=_census_gdf[_demographic_var].quantile(0.95),
    colors=["white", "red"],
    caption=_demographic_var
    )

    generate_choropleth_map(_census_gdf, _demographic_var, colormap).add_to(m)

    # if pd.isnull(race):  # Check if the selected race is NaN
    #     race_data = stop_gdf[pd.isnull(stop_gdf['subject_race'])]
    # else:
    #     race_data = stop_gdf[stop_gdf['subject_race'] == race]  # Filter by selected race

    generate_marker_cluster(_stop_gdf).add_to(m)

    colormap.add_to(m)

    with st.form(key='main_map'):
        st.form_submit_button(disabled=True)
        return st_folium(m, width=700, height=500)


def generate_choropleth_map(_census_gdf, _demographic_var, _colormap):
    popup = GeoJsonPopup(
    fields=["TractID", _demographic_var],
    aliases=["Tract", _demographic_var],
    localize=True,
    labels=True,
    style="background-color: yellow;",
    )

    choro = folium.GeoJson(
        _census_gdf,
        style_function=lambda x: {
            "fillColor": _colormap(x["properties"][_demographic_var])
            if x["properties"][_demographic_var] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        popup=popup,
    )
    return choro


def generate_marker_cluster(_stop_gdf):
    marker_cluster = MarkerCluster()
    for i in range(len(_stop_gdf)):
        iframe = folium.IFrame("<b>Subject Race: </b> " + str(_stop_gdf.iloc[i]['subject_race']) + "<br><b>Subject Age: </b> " + str(_stop_gdf.iloc[i]['subject_age']) + "<br><b>Search Conducted: </b> " + str(_stop_gdf.iloc[i]['search_conducted']) + "<br><b>Outcome: </b> " + str(_stop_gdf.iloc[i]['outcome']), width=200, height=100)
        marker = folium.Marker(
            location=[_stop_gdf.iloc[i]['geometry'].y, _stop_gdf.iloc[i]['geometry'].x],
            icon=folium.Icon(color='red', icon='car', prefix='fa'),
            popup=folium.Popup(iframe, minwidth=100, maxwidth=100)
        )
        marker.add_to(marker_cluster)
    return marker_cluster

def main():
    census_gdf, stop_gdf = get_data()
    demographic_var = "PctBlack"
    
     # Title and subtitle
    st.title("Geospatial Results and Analysis")
    st.subheader("A geospatial analysis was performed to understand demographic spatial patterns and potential correlations with police stops.")
    st.write("Race, age, gender, income and eduation demographics at the census tract level are presented on StopByRaceMap page of this app. High concentrations of BIPOC individuals are located in the Southeast portion of King County, specifically in south Seattle, as well as east of Seattle (Bellevue, Redmond). These areas also display a larger portion of individuals below the poverty level. Interestingly enough, downtown Seattle (Sodo in particular) has more male than female residents.")

    st.write("The distribution and count of police stops in King County were also plotted. Washington State Patrol stops are concentrated along major roadways (state highways, interstates, etc.). The census tract with the highest number of police stops is located in the Sodo neighborhood of Seattle. Interestingly enough, this is also the census tract with the highest proportion of male residents. However, stop data is not necessarily reflective of the residents who live in the census tract that they are stopped in, as travelers may be coming from any part of the county. The census tract with the most stops also touches three different major routes–SR-99, I-5, and I-90– as well as land uses which generate many trips (Lumen Field, T-Mobile Park). These transportation network and land use factors may be better explanatory factors for the high amount of stops.")
    # races = stop_gdf['subject_race'].unique()
    # selected_race = st.selectbox("Select Race", races)
    demographic_variables = census_gdf.columns[2:-1]
    demographic_var = st.selectbox("Select Demographic Variable", demographic_variables)
    
    generate_map_button = st.checkbox("Generate Map")
    map_placeholder = st.empty()  # Placeholder for the map
    
    if generate_map_button:
        st.header(f"Spatial distribution of {demographic_var} and police stops in King County")
        map_placeholder = generate_map_for_race(census_gdf, stop_gdf, demographic_var)
        st.stop()  # Stop execution after generating the map

if __name__ == "__main__":
    main()
