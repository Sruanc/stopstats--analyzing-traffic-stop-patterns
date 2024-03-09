import streamlit as st
import folium
import branca
from folium.features import GeoJsonPopup
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
from shapely import wkt

@st.cache_data
def get_data():
    '''
    Read and format data
    Input: None
    Output: census_data, stop_data geodataframes
    '''
    # Read in census data
    census_url = 'https://drive.google.com/file/d/1kt7EPrEK5T22ryGcmanxRY67AIr9Gyjq/view?usp=sharing'
    census_url = 'https://drive.google.com/uc?id=' + census_url.split('/')[-2]
    census_data = pd.read_csv(census_url)

    # Read in stop data
    stop_url = 'https://drive.google.com/file/d/1nK5givbyegb7w9rSNLbEr-hdmXxKEnFb/view?usp=sharing'
    stop_url = 'https://drive.google.com/uc?id=' + stop_url.split('/')[-2]
    stop_data = pd.read_csv(stop_url)
    
    # Convert to GeoDataFrame
    census_data["geometry"] = census_data["geometry"].apply(wkt.loads)
    stop_data["geometry"] = stop_data["geometry"].apply(wkt.loads)
    census_data = gpd.GeoDataFrame(census_data, geometry=census_data.geometry, crs='EPSG:4326')
    stop_data = gpd.GeoDataFrame(stop_data, geometry=stop_data.geometry, crs='EPSG:4326')
    
    # Turn timestamp into string to be JSON compatible
    stop_data['date_time'] = pd.to_datetime(stop_data['date_time'])
    stop_data['time_of_day'] = stop_data['date_time'].dt.hour

    return census_data, stop_data

def generate_map(_census_gdf, _stop_gdf, _demographic_var, _time_of_day):
    '''
    Generate map with base layer of demographic census data, with police stop cluster marker layer.
    Popup functionality for both.
    '''
    # Filter stop data based on the selected time of day
    filtered_stop_data = _stop_gdf[_stop_gdf['time_of_day'] == _time_of_day]

    colormap = branca.colormap.LinearColormap(
        vmin=_census_gdf[_demographic_var].quantile(0.0),
        vmax=_census_gdf[_demographic_var].quantile(1),
        colors=["white", "red"],
        caption=_demographic_var
    )

    m = folium.Map(location=[47.4405, -121.8836], zoom_start=9, prefer_canvas=True)

    popup = GeoJsonPopup(
        fields=["TractID", _demographic_var],
        aliases=["Tract", _demographic_var],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    folium.GeoJson(
        _census_gdf,
        style_function=lambda x: {
            "fillColor": colormap(x["properties"][_demographic_var])
            if x["properties"][_demographic_var] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        popup=popup,
    ).add_to(m)

    # Create MarkerCluster for stop data
    marker_cluster = MarkerCluster()
    for i in range(0, len(filtered_stop_data)):
        stop_info = filtered_stop_data.iloc[i]
        popup_html = f"""
            <b>Subject Race:</b> {stop_info.subject_race}<br>
            <b>Search Conducted:</b> {stop_info.search_conducted}<br>
            <b>Outcome:</b> {stop_info.outcome}<br>
            <b>Time:</b> {stop_info.date_time}<br>
            """
        iframe = folium.IFrame(popup_html, width=200, height=100)
        marker = folium.Marker(
            location=[stop_info['geometry'].y, stop_info['geometry'].x],
            icon=folium.Icon(color='red', icon='car', prefix='fa'),
            popup=folium.Popup(iframe, minwidth=200, maxwidth=200))
        marker.add_to(marker_cluster)
    marker_cluster.add_to(m)

    colormap.add_to(m)

    return m

def main():
    st.title("Police Stop Data Visualization")
    st.write("""
    This web app visualizes police stop data along with demographic census data.
    """)

    # Description for "Stops by Time"
    st.subheader("Stops by Time")
    st.write("""
    Understanding the temporal patterns of police stops provides valuable insights into law enforcement activities throughout the day. By visualizing police stops alongside demographic census data, we gain a comprehensive understanding of the spatial and temporal dynamics of law enforcement interactions within King County.
    
    **Insights:**
    **Temporal Patterns:** The map visualizes police stops across different times of the day. As you adjust the slider to select the time of day, you'll notice fluctuations in the density and distribution of police stops. These variations shed light on when law enforcement activities are more prevalent within the county.
    
    **Peak Hours:** Certain times of the day may exhibit higher concentrations of police stops compared to others. These peak hours could coincide with rush hour traffic, events, or other factors influencing law enforcement activities.
    
    **Temporal Correlations:** Exploring the relationship between the time of day and the locations of police stops allows us to identify potential correlations. For instance, we may observe increased stoppage rates during late-night hours or specific patterns during morning or afternoon rush hours.
    
    By examining police stops through a temporal lens, we aim to uncover nuanced patterns that contribute to a deeper understanding of law enforcement dynamics and their intersection with demographic characteristics within King County.
    """)
    
    census_gdf, stop_gdf = get_data()
    demographic_var = "PctBlack"
    
    # Create Streamlit slider to select time of day
    st.sidebar.title("Settings")
    time_of_day = st.sidebar.slider('Select Time of Day', 0, 23, 12)

    m = generate_map(census_gdf, stop_gdf, demographic_var, time_of_day)
    st_folium(m, width=700, height=500)

if __name__ == "__main__":
    main()
