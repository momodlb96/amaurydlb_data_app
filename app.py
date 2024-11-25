import folium
import geopandas as gpd
import streamlit as st
from folium.raster_layers import WmsTileLayer
from streamlit_folium import st_folium

from data.dreal import fetch_natura2000, fetch_znieff_layers

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
- **Natural Protection Areas** [Natura 2000](https://inpn.mnhn.fr/programme/natura2000/presentation/objectifs) and [ZNIEFF](https://inpn.mnhn.fr/programme/inventaire-znieff/presentation) areas from [DREAL Bretagne](https://www.bretagne.developpement-durable.gouv.fr/spip.php?page=sommaire)
- **Fishing Activities** [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/ports-departementaux-des-cotes-darmor/)
- **Offshore Wind Projects** [Saint Brieuc - Carte Interactive: Le parc éolien au large de la baie de Saint-Brieuc](https://www.arcgis.com/home/item.html?id=359ff8497809483391012bfcc7d1bf0e)
"""
)

# Layout for Map and Table
col1, col2 = st.columns(2)

# Load GeoJSON data as GeoDataFrames
ports_gdf = gpd.read_file("data/ports-departementaux-des-cotes-darmor.geojson")
znieff_gdf = fetch_znieff_layers()
natura_gdf = fetch_natura2000()
windmills_gdf = gpd.read_file("data/windmills.geojson")

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
        marker=folium.Marker(icon=folium.Icon(icon="anchor", prefix="fa")),
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
        marker=folium.Marker(icon=folium.Icon(icon="fa-wind", prefix="fa")),
    ).add_to(m)

    # Add Znieff Areas
    popup_znieff = folium.GeoJsonPopup(
        fields=["nom", "url"],
        aliases=["Name:", "Url:"],
    )
    style_znieff = lambda x: {
        "fillColor": "#90EE90",
        "lineColor": "#006400",
        "fillOpacity": 1,
        "opacity": 1,
    }
    folium.GeoJson(
        znieff_gdf, popup=popup_znieff, name="ZNIEFF sites", style_function=style_znieff
    ).add_to(m)

    # Add Natura2000 Areas
    popup_natura = folium.GeoJsonPopup(
        fields=["nom", "url"],
        aliases=["Name:", "Url:"],
    )
    style_natura = lambda x: {
        "fillColor": "#6495ED",
        "lineColor": "#00008B",
        "fillOpacity": 1,
        "opacity": 1,
    }
    folium.GeoJson(
        natura_gdf,
        popup=popup_natura,
        name="Natura2000 areas",
        style_function=style_natura,
    ).add_to(m)

    # Layer Control
    folium.LayerControl().add_to(m)

    # Display the map
    st_folium(m, width=800, height=500)

with col2:
    st.header("Data Tables and Insights")

    col_table1, col_table2 = st.columns(2)

    with col_table1:

        # Layout for two side-by-side tables
        st.subheader("Fishing Ports")
        ports_df = ports_gdf[["COMMUNE", "ACTIVITE"]]
        ports_df.columns = [col.capitalize() for col in ports_df.columns]
        st.dataframe(ports_df, use_container_width=True)

        # Count the windmills
        windmill_count = len(windmills_gdf)
        st.subheader(f"Windmills Count: {windmill_count}")

    with col_table2:
        st.subheader("ZNIEFF Areas")
        st.dataframe(
            znieff_gdf.drop(columns=["geometry"]),
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
        )

        st.subheader("Natura2000 Areas")
        st.dataframe(
            natura_gdf.drop(columns=["geometry"]),
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
        )


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
