from GrStat import GroundStation, Reception
from sat import Satellite
import sys, os
import pickle
import numpy as np
import time

# This function runs the atmospheric attenuation functions and prepare the interface outputs

def calc_atm_atnn():
    with open('temp/args.pkl', 'rb') as f:
        p, site_lat, site_long, ant_size, ant_eff, sat_long, freq, method = pickle.load(f)
        f.close()

    sys.stdout = open('temp/out.txt', 'w')  # creating a output file to show in the interface
    gr_station = GroundStation(site_lat, site_long)
    satellite = Satellite(sat_long, freq)
    reception = Reception(ant_size, ant_eff)

    satellite.set_grstation(gr_station)
    satellite.set_reception(reception)

    start = time.time()
    # running the atmospheric attenuation calculations and storing the results
    a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = satellite.get_link_attenuation(p, method)

    # preparing the outputs
    # ====== REMEMBER TO ADJUST TO 3 DECIMALS ALL OUTPUTS!!!!! =======
    print('RESULTS', file=sys.stdout)
    print('', file=sys.stdout)
    print('Reception characteristics:', file=sys.stdout)
    print('', file=sys.stdout)
    print('Earth\'s radius in lat/long: ', np.round(satellite.grstation.get_earth_radius(),3), ' km', file=sys.stdout)
    print('Elevation angle: ', np.round(satellite.get_elevation(), 3), ' degress', file=sys.stdout)
    print('Link length: ', np.round(satellite.get_distance(), 3), 'km', file=sys.stdout)
    print('Ground noise temperature: ', np.round(satellite.reception.get_ground_temp(), 3), ' K', file=sys.stdout)
    print('Sky brightness temperature', np.round(satellite.reception.get_brightness_temp(), 3), ' K', file=sys.stdout)
    print('', file=sys.stdout)
    print('', file=sys.stdout)

    print('Link budget Aaalysis:', file=sys.stdout)
    print('', file=sys.stdout)
    print("Gaseous attenuation: ", np.round(a_g, 3), file=sys.stdout)
    print("Cloud attenuation: ", np.round(a_c, 3), file=sys.stdout)
    print("Rain attenuation: ", np.round(a_r, 3), file=sys.stdout)
    print("Scintillation attenuation: ", np.round(a_s, 3), file=sys.stdout)
    print("Total atmospheric attenuation: ", np.round(a_t, 3), file=sys.stdout)
    print('Free space attenuation: ', np.round(a_fs, 3), file=sys.stdout)
    print('Free space + atmospheric + depointing attenuation: ', np.round(a_tot, 3), ' dB', file=sys.stdout)

    print('', file=sys.stdout)
    print('Runtime: ', np.round(time.time() - start, 2), ' s', file=sys.stdout)

    if os.path.exists('temp/args.pkl'):  # deleting the input variables temp file
        os.remove('temp/args.pkl')

    sys.stdout.close()

    return
