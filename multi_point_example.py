import pandas as pd
import numpy as np
from sat import Satellite
from GrStat import GroundStation, Reception
import multiprocessing
import tqdm
import os
import datetime

# this is a code example and very good approximation of the multi-point calculation used in link_performance.py


def point_availability(args):  # function loop - return the availability to a given Lat/Long
    point = args[0]
    sat = args[1]
    reception = args[2]
    lat = point['Lat']
    long = point['Long']
    station = GroundStation(lat, long)
    sat.set_grstation(station)
    sat.set_reception(reception)
    point['availability'] = sat.get_availability()
    return point


if __name__ == '__main__':

    # reading the input table
    location = 'input examples\\'
    file = 'list'
    point_list = pd.read_csv(location + file + '.csv', sep=';', encoding='latin1')
    point_list['availability'] = np.nan  # creating an empty results column

    ##############################
    ### satellite parameters ###
    ##############################

    sat_long = -70  # [decimal degrees]
    freq = 18  # [Ghz]
    eirp = 54  # [dBW]
    hsat = 35800  # satellite's height [km]
    tau = 90  # H=0, V = 90, circ = 45
    b_transponder = 36  # transponder bandwidth [MHz]
    b_util = 9  # effective used bandwidth [MHz]
    backoff = 0  # not used for now!
    contour = 0  # not used for now!
    mod = '8PSK'  # modulation (from modcod file)
    fec = '120/180'  # FEC (from modcod file)
    rolloff = 0.2  # roll-off factor (raised cosine filter)

    # creating the satellite object
    sat = Satellite(sat_long, freq, eirp, hsat, b_transponder, b_util, backoff, contour, mod, rolloff, fec)

    ##############################
    ### reception parameters ###
    ##############################
    ant_size = 1.2  # reception antenna diameter [m]
    ant_eff = 0.6  # reception antenna efficiency
    coupling_loss = 0  # [dB]
    polarization_loss = 3  # [dB]
    lnb_gain = 55  # [dB]
    lnb_noise_temp = 20  # temperatura de ruído do LNBF
    cable_loss = 4  # [dB]
    max_depoint = 0.1  # maximum depointing angle [degrees]

    # creating a reception object
    reception = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_noise_temp, cable_loss,
                          max_depoint)

    cores = multiprocessing.cpu_count() - 2

    p = multiprocessing.Pool(processes=cores)

    # calculation loop

    data = list(
        tqdm.tqdm(p.imap_unordered(point_availability, [(city, sat, reception) for index, city in point_list.iterrows()]),
                  total=len(point_list)))
    p.close()

    point_list.drop(point_list.index, inplace=True)
    point_list = point_list.append(data, ignore_index=True)
    point_list['unavailability time'] = round(((100 - point_list['availability'])/100) * 525600, 0)  # calculating the unavailability in minutes


    # saving the results into a csv file

    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)

    point_list.to_csv(path + '\\' + 'results ' + datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S') + '.csv', sep=';',
                  encoding='latin1')

    print('Complete!!!')

