from GrStat import GroundStation, Reception
from sat import Satellite
import numpy as np
import time

#####################################
### parâmetros da estacao terrena ###
#####################################

site_lat = -22.95
site_long = -43.2

#criando um objeto estação
estacao = GroundStation(site_lat, site_long)

##############################
### parâmetros do satélite ###
##############################

sat_long = -70
freq = 12  # gigaherz
eirp_max = 54  # dBW
hsat = 35800  # altura do satélite, em metros
tau = 90  # H=0, V = 90, circ = 45
b_transponder = 9  # banda do transponder, em MHz
b_util = 9  # banda utilizada do transpoder, em MHz
backoff = 0  # MHz
contorno = 0  # não sei o que é isso
# tech = 'DVB-S2x'  # tecnologia utilizada
mod = '8PSK'  # modulação
fec = '100/180'  # FEC
rolloff = 0.2

# criando o objeto satélite
satelite = Satellite(sat_long, freq, eirp_max, hsat, b_transponder, b_util, backoff, contorno, mod, rolloff, fec)
satelite.p = 0.3

# atribuindo uma estação terrena à um satélite
satelite.set_grstation(estacao)

##############################
### parâmetros da recepção ###
##############################
ant_size = 0.9  # diâmetro da antena receptora, em metros
ant_eff = 0.6  # eficiência da antena receptora
coupling_loss = 0.5
cable_loss = 3  # perda do feeder, em dB
polarization_loss = 3 # perda de polarização, em dB (3)
lnb_noise_temp = 17  # temperatura de ruído do LNBF
lnb_gain = 50  # temparatura de ruído do feeder
desfoc_max = 0.1  # ângulo de desfocalização máximo, em graus

# criando o objeto receptor
receptor = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_noise_temp, cable_loss, desfoc_max)

#atribuindo uma recepção à um enlace de satélite
satelite.set_reception(receptor)  # setando o receptor do link de satélite




###################################
#########     OUTPUTS     #########
###################################


########### calculo para um dado p #############
# start = time.time()
#
# p = 0.02  # probabilidade da chuva exceder a probabilidade p
#
# a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = satelite.get_link_attenuation(p)
#
# print('raio da terra na lat/long: ', satelite.grstation.get_earth_radius(), ' km')
# print('ângulo de elevação: ', satelite.get_elevation(), ' graus')
# print('distância do enlace: ', satelite.get_distance(), 'km')
# print('figura de mérito: ', satelite.reception.get_figure_of_merit())
# print('temperatura de ruído do solo: ', satelite.reception.get_ground_temp(), ' K')
# print('temperatura de radiação do céu', satelite.reception.get_brightness_temp(), ' K')
# print('temperatura de ruído da antena: ', satelite.reception.get_antenna_noise_temp(), ' K')
# print('temperatura de ruído total: ', satelite.reception.get_total_noise_temp(), ' K')
# print('ganho da antena receptora: ', satelite.reception.get_antenna_gain(), ' dBi')
# print('ângulo de meia potência da antena receptora: ', satelite.reception.get_beamwidth(), ' graus')
#
# print("Atenuação por gases: ", a_g, ' dB')
# print("Atenuação por nuvens: ", a_c, ' dB')
# print("Atenuação por chuva: ", a_r, ' dB')
# print("Atenuação por cintilação: ", a_s, ' dB')
# print("Atenuação atmosférica total: ", a_t, ' dB')
# print('Atenuação espaço livre: ', a_fs, ' dB')
# print('Perda por desfocalização: ', a_dep, ' dB')
# print('Atenuação atm + espaço livre: ', a_tot, ' dB')
# print('limiar de recepção (SNR): ', satelite.get_reception_threshold(), ' dB')
# print('bitrate: ', satelite.get_bitrate(), ' bps')
# print('symbolrate: ', satelite.get_symbol_rate(), 'kSps')
# print('C/N0: ', satelite.get_c_over_n0(p), ' dB')
# print('SNR: ', satelite.get_snr(p), ' dB')
#
# print('tempo de execução: ', time.time() - start)
#
# print('')
# print('')

############ calculo para uma meta de SNR ################

start = time.time()
# print('Disponibilidade para a meta de SNR: ', satelite.get_availability(), '%')

print('raio da terra na lat/long: ', satelite.grstation.get_earth_radius(), ' km')
print('ângulo de elevação: ', satelite.get_elevation(), ' graus')
print('distância do enlace: ', satelite.get_distance(), 'km')
print('ganho da antena receptora: ', satelite.reception.get_antenna_gain(), ' dBi')
print('ângulo de meia potência da antena receptora: ', satelite.reception.get_beamwidth(), ' graus')

a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = satelite.get_link_attenuation(satelite.p)

print("Atenuação por gases: ", a_g, ' dB')
print("Atenuação por nuvens: ", a_c, ' dB')
print("Atenuação por chuva: ", a_r, ' dB')
print("Atenuação por cintilação: ", a_s, ' dB')
print("Atenuação atmosférica total: ", a_t, ' dB')
print('Atenuação espaço livre: ', a_fs, ' dB')
print('Perda por desfocalização: ', a_dep, ' dB')
print('Atenuação atm + espaço livre: ', a_tot, ' dB')

print('temperatura de ruído do solo: ', satelite.reception.get_ground_temp(), ' K')
print('temperatura de radiação do céu', satelite.reception.get_brightness_temp(), ' K')
print('temperatura de ruído da antena: ', satelite.reception.get_antenna_noise_temp(), ' K')
print('temperatura de ruído na chuva: ', satelite.get_antenna_noise_rain(), 'K')
print('temperatura de ruído total: ', satelite.get_total_noise_temp(), ' K')
print('figura de mérito: ', satelite.get_figure_of_merit())

print('Densidade de potência na estação terrestre: ', satelite.get_power_flux_density())
print('C/N0: ', satelite.get_c_over_n0(satelite.p), ' dB')
print('limiar de recepção: ', satelite.get_reception_threshold(), ' dB')
print('SNR: ', satelite.get_snr(satelite.p), ' dB')
print('margem: ', satelite.get_snr(satelite.p) - satelite.get_reception_threshold(), ' dB')

print('tempo de execução: ', time.time() - start)





