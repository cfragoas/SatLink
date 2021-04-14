from GrStat import GroundStation, Reception
from sat import Satellite
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

# ground station parameters
site_lat = -3.7  # [decimal degrees]
site_long = -45.9  # [decimal degrees]
station = GroundStation(site_lat, site_long)

# satellite parameters
sat_long = -70  # [decimal degrees]
freq = 12  # [Ghz]
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

availability_vector = []

ant_min = 0.6
ant_max = 4.5
step = 0.2
interp_step = int(round((ant_max - ant_min) * 100))

ant_size_vector = np.arange(ant_min, ant_max, step)
x_new = np.linspace(ant_min, ant_max, interp_step)

check = False
for ant_size in ant_size_vector:
    sat.reception.ant_size = ant_size
    availability_vector.append(sat.get_availability())
    # print(sat.get_availability())
    if sat.get_availability() >= 99.999 and check is False:
        max_availability_x = ant_size
        max_availability_y = sat.get_availability()
        check = True

a_BSpline = interpolate.make_interp_spline(ant_size_vector, availability_vector)
y_new = a_BSpline(x_new)
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Antenna Size x Year availability')
availability_time_vector = (1 - np.array(availability_vector)/100) * 8760

# ax1.plot(ant_size_vector, availability_vector)
ax1.plot(x_new, y_new)

ax2.plot(ant_size_vector, availability_time_vector)
# ax1.xlabel(' Antenna Size (m)')
# ax1.ylabel(' Availability (%year)')
# ax2.ylabel(' Availability (hours/year)')

plt.setp(ax1, ylabel='Availability (%year)')
plt.setp(ax2, xlabel='Antenna size')
plt.setp(ax2, ylabel='Availability (hours/year)')
plt.show()

# plt.plot(ant_size_vector, availability_vector)
# plt.plot(max_availability_x, max_availability_y)
# plt.xlabel(' Antenna Size (m)')
# plt.ylabel(' Availability (%year)')
# plt.title('Antenna Size x Year availability')
# plt.show()