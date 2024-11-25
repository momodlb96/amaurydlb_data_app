import folium
import geopandas as gpd
import requests
import streamlit as st
from streamlit_folium import st_folium


@st.cache_data(ttl=86400)
def fetch_windmills() -> gpd.GeoDataFrame:
    # Define the Esri Feature Layer URL
    feature_layer_url = "https://services2.arcgis.com/If7uF4q7Do2KTuHr/arcgis/rest/services/SBR_project_AM_pFRAsbr077_WTG_Layout_2022/FeatureServer/4/query"

    # Fetch the GeoJSON data
    params = {
        "where": "1=1",  # Query all features
        "outFields": "*",  # Fetch all fields
        "f": "geojson",  # Request GeoJSON format
    }
    response = requests.get(feature_layer_url, params=params)
    response.raise_for_status()
    gdf = gpd.read_file(response.content)
    return gdf
