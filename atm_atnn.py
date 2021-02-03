from GrStat import GroundStation, Reception
from sat import Satellite
import sys, os
import pickle



def calc_atm_atnn():
    with open('temp\\args.pkl', 'rb') as f:
        p, site_lat, site_long, ant_size, ant_eff, sat_long, freq = pickle.load(f)
        f.close()

    sys.stdout = open('temp\\out.txt', 'w')
    estacao = GroundStation(site_lat, site_long)
    satelite = Satellite(sat_long, freq)
    receptor = Reception(ant_size, ant_eff)

    satelite.set_grstation(estacao)
    satelite.set_reception(receptor)

    a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = satelite.get_link_attenuation(p)

    print('RESULTS', file=sys.stdout)
    print('', file=sys.stdout)
    print('Reception characteristics:', file=sys.stdout)
    print('', file=sys.stdout)
    print('Earth\'s radius in lat/long: ', satelite.grstation.get_earth_radius(), ' km', file=sys.stdout)
    print('Elevation angle: ', satelite.get_elevation(), ' graus', file=sys.stdout)
    print('Link length: ', satelite.get_distance(), 'km', file=sys.stdout)
    print('Ground noise temperature: ', satelite.reception.get_ground_temp(), ' K', file=sys.stdout)
    print('Sky brightness temperature', satelite.reception.get_brightness_temp(), ' K', file=sys.stdout)
    print('Antenna noise temperature: ', satelite.reception.get_antenna_noise_temp(), ' K', file=sys.stdout)
    print('Antenna noise temperature w/ rain:', satelite.get_antenna_noise_rain(), ' K', file=sys.stdout)
    print('Total noise temperature: ', satelite.get_total_noise_temp(), ' K', file=sys.stdout)
    print('Reception antenna gain: ', satelite.reception.get_antenna_gain(), ' dBi', file=sys.stdout)
    print('Reception antenna 3dB beamwidth: ', satelite.reception.get_beamwidth(), ' degrees', file=sys.stdout)
    print('Figure of Merit: ', satelite.get_figure_of_merit(), file=sys.stdout)
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

    if os.path.exists('temp\\args.pkl'):
        os.remove('temp\\args.pkl')

    sys.stdout.close()