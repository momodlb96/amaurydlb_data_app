import logging

import geopandas as gpd
import pandas as pd
import requests
import streamlit as st

URL = "https://geobretagne.fr/geoserver/dreal_b/wfs"
PARAMS = {
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "REQUEST": "GetFeature",
    "BBOX": "-3.207907340894053,48.30790276106265,-2.228065745188843,48.971965337224646,EPSG:4326",
    "OUTPUTFORMAT": "application/json",
}


@st.cache_data(ttl=86400)
def fetch_znieff_layers() -> gpd.GeoDataFrame:
    all_gdfs: List[gpd.GeoDataFrame] = []
    for layer in [
        "dreal_b:znieff1",
        "dreal_b:znieff2",
        "dreal_b:znieff_mer_1",
        "dreal_b:znieff_mer_2",
    ]:
        try:
            response = requests.get(URL, params={"TYPENAMES": layer} | PARAMS)
            response.raise_for_status()
            layer_gdf: gpd.GeoDataFrame = gpd.read_file(response.content)
            layer_gdf.columns = [
                "id",
                "fid",
                "id_mnhn",
                "id_org",
                "nom",
                "generation",
                "url",
                "geometry",
            ]
            layer_gdf["layer"] = layer
            all_gdfs += [layer_gdf]
        except Exception as err:
            logging.warning(f"Error when fetching {layer} : {err}")
    znieff_layers = gpd.GeoDataFrame(pd.concat(all_gdfs))
    return znieff_layers


@st.cache_data(ttl=86400)
def fetch_natura2000() -> gpd.GeoDataFrame:
    try:
        response = requests.get(URL, params={"TYPENAMES": "dreal_b:ZSC"} | PARAMS)
        response.raise_for_status()
        layer_gdf: gpd.GeoDataFrame = gpd.read_file(response.content)
        layer_gdf.columns = [
            "id",
            "code_europ",
            "nom",
            "url",
            "aamp_maia",
            "statut",
            "geometry",
        ]
    except Exception as err:
        logging.warning(f"Error when fetching {layer} : {err}")
    return layer_gdf
