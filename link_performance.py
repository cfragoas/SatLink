from GrStat import GroundStation, Reception
from sat import Satellite
from pathos.pools import ParallelPool
import pandas as pd
import numpy as np
import pickle
import tqdm
import time
import datetime
import sys, os


def point_availability(args):
    city = args[0]
    sat = args[1]
    reception = args[2]
    margin = args[3]
    snr_relaxation = args[4]
    lat = city['Lat']
    long = city['Long']
    station = GroundStation(lat, long)
    sat.set_grstation(station)
    sat.set_reception(reception)
    city['availability'] = sat.get_availability(margin, snr_relaxation)
    return city

def sp_link_performance():

    with open('temp\\args.pkl', 'rb') as f:
        (site_lat, site_long, sat_long, freq, max_eirp, sat_height, max_bw, bw_util, modcod, pol,
         roll_off, ant_size, ant_eff, lnb_gain, lnb_temp, coupling_loss, cable_loss, max_depoint,
         snr_relaxation, margin) = pickle.load(f)
        f.close()

    #####################################
    ##### ground station parameters #####
    #####################################

    #creating a ground station object
    station = GroundStation(site_lat, site_long)

    ##############################
    ### satellite parameters ###
    ##############################

    data = pd.read_csv('models\\Modulation_dB.csv', sep=';')
    line = data.loc[(data.Modcod) == modcod]
    # tech = line['Tech'].values[0]
    mod = line['Modulation'].values[0]
    fec = line['FEC'].values[0]


    # criando o objeto satélite
    satelite = Satellite(sat_long, freq, max_eirp, sat_height, max_bw, bw_util, 0, 0, mod, roll_off, fec)

    # atribuindo uma estação terrena à um satélite
    satelite.set_grstation(station)

    ##############################
    ### reception parametters ####
    ##############################

    polarization_loss = 3  # perda de polarização, em dB

    # criando o objeto receptor
    reception = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_temp, cable_loss, max_depoint)

    #atribuindo uma recepção à um enlace de satélite
    satelite.set_reception(reception)  # setando o receptor do link de satélite

    ###################################
    #########     OUTPUTS     #########
    ###################################

    ############ SNR target's calcullation ################

    sys.stdout = open('temp\\out.txt', 'w')

    start = time.time()
    print('RESULTS', file=sys.stdout)
    print('', file=sys.stdout)
    print('Link budget at 0.001%:', file=sys.stdout)
    print('', file=sys.stdout)
    print('C/N0: ', satelite.get_c_over_n0(0.001), ' dB')
    print('SNR: ', satelite.get_snr(0.001), ' dB')
    print('', file=sys.stdout)
    print('', file=sys.stdout)

    print('Actual SNR target\'s availability: ', satelite.get_availability(margin, snr_relaxation), '%', file=sys.stdout)
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

    a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = satelite.get_link_attenuation(satelite.p)

    print('Link budget Analysis:', file=sys.stdout)
    print('', file=sys.stdout)

    print("Gaseous attenuation: ", a_g, ' dB', file=sys.stdout)
    print("Cloud attenuation: ", a_c, ' dB', file=sys.stdout)
    print("Rain attenuation: ", a_r, ' dB', file=sys.stdout)
    print("Scintillation attenuation: ", a_s, ' dB', file=sys.stdout)
    print("Total atmospheric attenuation: ", a_t, ' dB', file=sys.stdout)
    print('Free space attenuation: ', a_fs, ' dB', file=sys.stdout)
    print('Free space + atmospheric + depointing attenuation: ', a_tot, ' dB', file=sys.stdout)

    print('Reception threshold (SNR): ', satelite.get_reception_threshold(), ' dB', file=sys.stdout)

    print('', file=sys.stdout)
    print('Runtime: ', time.time() - start, ' s', file=sys.stdout)



    if os.path.exists('temp\\args.pkl'):
        os.remove('temp\\args.pkl')

    sys.stdout.close()

def mp_link_performance():

    with open('temp\\args.pkl', 'rb') as f:
        (gr_station_path, sat_long, freq, max_eirp, sat_height, max_bw, bw_util, modcod, pol,
         roll_off, ant_size, ant_eff, lnb_gain, lnb_temp, coupling_loss, cable_loss, max_depoint,
         snr_relaxation, margin, threads) = pickle.load(f)
        f.close()

    # reading the input table
    dir = 'models\\'
    file = 'CitiesBrazil'
    cities = pd.read_csv(dir + file + '.csv', sep=';', encoding='latin1')
    cities['availability'] = np.nan  # creating an empty results column

    # creating the satellite object

    data = pd.read_csv('models\\Modulation_dB.csv', sep=';')
    line = data.loc[(data.Modcod) == modcod]
    # tech = line['Tech'].values[0]
    mod = line['Modulation'].values[0]
    fec = line['FEC'].values[0]

    sat = Satellite(sat_long, freq, max_eirp, sat_height, max_bw, bw_util, 0, 0, mod, roll_off, fec)

    # creating the receptor object

    polarization_loss = 3

    reception = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_temp, cable_loss,
                          max_depoint)

    pool = ParallelPool(nodes=threads)


    # to print the output dynamically

    sys.stderr = open('temp\\out.txt', 'w')

    # =====================================================

    print('initializing . . .', file=sys.stderr)


    data = list(
        tqdm.tqdm(pool.imap(point_availability, [(city, sat, reception, margin, snr_relaxation) for index, city in cities.iterrows()]),
                  total=len(cities)))
    pool.close()

    cities.drop(cities.index, inplace=True)
    cities = cities.append(data, ignore_index=True)
    cities['availability time'] = round(((100 - cities['availability']) / 100) * 525600,
                                        0)  # calculating the availability in seconds

    # saving the results into a csv file

    dir = 'results'
    if not os.path.exists(dir):
        os.makedirs(dir)

    cities.to_csv(dir + '\\' + 'results ' + datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S') + '.csv', sep=';',
                  encoding='latin1')

    print('Complete!!!', file=sys.stderr)

    sys.stderr.close()

    return




