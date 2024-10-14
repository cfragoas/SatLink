from GrStat import GroundStation, Reception
from sat import Satellite
from pathos.pools import ParallelPool
import pandas as pd
import numpy as np
import pickle
import tqdm
import time
import datetime
import sys, os, platform

# this file contains the functions used to calculate availability and display the results in the interface


# STILL NEED TO CREATE A HEADER IN THE CSV OUTPUT (mp_link_performance)


def point_availability(args): # this function is just to run the availability for multiple points in mp_link_performance's pool
    point = args[0]
    sat = args[1]
    reception = args[2]
    margin = args[3]
    snr_relaxation = args[4]
    lat = point['Lat']
    long = point['Long']
    station = GroundStation(lat, long)
    sat.set_grstation(station)
    sat.set_reception(reception)
    point['availability'] = sat.get_availability(margin, snr_relaxation)
    return point


def sp_link_performance():  # this function runs the availability for a single point and shows a complete output
    path = 'temp/args.pkl'
    with open(path, 'rb') as f:
        (site_lat, site_long, sat_long, freq, max_eirp, sat_height, max_bw, bw_util, modcod, pol,
         roll_off, ant_size, ant_eff, lnb_gain, lnb_temp, coupling_loss, cable_loss, max_depoint,
         snr_relaxation, margin) = pickle.load(f)
        f.close()

    #####################################
    ##### ground station parameters #####
    #####################################

    # creating a ground station object
    station = GroundStation(site_lat, site_long)

    ##############################
    ### satellite parameters ###
    ##############################

    path = 'models/Modulation_dB.csv'
    data = pd.read_csv(path, sep=';')
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
    reception = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_temp, cable_loss,
                          max_depoint)

    # atribuindo uma recepção à um enlace de satélite
    satelite.set_reception(reception)  # setando o receptor do link de satélite

    ###################################
    #########     OUTPUTS     #########
    ###################################

    ############ SNR target's calcullation ################
    path = 'temp/out.txt'
    sys.stdout = open(path, 'w')

    start = time.time()
    print('RESULTS', file=sys.stdout)
    print('', file=sys.stdout)
    print('Link budget at 0.001%:', file=sys.stdout)
    print('', file=sys.stdout)
    print('C/N0: ', satelite.get_c_over_n0(0.001), ' dB')
    print('SNR: ', satelite.get_snr(0.001), ' dB')
    print('', file=sys.stdout)
    print('', file=sys.stdout)

    print('Actual SNR target\'s availability: ', satelite.get_availability(margin, snr_relaxation), '%',
          file=sys.stdout)
    print('', file=sys.stdout)

    print('Reception characteristics:', file=sys.stdout)
    print('', file=sys.stdout)

    print('Earth\'s radius in lat/long: ', np.round(satelite.grstation.get_earth_radius(), 3), ' km', file=sys.stdout)
    print('Elevation angle: ', np.round(satelite.get_elevation(), 3), ' degrees', file=sys.stdout)
    print('Link length: ', np.round(satelite.get_distance(), 3), 'km', file=sys.stdout)
    print('Ground noise temperature: ', np.round(satelite.reception.get_ground_temp(), 3), ' K', file=sys.stdout)
    print('Sky brightness temperature', np.round(satelite.reception.get_brightness_temp(), 3), ' K', file=sys.stdout)
    print('Antenna noise temperature: ', np.round(satelite.reception.get_antenna_noise_temp(), 3), ' K', file=sys.stdout)
    print('Antenna noise temperature w/ rain:', np.round(satelite.get_antenna_noise_rain(), 3), ' K', file=sys.stdout)
    print('Total noise temperature: ', np.round(satelite.get_total_noise_temp(), 3), ' K', file=sys.stdout)
    print('Reception antenna gain: ', np.round(satelite.reception.get_antenna_gain(), 3), ' dBi', file=sys.stdout)
    print('Reception antenna 3dB beamwidth: ', np.round(satelite.reception.get_beamwidth(), 3), ' degrees', file=sys.stdout)
    print('Figure of Merit: ', np.round(satelite.get_figure_of_merit(), 3), file=sys.stdout)
    print('', file=sys.stdout)
    print('', file=sys.stdout)

    a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = satelite.get_link_attenuation(satelite.p)

    print('Link budget Analysis:', file=sys.stdout)
    print('', file=sys.stdout)

    print("Gaseous attenuation: ", np.round(a_g, 3), file=sys.stdout)
    print("Cloud attenuation: ", np.round(a_c, 3), file=sys.stdout)
    print("Rain attenuation: ", np.round(a_r, 3), file=sys.stdout)
    print("Scintillation attenuation: ", np.round(a_s, 3), file=sys.stdout)
    print("Total atmospheric attenuation: ", np.round(a_t, 3), file=sys.stdout)
    print('Free space attenuation: ', np.round(a_fs, 3), file=sys.stdout)
    print('Free space + atmospheric + depointing attenuation: ', np.round(a_tot, 3), ' dB', file=sys.stdout)

    print('Reception threshold (SNR): ', np.round(satelite.get_reception_threshold(), 3), ' dB', file=sys.stdout)

    print('', file=sys.stdout)
    print('Runtime: ', np.round(time.time() - start, 2), ' s', file=sys.stdout)

    sys.stdout.close()

    path = 'temp/args.pkl'

    if os.path.exists(path):
        os.remove(path)

    return


def mp_link_performance():
    path = 'temp/args.pkl'
    with open(path, 'rb') as f:  # opening the input variables in the temp file
        (gr_station_path, sat_long, freq, max_eirp, sat_height, max_bw, bw_util, modcod, pol,
         roll_off, ant_size, ant_eff, lnb_gain, lnb_temp, coupling_loss, cable_loss, max_depoint,
         snr_relaxation, margin, threads) = pickle.load(f)
        f.close()

    # reading the input table
    # dir = 'models/'
    # file = 'CitiesBrazil'
    # cities = pd.read_csv(dir + file + '.csv', sep=';', encoding='latin1')
    # cities['availability'] = np.nan  # creating an empty results column

    point_list = pd.read_csv(gr_station_path, sep=';', encoding='latin1')  # creating a point dataframe from csv file
    point_list['availability'] = np.nan  # creating an empty results column

    path = 'models/Modulation_dB.csv'
    data = pd.read_csv(path, sep=';')
    line = data.loc[(data.Modcod) == modcod]
    # tech = line['Tech'].values[0]
    mod = line['Modulation'].values[0]
    fec = line['FEC'].values[0]

    # creating the satellite object
    sat = Satellite(sat_long, freq, max_eirp, sat_height, max_bw, bw_util, 0, 0, mod, roll_off, fec)

    polarization_loss = 3

    reception = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_temp, cable_loss,
                          max_depoint)  # creating the receptor object

    # ======================== PARALLEL POOL =============================
    pool = ParallelPool(nodes=threads)  # creating the parallelPoll

    path = 'temp/out.txt'
    sys.stderr = open(path, 'w')  # to print the output dynamically

    print('initializing . . .', file=sys.stderr)

    # running the parallel pool
    data = list(
        tqdm.tqdm(pool.imap(point_availability,
                            [(point, sat, reception, margin, snr_relaxation) for index, point in point_list.iterrows()]),
                  total=len(point_list)))
    pool.clear()

    point_list.drop(point_list.index, inplace=True)
    point_list = point_list.append(data, ignore_index=True)
    point_list['unavailability time (min)'] = round(((100 - point_list['availability']) / 100) * 525600,
                                            0)  # calculating the availability in minutes

    # saving the results into a csv file

    dir = 'results'
    if not os.path.exists(dir):
        os.makedirs(dir)

    path = convert_path_os(dir + '/' + 'results ' + datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S') + '.csv')
    point_list.to_csv(path, sep=';',
                      encoding='latin1')

    print('Complete!!!', file=sys.stderr)

    sys.stderr.close()

    return
