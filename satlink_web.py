# this script generates an web app with streamlit to calculate a single point downlink availability
# the scope of this window is the same as Single Point Calculation -> Downlink Performance from the Qt GUI

from models.util import convert_path_os
import streamlit as st
import subprocess
import pandas as pd
import pickle
import platform
from link_performance import sp_link_performance


st.set_page_config(page_title='Satlink', page_icon='UI\icon.png', layout="wide", initial_sidebar_state="auto", menu_items=None)

# creating the sidebar
st.sidebar.title('Satlink')
st.sidebar.image('pics/LogoSatLink225_225_white.png', width=150)
st.sidebar.subheader('SatLink is a python based application that runs speciffic satellite downlink calcullations')
st.sidebar.subheader('This project is a attempt to simplify satellite\'s link budget calcullations and to create a tool for teaching purposes')
st.sidebar.markdown('**Please refer to [**github**](https://github.com/cfragoas/SatLink) for more information**')

# this is to tune the sidebar size
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Ground Station variables
st.subheader('Ground Station')
grstat_exp = st.expander(label='', expanded=True)
with grstat_exp:
    grstat_col1, grstat_col2= st.columns(2)

    # grstat_lat.header("Latitude (degress)")
    site_lat = grstat_col1.number_input('Latitude (degrees)')


    # grstat_long.header("Longitude (degrees)")
    site_long = grstat_col2.number_input('Longitude (degrees)')

# Satellite variables
st.subheader('Satellite')
sat_exp = st.expander(label='', expanded=True)
path = convert_path_os('models\\Modulation_dB.csv')
mod_list = pd.read_csv(path, sep=';')['Modcod']  # to fill modulation combobox

with sat_exp:
    sat_col1, sat_col2, sat_col3, sat_col4, sat_col5 = st.columns(5)

    sat_long = sat_col1.number_input('Longitude (degress)')
    max_bw = sat_col1.number_input('Transponder s max bandwidith (MHz)')


    sat_height = sat_col2.number_input('Altitude (Km)')
    bw_util = sat_col2.number_input('Effective bandwith (MHz)')

    
    freq = sat_col3.number_input('Frequency (GHz)')
    roll_off = sat_col3.number_input('Roll-off')

    max_eirp = sat_col4.number_input('EIRP (dBW)')
    modcod = sat_col4.selectbox('Modulation', mod_list)

    pol = sat_col5.selectbox('Polarization', ('Horizontal', 'Vertical', 'Circular'))

# Reception variables
st.subheader('Reception Characteristcs')
rcp_exp = st.expander(label='', expanded=True)
with rcp_exp:
    rcp_col1, rcp_col2, rcp_col3, rcp_col4 = st.columns(4)

    ant_size = rcp_col1.number_input('Antenna Size (m)')
    ant_eff = rcp_col1.number_input('Antenna Efficiency')

    lnb_gain = rcp_col2.number_input('LNB Gain (dB)')
    lnb_temp = rcp_col2.number_input('LNB Noise Temp. (K)')

    cable_loss = rcp_col3.number_input('Cable Loss dB)')
    aditional_losses = rcp_col3.number_input('Additional Losses (dB)')

    max_depoint = rcp_col4.number_input('Maximum depoing (degrees)')


db_field = st.button('Run Calculations')  # this button will run sp_link_performance from link_performance.py 
if db_field:
    path = convert_path_os('temp\\args.pkl')  # dumping the pickle file with all the variables
    with open(path, 'wb') as f:
        pickle.dump(
            [site_lat, site_long, sat_long, freq, max_eirp, sat_height, max_bw, bw_util,
                modcod, pol, roll_off, ant_size, ant_eff, lnb_gain, lnb_temp, aditional_losses,
                cable_loss, max_depoint, 1, 0], f)
        f.close()

    sp_link_performance()  # function to calculate the link performace

    path = convert_path_os('temp\\out.txt')
    with open(path, 'r') as output:  # this will pick the output form sp_link_performance
        x = output.read()

    st.text(x)


# run = st.button('Debug calc')

# if run:
#     c = st.container()
#     with c:
#         value = subprocess.check_output(['python', 'single_point_example.py'], shell=True, text=True)
#         st.text(value)
    