from GrStat import GroundStation, Reception
from sat import Satellite
import numpy as np
import multiprocessing
import pandas as pd
import tqdm
import time


def point_ant_size(args):  # function loop - return the availability to a given Lat/Long
    min_ant_size = 0.5
    max_ant_size = 10
    step_ant_size = 0.2
    target_availability = 99.97

    point = args[0]
    sat = args[1]
    reception = args[2]
    lat = point['Lat']
    long = point['Long']
    station = GroundStation(lat, long)
    sat.set_grstation(station)
    sat.set_reception(reception)

    ant_size_vector = np.arange(min_ant_size, max_ant_size, step_ant_size)
    for ant_size in ant_size_vector:
        sat.reception.ant_size = ant_size
        # print(sat.get_availability())
        if sat.get_availability() >= target_availability:
            # print('ant_size ', ant_size)
            sat.reception.ant_size = ant_size - 0.1
            if sat.get_availability() >= target_availability:
                point['ant size'] = ant_size - 0.1
            else:
                point['ant size'] = ant_size
            break
    return point


if __name__ == '__main__':

    # reading the input table
    location = 'input examples\\'
    file = 'list'
    point_list = pd.read_csv(location + file + '.csv', sep=';', encoding='latin1')
    point_list['ant size'] = np.nan  # creating an empty results column

    # ground station parameters
    site_lat = -3.7  # [decimal degrees]
    site_long = -45.9  # [decimal degrees]
    station = GroundStation(site_lat, site_long)

    # satellite parameters
    sat_long = -70  # [decimal degrees]
    freq = 12  # [Ghz]
    eirp = 50 # [dBW]
    hsat = 35800  # satellite's height [km]
    tau = 90  # H=0, V = 90, circ = 45
    b_transponder = 36  # transponder bandwidth [MHz]
    b_util = 9  # effective used bandwidth [MHz]
    backoff = 0  # not used for now!
    contour = 0  # not used for now!
    rolloff = 0.2  # roll-off factor (raised cosine filter)
    mod = '8PSK'  # modulation (from modcod file)
    fec = '120/180'  # FEC (from modcod file)

    # creating the satellite object
    sat = Satellite(sat_long, freq, eirp, hsat, b_transponder, b_util, backoff, contour, mod, rolloff, fec)

    # reception parameters
    ant_size = 1.2  # reception antenna diameter [m]
    ant_eff = 0.6  # reception antenna efficiency
    coupling_loss = 0  # [dB]
    polarization_loss = 3  # [dB]
    lnb_gain = 55  # [dB]
    lnb_noise_temp = 20  # [dB]
    cable_loss = 4  # [dB]
    max_depoint = 0.1  # maximum depointing angle [degrees]

    # creating a reception object
    reception = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_noise_temp, cable_loss,
                          max_depoint)

    cores = multiprocessing.cpu_count() - 2

    p = multiprocessing.Pool(processes=cores)

    # calculation loop
    start_time = time.time()

    data = list(
        tqdm.tqdm(p.imap_unordered(point_ant_size, [(city, sat, reception) for index, city in point_list.iterrows()]),
                  total=len(point_list)))
    p.close()

    point_list.drop(point_list.index, inplace=True)
    point_list = point_list.append(data, ignore_index=True)

    print("--- %s seconds ---" % (time.time() - start_time))

    print(point_list)