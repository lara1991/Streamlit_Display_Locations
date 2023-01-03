import geocoder
import streamlit as st
from streamlit_folium import st_folium
import folium

import pyodbc

from db_connection_access import Database

BING_API_KEY = "Anxxxxxx" ## bing API key
DB_PATH = "G:\\database.mdb" ## sample


def get_latlng(address):
    g = geocoder.bing(address,key=BING_API_KEY)
    results = g.json
    
    if results is None:
        latlng = [7.365201,80.034111]
    else:
        latlng = [results['lat'],results['lng']]
    
    return latlng
    

basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
    )
    
}

def get_address_list(db_connection,sql_query):
    df = db_connection.search_and_get_data(sql_query)
    df = df[['SBUCode','CompName','Address']]
    return df

@st.cache(allow_output_mutation=True)
def get_location_list(table_name='sbu'):
    db_conn = Database(database_path=DB_PATH)
    sql_query = f'select * from {table_name}'
    address_list_from_db = get_address_list(db_connection=db_conn,sql_query=sql_query)
    return address_list_from_db,db_conn

df_company_loc_list,database_con = get_location_list()

## one of the default location
m = folium.Map(location=[7.9570,80.7603],zoom_start=8)
basemaps['Google Maps'].add_to(m)

## add markers for each company location
company_idxs_to_access = {}

for idx,row in df_company_loc_list.iterrows():
    company_id = row[0]
    company_name = row[1]
    company_address = row[2]
    tooltip = f"{company_name}: {company_address}"
    
    latlng = get_latlng(address=company_address)
    company_idxs_to_access[tuple(latlng)] = company_id
    
    folium.Marker(
        latlng,
        tooltip=tooltip,
        icon=folium.Icon(color='red',icon="location-dot",prefix='fa')
    ).add_to(m)

st.title("Company Locations")
c1,c2 = st.columns([3,1])

with c1:
    st_data = st_folium(m,width=900,height=800,returned_objects=['last_object_clicked'])
with c2:
    st.header("Company Details")
    clicked_location = tuple([st_data["last_object_clicked"]['lat'],st_data["last_object_clicked"]['lng']])
    company_id_clicked = company_idxs_to_access[clicked_location]
    tmp_df_row = df_company_loc_list[df_company_loc_list['SBUCode'] == company_id_clicked]
    tmp_df_row.reset_index(inplace=True)
    # print(tmp_df_row.loc[0,'office_name'])
    st.write(f"Company ID: {company_id_clicked}")
    st.write(f"Company Name: {tmp_df_row.loc[0,'CompName']}")
    st.write(f"Company Address: {tmp_df_row.loc[0,'Address']}")






