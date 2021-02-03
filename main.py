import pandas as pd
import numpy as np
from sat import Satellite
from GrStat import GroundStation, Reception
import multiprocessing
import tqdm
import os
import datetime


def point_availability(args):
    city = args[0]
    sat = args[1]
    reception = args[2]
    # print(city)
    lat = city['Lat']
    long = city['Long']
    station = GroundStation(lat, long)
    sat.set_grstation(station)
    sat.set_reception(reception)
    city['availability'] = sat.get_availability()
    return city


if __name__ == '__main__':

    # reading the input table
    dir = 'models\\'
    file = 'CitiesBrazil'
    cities = pd.read_csv(dir + file + '.csv', sep=';', encoding='latin1')
    cities['availability'] = np.nan  # creating an empty results column

    ##############################
    ### parâmetros do satélite ###
    ##############################

    sat_long = -70
    freq = 18  # gigaherz
    eirp = 54  # dBW
    hsat = 35800  # altura do satélite, em km
    tau = 90  # H=0, V = 90, circ = 45
    b_transponder = 9  # banda do transponder, em MHz
    b_util = 9  # banda utilizada do transpoder, em MHz
    backoff = 0  # MHz
    contorno = 0  # não sei o que é isso
    mod = '8PSK'  # modulação
    fec = '120/180'  # FEC
    rolloff = 0.2

    # criando o objeto satélite
    sat = Satellite(sat_long, freq, eirp, hsat, b_transponder, b_util, backoff, contorno, mod, rolloff, fec)

    ##############################
    ### parâmetros da recepção ###
    ##############################
    ant_size = 1.2  # diâmetro da antena receptora, em metros
    ant_eff = 0.6  # eficiência da antena receptora
    coupling_loss = 0  # perda de acoplamento, em dB
    polarization_loss = 3  # perda de polarização, em dB
    lnb_gain = 55
    lnb_noise_temp = 20  # temperatura de ruído do LNBF
    cable_loss = 4  # temparatura de ruído do feeder
    desfoc_max = 0.1  # ângulo de desfocalização máximo, em graus

    # criando o objeto receptor
    reception = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_noise_temp, cable_loss,
                          desfoc_max)

    cores = multiprocessing.cpu_count() - 2

    p = multiprocessing.Pool(processes=cores)

    #TESTE PRINTANDO A SAÍDA ========================
    # import sys

    # sys.stderr = open('temp\\out.txt', 'w')


    #=====================================================

    # print('initializing . . .', file=sys.stderr)

    data = list(
        tqdm.tqdm(p.imap_unordered(point_availability, [(city, sat, reception) for index, city in cities.iterrows()]),
                  total=len(cities)))
    p.close()

    cities.drop(cities.index, inplace=True)
    cities = cities.append(data, ignore_index=True)
    cities['availability time'] = round(((100 - cities['availability'])/100) * 525600, 0)  # calculating the availability in seconds
    # import itur
    # cities['height'] = itur.topographic_altitude(cities['Lat'], cities['Long'])

    # saving the results into a csv file

    dir = 'results'
    if not os.path.exists(dir):
        os.makedirs(dir)

    cities.to_csv(dir + '\\' + 'results ' + datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S') + '.csv', sep=';',
                  encoding='latin1')

    # print('Complete!!!', file=sys.stderr)

    # sys.stderr.close()
