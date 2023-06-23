import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title='My App',page_icon=':red_triangle_pointed_down:',layout='wide')

# Read the zip code coordinates file
#@st.cache_data
def get_zip_coordinates():
    zip_coordinates = pd.read_csv('US.txt',sep='\t',header=None)
    zip_coordinates = zip_coordinates.iloc[:,[1,9,10]]
    zip_coordinates.columns = ['Zip','lat','lon']
    zip_coordinates["Zip"] = zip_coordinates["Zip"].astype(str)
    zip_coordinates["Zip"] = zip_coordinates["Zip"].str.zfill(5)

    return zip_coordinates
zip_coordinates = get_zip_coordinates().copy()


# Read the Ceva zips and zones (zip column = 'Zip Code')
#@st.cache_data
def get_ceva_zip_reference():
    ceva_zip_reference = pd.read_csv('CEVAxWalts - Zip Guide Regional Deliveries.csv')
    ceva_zip_reference["Zip Code"] = ceva_zip_reference["Zip Code"].astype(str)
    ceva_zip_reference["Zip Code"] = ceva_zip_reference["Zip Code"].str.zfill(5)
    return ceva_zip_reference
ceva_zip_reference = get_ceva_zip_reference().copy()

# join zip coordinates to ceva zips
ceva_zip_reference = ceva_zip_reference.merge(zip_coordinates,left_on='Zip Code',right_on='Zip',how='inner')
# CEVA zips per transit
az_2 = ceva_zip_reference[(ceva_zip_reference['Origin']=='Origin - Chandler, AZ 85286') & \
                          (ceva_zip_reference['Day Transit']==2)].copy()
az_3 = ceva_zip_reference[(ceva_zip_reference['Origin']=='Origin - Chandler, AZ 85286') & \
                          (ceva_zip_reference['Day Transit']==3)].copy()
tx_2 = ceva_zip_reference[(ceva_zip_reference['Origin']=='Origin - Coppell, TX 75019') & \
                          (ceva_zip_reference['Day Transit']==2)].copy()
tx_3 = ceva_zip_reference[(ceva_zip_reference['Origin']=='Origin - Coppell, TX 75019') & \
                          (ceva_zip_reference['Day Transit']==3)].copy()

# Plot ceva zips on 4 maps
st.title('CEVA Zip Codes')
st.header('Arizona')
az_2_col, az_3_col = st.columns(2)
with az_2_col:
    st.subheader('2 Day Transit')
    st.map(az_2)
with az_3_col:
    st.subheader('3 Day Transit')
    st.map(az_3)

st.header('Texas')
tx_2_col,tx_3_col = st.columns(2)
with tx_2_col:
    st.subheader('2 Day Transit')
    st.map(tx_2)
with tx_3_col:
    st.subheader('3 Day Transit')
    st.map(tx_3)

