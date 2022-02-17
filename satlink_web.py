import streamlit as st
import subprocess


# st.set_page_config(layout="wide")
st.set_page_config(page_title='Satlink', page_icon='UI\icon.png', layout="wide", initial_sidebar_state="auto", menu_items=None)

st.markdown('SatLink is a python based application that makes satellite downlink link budget calculations.')

st.subheader('Ground Station')
grstat_exp = st.expander(label='', expanded=True)
with grstat_exp:
    grstat_col1, grstat_col2= st.columns(2)

    # grstat_lat.header("Latitude (degress)")
    grstat_col1.number_input('Latitude (degrees)')


    # grstat_long.header("Longitude (degrees)")
    grstat_col2.number_input('Longitude (degrees)')


st.subheader('Satellite')
sat_exp = st.expander(label='', expanded=True)
with sat_exp:
    sat_col1, sat_col2, sat_col3, sat_col4 = st.columns(4)

    sat_col1.number_input('Longitude (degress)')
    sat_col1.number_input('Transponder s max bandwidith (MHz)')


    sat_col2.number_input('Altitude (Km)')
    sat_col2.number_input('Effective bandwith (MHz)')

    
    sat_col3.number_input('Frequency (GHz)')
    sat_col3.number_input('Roll-off')

    sat_col4.number_input('EIRP (dBW)')
    sat_col4.selectbox('Modulation', ('64QAM', 'QPSK', '8PSK'))


st.subheader('Reception Characteristcs')
rcp_exp = st.expander(label='', expanded=True)
with rcp_exp:
    rcp_col1, rcp_col2, rcp_col3, rcp_col4 = st.columns(4)

    rcp_col1.number_input('Antenna Size (m)')
    rcp_col1.number_input('Antenna Efficiency')

    rcp_col2.number_input('LNB Gain (dB)')
    rcp_col2.number_input('LNB Noise Temp.(K)')

    rcp_col3.number_input('Cable Loss dB)')
    rcp_col3.number_input('Additional Losses (dB)')

    rcp_col4.number_input('Maximum depoing (degrees)')

run = st.button('Run calculations')

if run:
    c = st.container()
    with c:
        value = subprocess.check_output(['python', 'single_point_example.py'], shell=True, text=True)
        st.text(value)
        # print(str(value))
