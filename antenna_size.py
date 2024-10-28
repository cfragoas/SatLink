from GrStat import GroundStation, Reception
from sat import Satellite
from pathos.pools import ParallelPool
from scipy import interpolate
import pandas as pd
import numpy as np
import pickle
import tqdm
import datetime
import sys, os


# this file contains the functions used to estimate antenna sizes and display the results in the interface


# STILL NEED TO CREATE A HEADER IN THE CSV OUTPUT (mp_mp_ant_size)

def loop_graph_ant_size(args):
    sat, margin, snr_relaxation, ant_size = args
    sat.reception.ant_size = round(ant_size, 1)
    availability = sat.get_availability(margin, snr_relaxation)
    return availability

def point_ant_size(args):  # function loop - return the availability to a given Lat/Long
    min_ant_size = 0.5
    max_ant_size = 10
    step_ant_size = 0.2

    point, sat, reception, margin, snr_relaxation, target_availability, idx = args

    station = GroundStation(point['Lat'], point['Long'])
    sat.set_grstation(station)
    sat.set_reception(reception)

    ant_size_vector = np.arange(min_ant_size, max_ant_size, step_ant_size)
    for ant_size in ant_size_vector:
        sat.reception.ant_size = round(ant_size, 1)
        if sat.get_availability(margin, snr_relaxation) >= target_availability:
            sat.reception.ant_size = round(round(ant_size, 1) - 0.1, 1)
            if sat.get_availability(margin, snr_relaxation) >= target_availability:
                ant_size = round(round(ant_size, 1) - 0.1, 1)
            else:
                ant_size = round(ant_size, 1)
            break
    return (idx, ant_size)


def sp_ant_size():  # this function runs the availability for a single point and shows a complete output
    with open('temp/args.pkl', 'rb') as f:
        (site_lat, site_long, sat_long, freq, max_eirp, sat_height, max_bw, bw_util,
         modcod, pol, roll_off, ant_eff, lnb_gain, lnb_temp, aditional_losses,
         cable_loss, max_depoint, max_ant_size, min_ant_size, margin, cores) = pickle.load(f)
        f.close()

    #####################################
    ##### ground station parameters #####
    #####################################

    # creating a ground station object
    station = GroundStation(site_lat, site_long)

    ##############################
    ### satellite parameters ###
    ##############################

    data = pd.read_csv('models/Modulation_dB.csv', sep=';')
    line = data.loc[(data.Modcod) == modcod]
    # tech = line['Tech'].values[0]
    mod = line['Modulation'].values[0]
    fec = line['FEC'].values[0]

    # criando o objeto satélite
    satellite = Satellite(sat_long, freq, max_eirp, sat_height, max_bw, bw_util, 0, 0, mod, roll_off, fec)

    # atribuindo uma estação terrena à um satélite
    satellite.set_grstation(station)

    ##############################
    ### reception parametters ####
    ##############################

    polarization_loss = 3  # perda de polarização, em dB

    # criando o objeto receptor
    reception = Reception(None, ant_eff, aditional_losses, polarization_loss, lnb_gain, lnb_temp, cable_loss,
                          max_depoint)

    # atribuindo uma recepção à um enlace de satélite
    satellite.set_reception(reception)  # setando o receptor do link de satélite

    ###################################
    #########     OUTPUTS     #########
    ###################################

    ############ SNR target's calcullation ################

    step = 0.2
    interp_step = int(round((max_ant_size - min_ant_size) * 100))
    ant_size_vector = np.arange(min_ant_size, max_ant_size, step)
    ant_size_vector_interp = np.linspace(min_ant_size, max_ant_size, interp_step)

    # parallel loop for each antenna size
    pool = ParallelPool(nodes=round(cores/2))    #ARRUMAR AQUI
    availability_vector = list(pool.imap(loop_graph_ant_size, [(satellite, margin, 1, ant_size) for ant_size in ant_size_vector]))
    pool.clear()

    ant_size_vector = np.array(ant_size_vector)
    availability_vector = np.array(availability_vector)
    ant_size_vector = ant_size_vector[availability_vector > 60]
    availability_vector = availability_vector[availability_vector > 60]

    # a_BSpline = interpolate.make_interp_spline(ant_size_vector, availability_vector, k=2)
    # availability_vector_interp = a_BSpline(ant_size_vector_interp)

    availability_vector_interp = 0
    with open('temp/args.pkl', 'wb') as f:
        pickle.dump(
            [ant_size_vector, ant_size_vector_interp, availability_vector, availability_vector_interp], f)
        f.close()

    return


def mp_ant_size():
    with open('temp/args.pkl', 'rb') as f:  # opening the input variables in the temp file
        (gr_station_path, sat_long, freq, max_eirp, sat_height, max_bw, bw_util,
         modcod, pol, roll_off, ant_eff, lnb_gain, lnb_temp, aditional_losses,
         cable_loss, max_depoint, availability_target, snr_relaxation, margin, threads) = pickle.load(f)
        f.close()

    # reading the input table
    # dir = 'models/'
    # file = 'CitiesBrazil'
    # cities = pd.read_csv(dir + file + '.csv', sep=';', encoding='latin1')
    # cities['availability'] = np.nan  # creating an empty results column

    point_list = pd.read_csv(gr_station_path, sep=';', encoding='latin1')  # creating a point dataframe from csv file

    data = pd.read_csv('models/Modulation_dB.csv', sep=';')
    line = data.loc[data.Modcod == modcod]
    # tech = line['Tech'].values[0]
    mod = line['Modulation'].values[0]
    fec = line['FEC'].values[0]

    # creating the satellite object
    sat = Satellite(sat_long, freq, max_eirp, sat_height, max_bw, bw_util, 0, 0, mod, roll_off, fec)

    polarization_loss = 3

    reception = Reception(None, ant_eff, aditional_losses, polarization_loss, lnb_gain, lnb_temp, cable_loss,
                          max_depoint)  # creating the receptor object

    # ======================== PARALLEL POOL =============================

    pool = ParallelPool(nodes=threads)  # creating the parallelPoll

    sys.stderr = open('temp/out.txt', 'w')  # to print the output dynamically

    print('initializing . . .', file=sys.stderr)

    # running the parallel pool
    data = list(
        tqdm.tqdm(pool.imap(point_ant_size, [(point, sat, reception, margin, snr_relaxation, availability_target, index) 
                                             for index, point in point_list.iterrows()]), total=len(point_list)))
    pool.clear()

    point_list['ant size'] = np.array(sorted(data, key=lambda x: x[0]))[:,1]

    # saving the results into a csv file

    dir = 'results'
    if not os.path.exists(dir):
        os.makedirs(dir)

    point_list.to_csv(dir + '/' + 'results_ant ' + datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S') + '.csv', sep=';',
                      encoding='latin1')

    print('Complete!!!', file=sys.stderr)

    sys.stderr.close()

    return
