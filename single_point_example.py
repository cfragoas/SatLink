from GrStat import GroundStation, Reception
from sat import Satellite
import numpy as np

# ground station parameters
site_lat = -3.7  # [decimal degrees]
site_long = -45.9  # [decimal degrees]
station = GroundStation(site_lat, site_long)

# satellite parameters
sat_long = -70  # [decimal degrees]
freq = 15  # [Ghz]
eirp = 54 # [dBW]
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

sat.set_grstation(station)  # relating the ground station object to a satellite one

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

sat.set_reception(reception)  # relating the ground station object to a satellite one

p = np.random.rand()  # creating a random percentage for the calculations
print('choosen p (%): ', p)

a_fs, a_dep, a_g, a_c, a_r, a_s, a_t, a_tot = sat.get_link_attenuation(p)

# displaying some reception parameters/variables
print('reception SNR threshold  ',sat.get_reception_threshold())

print('coordinates\' earth\'s radius: ', sat.grstation.get_earth_radius(), ' km')
print('elevation angle: ', sat.get_elevation(), ' degrees')
print('link distance: ', sat.get_distance(), ' km')
print('figure of merit: ', sat.get_figure_of_merit())
print('brightness temperature of the ground: ', sat.reception.get_ground_temp(), ' K')
print('sky brightness temperature', sat.reception.get_brightness_temp(), ' K')
print('antenna noise temperature: ', sat.reception.get_antenna_noise_temp(), ' K')
print('total noise temperature: ', sat.get_total_noise_temp(), ' K')
print('Rx antenna gain: ', sat.reception.get_antenna_gain(), ' dBi')
print('Rx antenna half power beamwidth: ', sat.reception.get_beamwidth(), ' degrees')

# displaying some link budget calculation results

print("gaseous attenuation: ", a_g, ' dB')
print("cloud attenuation: ", a_c, ' dB')
print("rain attenuation: ", a_r, ' dB')
print("scintillation attenuation: ", a_s, ' dB')
print("total atmospheric attenuation: ", a_t, ' dB')
print('free-space attenuation: ', a_fs, ' dB')
print('depointing loss: ', a_dep, ' dB')
print('atmospheric + free-space attenuation: ', a_tot, ' dB')
print('link C/N0: ', sat.get_c_over_n0(p), ' dB-Hz')
print('link SNR: ', sat.get_snr(p), ' dB')

# availability example calculation (this does not uses the variable p)
# actually, this changes p to achieve the target the modulation target SNR
print('example link availability', sat.get_availability())

