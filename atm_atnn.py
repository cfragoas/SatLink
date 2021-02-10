from GrStat import GroundStation, Reception
from sat import Satellite
import sys, os
import pickle

# This function runs the atmospheric attenuation functions and prepare the interface outputs

def calc_atm_atnn():
    with open('temp\\args.pkl', 'rb') as f:
        p, site_lat, site_long, ant_size, ant_eff, sat_long, freq, method = pickle.load(f)
        f.close()

    sys.stdout = open('temp\\out.txt', 'w')  # creating a output file to show in the interface
    gr_station = GroundStation(site_lat, site_long)
    satellite = Satellite(sat_long, freq)
    reception = Reception(ant_size, ant_eff)

    satellite.set_grstation(gr_station)
    satellite.set_reception(reception)

    # running the atmospheric attenuation calculations and storing the results
    a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = satellite.get_link_attenuation(p, method)

    # preparing the outputs
    # ====== REMEMBER TO ADJUST TO 3 DECIMALS ALL OUTPUTS!!!!! =======
    print('RESULTS', file=sys.stdout)
    print('', file=sys.stdout)
    print('Reception characteristics:', file=sys.stdout)
    print('', file=sys.stdout)
    print('Earth\'s radius in lat/long: ', satellite.grstation.get_earth_radius(), ' km', file=sys.stdout)
    print('Elevation angle: ', satellite.get_elevation(), ' graus', file=sys.stdout)
    print('Link length: ', satellite.get_distance(), 'km', file=sys.stdout)
    print('Ground noise temperature: ', satellite.reception.get_ground_temp(), ' K', file=sys.stdout)
    print('Sky brightness temperature', satellite.reception.get_brightness_temp(), ' K', file=sys.stdout)
    print('Antenna noise temperature: ', satellite.reception.get_antenna_noise_temp(), ' K', file=sys.stdout)
    print('Antenna noise temperature w/ rain:', satellite.get_antenna_noise_rain(), ' K', file=sys.stdout)
    print('Total noise temperature: ', satellite.get_total_noise_temp(), ' K', file=sys.stdout)
    print('Reception antenna gain: ', satellite.reception.get_antenna_gain(), ' dBi', file=sys.stdout)
    print('Reception antenna 3dB beamwidth: ', satellite.reception.get_beamwidth(), ' degrees', file=sys.stdout)
    print('Figure of Merit: ', satellite.get_figure_of_merit(), file=sys.stdout)
    print('', file=sys.stdout)
    print('', file=sys.stdout)

    print('Link budget Aaalysis:', file=sys.stdout)
    print('', file=sys.stdout)
    print("Gaseous attenuation: ", a_g, ' dB', file=sys.stdout)
    print("Cloud attenuation: ", a_c, ' dB', file=sys.stdout)
    print("Rain attenuation: ", a_r, ' dB', file=sys.stdout)
    print("Scintillation attenuation: ", a_s, ' dB', file=sys.stdout)
    print("Total atmospheric attenuation: ", a_t, ' dB', file=sys.stdout)
    print('Free space attenuation: ', a_fs, ' dB', file=sys.stdout)
    print('Free space + atmospheric + depointing attenuation: ', a_tot, ' dB', file=sys.stdout)

    if os.path.exists('temp\\args.pkl'):  # deleting the input variables temp file
        os.remove('temp\\args.pkl')

    sys.stdout.close()

    return
