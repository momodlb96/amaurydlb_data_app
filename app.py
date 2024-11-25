import folium
import geopandas as gpd
import streamlit as st
from folium.raster_layers import WmsTileLayer
from streamlit_folium import st_folium

# Page Configuration
st.set_page_config(
    page_title="Baie de Saint-Brieuc Overview",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("Baie de Saint-Brieuc: Environment and Industry")

# Description
st.markdown(
    """
The Baie de Saint-Brieuc is a vital ecological and economic area in France. This app provides an overview of its:
- **Natural Protection Areas** [DREAL Bretagne](https://www.bretagne.developpement-durable.gouv.fr/natura-2000-r94.html)
- **Fishing Activities** [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/ports-departementaux-des-cotes-darmor/)
- **Offshore Wind Projects** [Saint Brieuc - Carte Interactive: Le parc éolien au large de la baie de Saint-Brieuc](https://www.arcgis.com/home/item.html?id=359ff8497809483391012bfcc7d1bf0e)
"""
)

# Layout for Map and Table
col1, col2 = st.columns([2, 1])

# Load GeoJSON data as GeoDataFrames
ports_gdf = gpd.read_file("data/ports-departementaux-des-cotes-darmor.geojson")
natura2000_gdf = gpd.read_file("data/natura2000_zps.geojson")
windmills_gdf = gpd.read_file("data/windmills.geojson")

# Count the windmills
windmill_count = len(windmills_gdf)

with col1:
    # Add the map
    st.header("Map of the Baie de Saint-Brieuc")
    map_center = [48.55, -2.8]  # Coordinates of Baie de Saint-Brieuc
    m = folium.Map(location=map_center, zoom_start=10)

    # Add Fishing Activity Markers
    popup_ports = folium.GeoJsonPopup(
        fields=["COMMUNE", "ACTIVITE"],
        aliases=["City:", "Activity:"],
    )
    folium.GeoJson(
        ports_gdf,
        popup=popup_ports,
        name="Fishing Ports",
    ).add_to(m)

    # Add Offshore Wind Farm
    popup_windmills = folium.GeoJsonPopup(
        fields=["Turbine_Name"],
        aliases=["Turbine:"],
    )
    folium.GeoJson(
        windmills_gdf,
        popup=popup_windmills,
        name="Windmills",
    ).add_to(m)

    # Add Natura 2000 Areas
    popup_natura2000 = folium.GeoJsonPopup(
        fields=["SITENAME"],
        aliases=["Name:"],
    )
    folium.GeoJson(
        natura2000_gdf,
        popup=popup_natura2000,
        name="Natura 2000 Sites",
    ).add_to(m)

    # Layer Control
    folium.LayerControl().add_to(m)

    # Display the map
    st_folium(m, width=800, height=500)

with col2:
    st.header("Data Tables and Insights")
    st.subheader(f"Windmills Count: {windmill_count}")

    # Layout for two side-by-side tables
    col_table1, col_table2 = st.columns(2)

    with col_table1:
        st.subheader("Fishing Ports")
        ports_df = ports_gdf[["COMMUNE", "ACTIVITE"]]
        ports_df.columns = [col.capitalize() for col in ports_df.columns]
        st.dataframe(ports_df)

    with col_table2:
        st.subheader("Natura 2000 Sites")
        natura2000_df = natura2000_gdf[["SITENAME", "SITECODE"]]
        natura2000_df.columns = [col.capitalize() for col in natura2000_df.columns]
        st.dataframe(natura2000_df)

# Sidebar
st.sidebar.header("About This App")
st.sidebar.markdown(
    """
This app is developed to provide a spatial overview of the activities and protected areas in the Baie de Saint-Brieuc.
"""
)
st.sidebar.info(
    "Data displayed is for demonstration purposes and may not reflect actual boundaries or activity locations."
)
