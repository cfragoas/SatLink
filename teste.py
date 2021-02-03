from GrStat import GroundStation, Reception
from sat import Satellite
import numpy as np
import time


# parâmetros da estacao terrena
site_lat = -3.7
site_long = -45.9
estacao = GroundStation(site_lat, site_long)

# parâmetros do satélite
sat_long = -70
ant_diam = 1.2
freq = 15
eirp = 54 #dBW
hsat = 35800
tau = 90  # H=0, V = 90, circ = 45
b_transponder = 36
b_util = 36
backoff = 0
satelite = Satellite(sat_long, freq, eirp, hsat,b_transponder, b_util, backoff)

satelite.set_grstation(estacao)  # setando a estacao terrena no satélite

# parâmetros do receptor
ant_size = 1.2  # diâmetro da antena receptora, em metros
ant_eff = 0.6  # eficiência da antena receptora
feeder_loss = 1  # perda do feeder, em dB
polarization_loss = 3  # perda de polarização, em dB
lnbf_noise_temp = 90  # temperatura de ruído do LNBF
feeder_noise_temp = 90  # temparatura de ruído do feeder
desfoc_max = 0.1

# criando o objeto receptor
receptor = Reception(ant_size, ant_eff, feeder_loss, polarization_loss, lnbf_noise_temp, feeder_noise_temp, desfoc_max)

satelite.set_reception(receptor)  # setando o receptor do link de satélite


print('aaaaa  ',satelite.get_reception_threshold())

print('raio da terra na lat/long: ', satelite.grstation.get_earth_radius())
print('ângulo de elevação: ', satelite.get_elevation())
print('distância do enlace: ', satelite.get_distance())
print('figura de mérito: ', satelite.reception.get_figure_of_merit())
print('temperatura de ruído do solo: ', satelite.reception.get_ground_temp())
print('temperatura de radiação do céu', satelite.reception.get_brightness_temp())
print('temperatura de ruído da antena: ', satelite.reception.get_antenna_noise_temp())
print('temperatura de ruído total: ', satelite.reception.get_total_noise_temp())
print('ganho da antena receptora: ', satelite.reception.get_antenna_gain())
print('ângulo de meia potência da antena receptora: ', satelite.reception.get_beamwidth())


hS = 0.447  # altura da estação terrena

x = satelite.get_link_attenuation()
# start = time.time()
# print(satelite.get_availability())
# print('tempo de execução: ', time.time() - start)


start = time.time()
p = 0.2
unavailabilities = np.arange(0.01, 5, 0.01)

# for p in unavailabilities:

a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = satelite.get_link_attenuation(p)
print("Atenuação por gases: ", a_g)
print("Atenuação por nuvens: ", a_c)
print("Atenuação por chuva: ", a_r)
print("Atenuação por cintilação: ", a_s)
print("Atenuação atmosférica total: ", a_t)
print('Atenuação espaço livre: ', a_fs)
print('Perda por desfocalização: ', a_dep)
print('Atenuação atm + espaço livre: ', a_tot)
print('C/N: ', satelite.get_c_over_n0(p))
print('SNR: ', satelite.get_snr(p))

print('tempo de execução: ', time.time() - start)
