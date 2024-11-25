import geopandas as gpd
import pandas as pd
import requests
import streamlit as st


@st.cache_data(ttl=86400)
def fetch_ports() -> gpd.GeoDataFrame:
    headers = {
        "accept": "application/json",
    }
    response = requests.get(
        "https://tabular-api.data.gouv.fr/api/resources/dbaeb515-cfd6-451c-86d2-0844a1b95a3a/data/",
        headers=headers,
    )
    response.raise_for_status()
    df = pd.DataFrame(response.json()["data"])
    geometry = gpd.GeoSeries.from_xy(df["LONGITUDE"], df["LATITUDE"])
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    gdf.set_crs(epsg=4326, inplace=True)
    return gdf
