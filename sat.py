import sys
import numpy as np
import pandas as pd
import itur
from GrStat import GroundStation, Reception
from models.FsAtt import FreeSpaceAtt as FsAtt
import astropy.units as u
from models.util import truncate


# classe destinada ao calculo dos parâmetros espaciais relacionados ao satélite geoestacionário

class Satellite:
    # todos os parâmetros lat/long estão em formato de graus na entrada e na saída das funções

    def __init__(self, sat_long, freq, eirp_max=0, h_sat=35786, b_transp=36, b_util=36, back_off=0, contorno=0,
                 modulation='', roll_off=None, fec=''):
        self.sat_long = np.radians(sat_long)  # satellite longitude
        self.freq = freq  # frequency, in GHz
        self.eirp_max = eirp_max  # sattelite's eirp, in dBW
        self.h_sat = h_sat  # satellite's height
        self.b_transp = b_transp  # transpounder's band, in GHz
        self.b_util = b_util  # transponder's band that the carrier is using, in GHz
        self.back_off = back_off  # transponder's back off ????????????????
        self.contorno = contorno  # ver que diabos é isso aqui ????????????????
        # self.tech = tech  # technology (DVB-S, S2, S2X)
        self.modulation = modulation  # modulation name
        self.fec = fec  # FEC
        self.roll_off = roll_off
        self.eirp = eirp_max - back_off - contorno + 10 * np.log10(b_util / b_transp)

        # parâmetros não inicializáveis referentes à atenuação por chuva e espaço livre
        self.a_g = None  # gaseous attenuation
        self.a_c = None  # could attenuation
        self.a_r = None  # rain attenuation
        self.a_s = None  # citilation or tropospheric attenuation
        self.a_t = None  # total atmospheric attenuation
        self.a_fs = None  # free space attenuation
        self.a_tot = None  # total attenuation (atmospheric + free space)
        self.p = None  # exceed percentage - just to store the attenuation inm reference to a p value

        # outros parâmetros calculados na classe
        self.power_flux_density = None # power flux density at earth station (W/m^2)
        self.antenna_noise_rain = None
        self.total_noise_temp = None
        self.figure_of_merit = None
        self.c_over_n0 = None  # calculated C/N
        self.snr = None  # calculated SNR
        self.snr_threshold = None  # SNR threshold for a specific
        self.availability = None  # availability for a specific SNR threshold
        self.symbol_rate = None  # symbolrate based on the bandwidth and roll off factor
        self.bitrate = None  # bitrate based on the badwidth and inforate efficiency

        # objetos estação terrena e recepção relacionados ao satélite
        self.grstation = None  # ground station oject
        self.reception = None  # reception object

    def set_grstation(self, grstation: GroundStation):
        self.grstation = grstation
        pass

    def set_reception(self, reception: Reception):  # set the link's reception system
        reception.set_parameters(self.freq, self.get_elevation())  # parameters used in some functions in Reception
        self.reception = reception

        pass

    def get_elevation(self):  # returns the elevation angle between satellite and ground station
        if self.grstation is None:
            sys.exit(
                'Need to associate a ground station to a satellite first. Try satellite.set_reception(reception)!!!')

        site_lat = np.radians(self.grstation.site_lat)
        site_long = np.radians(self.grstation.site_long)
        E = np.arctan((np.cos(self.sat_long - site_long) * np.cos(site_lat) - 0.15116) /
                      (np.sqrt(1 - (np.cos(self.sat_long - site_long) ** 2) * (np.cos(site_lat) ** 2))))

        return np.degrees(E)

    def get_azimuth(self):  # returns the azimuth angle between satellite and ground station
        if self.grstation is None:
            sys.exit(
                'Need to associate a ground station to a satellite first. Try satellite.set_reception(reception)!!!')

        site_lat = np.radians(self.grstation.site_lat)
        site_long = np.radians(self.grstation.site_long)
        azimuth = np.pi + np.arctan2(np.tan(self.sat_long - site_long), np.sin(site_lat))

        return np.degrees(azimuth)

    def get_distance(self):  # returns the distance (km) between satellite and ground station
        if self.grstation is None:
            sys.exit(
                'Need to associate a ground station to a satellite first. Try satellite.set_reception(reception)!!!')

        e = np.radians(self.get_elevation())
        earth_rad = self.grstation.get_earth_radius()
        dist = np.sqrt(((earth_rad + self.h_sat) ** 2) - ((earth_rad * np.cos(e)) ** 2)) - earth_rad * np.sin(e)
        return dist

    def get_reception_threshold(self):
        if self.modulation == '' or self.fec == '':
            sys.exit(
                'You need to create a satellite class with a technology, modulation and FEC to use this function!!!')
        elif self.snr_threshold is not None:
            return self.snr_threshold

        data = pd.read_csv('models\\Modulation_dB.csv', sep=';')
        # line = data.loc[(data.Tech == self.tech) & (data.Modulation == self.modulation) & (data.FEC == self.fec)]
        line = data.loc[(data.Modulation == self.modulation) & (data.FEC == self.fec)]
        self.snr_threshold = line['C_over_N'].values[0]
        return self.snr_threshold

    def get_symbol_rate(self):
        if self.symbol_rate is not None:
            return self.symbol_rate
        if self.roll_off is None:
            sys.exit('You must define the roll off factor to calculate the symbol rate!!!')
        self.symbol_rate = self.b_util * 10 ** 6 / self.roll_off
        return self.symbol_rate

    def get_bitrate(self):
        if self.bitrate is not None:
            return self.bitrate
        if self.modulation == '' or self.fec == '':
            sys.exit(
                'You need to create a satellite class with a technology, modulation and FEC to use this function!!!')
        data = pd.read_csv('models\\Modulation_dB.csv', sep=';')
        line = data.loc[(data.Modulation == self.modulation) & (data.FEC == self.fec)]
        self.bitrate = self.b_util * line['Inforate efficiency bps_Hz'].values[0]
        return self.bitrate

    def get_link_attenuation(self, p=0.001):
        if self.grstation is None:
            sys.exit(
                'Need to associate a ground station to a satellite first. Try satellite.set_reception(reception)!!!')
        if self.reception is None:
            sys.exit('Need to associate a reception to a satellite first. Try satellite.set_reception(reception)!!!')
        if self.a_tot is not None and p == self.p:
            return self.a_fs, self.reception.get_depoint_loss(), self.a_g, self.a_c, self.a_r, self.a_s, self.a_t, self.a_tot
        else:
            freq = self.freq * u.GHz
            e = self.get_elevation()
            diam = self.reception.ant_size * u.m
            a_fs = FsAtt(self.get_distance(), self.freq)
            a_g, a_c, a_r, a_s, a_t = itur.atmospheric_attenuation_slant_path(
                self.grstation.site_lat, self.grstation.site_long, freq, e, p, diam, return_contributions=True)
            a_tot = a_fs + self.reception.get_depoint_loss() + a_t.value

            self.a_g = a_g
            self.a_c = a_c
            self.a_r = a_r
            self.a_s = a_s
            self.a_t = a_t
            self.a_fs = a_fs
            self.a_tot = a_tot
            self.p = p

            # erasing the dependent variables that will use link atten. for different p value
            self.power_flux_density = None
            self.antenna_noise_rain = None
            self.total_noise_temp = None
            self.figure_of_merit = None
            self.c_over_n0 = None
            self.snr = None

        return a_fs, self.reception.get_depoint_loss(), a_g, a_c, a_r, a_s, a_t, a_tot

    def get_power_flux_density(self, p=None):
        if self.grstation is None:
            sys.exit('Need to associate a grd. station to a satellite first. Try Satellite.set_grstation(Station)!!!')
        elif self.reception is None:
            sys.exit('Need to associate a reception to a satellite first. Try Satellite.set_reception(Reception)!!!')
        elif self.power_flux_density is not None and p == self.p:
            return self.power_flux_density

        if p is not None:
            _, _, _, _, _, _, a_t, _ = self.get_link_attenuation(p)
        else:
            _, _, _, _, _, _, a_t, _ = self.get_link_attenuation(self.p)

        a_t = a_t.value
        phi = (10 ** ((self.eirp - a_t)/10)) / (4 * np.pi * ((self.get_distance() * 1000 ) ** 2))

        self.power_flux_density = 10 * np.log10(phi)

        return self.power_flux_density

    def get_antenna_noise_rain(self, p=None):
        if self.reception is None:
            sys.exit('Need to associate a reception to a satellite first. Try satellite.set_reception(reception)!!!')
        elif self.antenna_noise_rain is not None and self.p == p:
            return self.antenna_noise_rain

        if p is not None:
            _, _, _, _, _, _, a_t, _ = self.get_link_attenuation(p)
        else:
            _, _, _, _, _, _, a_t, _ = self.get_link_attenuation(self.p)
        Tm = 275
        a_t = 10 ** (a_t.value/10)
        self.antenna_noise_rain = self.reception.get_brightness_temp()/a_t + (Tm * (1-1/a_t)) + self.reception.get_ground_temp()
        return self.antenna_noise_rain

    def get_total_noise_temp(self, p=None):
        if self.freq is None or self.reception.e is None:
            sys.exit('Need to associate a reception to a satellite first. Try satellite.set_reception(reception)!!!')
        elif self.total_noise_temp is not None and p == self.p:
            return self.total_noise_temp
        if p is not None:
            _, _, _, _, _, _, a_t, _ = self.get_link_attenuation(p)

        # self.total_noise_temp = (self.get_antenna_noise_rain() / (10 ** (self.reception.feeder_loss / 10))
        #                          + self.reception.feeder_noise_temp * (
        #                                  1 - 1 / (10 ** (self.reception.feeder_loss / 10))) + self.reception.lnbf_noise_temp)

        total_loss = self.reception.coupling_loss + self.reception.cable_loss
        loss = 10 ** (total_loss/10)
        t_loss = 290 * (loss - 1)
        self.total_noise_temp = self.get_antenna_noise_rain() +\
                                (self.reception.lnb_noise_temp + t_loss/(10 ** (self.reception.lnb_gain/10)))


        return self.total_noise_temp

    def get_figure_of_merit(self, p=None):
        if self.figure_of_merit is not None:
            return self.figure_of_merit
        elif self.figure_of_merit is not None and p == self.p:
            return self.figure_of_merit
        if p is not None:
            _, _, _, _, _, _, _, _ = self.get_link_attenuation(p)

        # self.figure_of_merit = 10 * np.log10(((10 **
        #                                        ((self.reception.get_antenna_gain() + 65 - (self.reception.feeder_loss +
        #                                        self.reception.get_depoint_loss() + self.reception.polarization_loss)) / 10))
        #                                       / self.get_total_noise_temp()))
        self.figure_of_merit = self.reception.get_antenna_gain() - \
                               self.reception.get_depoint_loss() - self.reception.polarization_loss - \
                               - self.reception.coupling_loss - self.reception.cable_loss - \
                               10 * np.log10(self.get_total_noise_temp())
        return self.figure_of_merit

    def get_c_over_n0(self, p=None):  # returns the C/N for the satellite link
        if self.reception is None:
            sys.exit('Need to associate a reception to a satellite first. Try satellite.set_reception(reception)!!!')
        if self.eirp_max == 0:
            sys.exit('Please set the satellite\'s E.I.R.P before running this!!!')
        if self.c_over_n0 is not None and self.p == p:
            return self.c_over_n0

        if p is not None:
            _, _, _, _, _, _, _, a_tot = self.get_link_attenuation(p)
        else:
            _, _, _, _, _, _, _, a_tot = self.get_link_attenuation(self.p)

        figure_of_merit = self.get_figure_of_merit()
        self.c_over_n0 = self.eirp - a_tot + figure_of_merit + 228.6

        self.snr = None  # erasing the dependent variables that will use C/N0 for different p value
        return self.c_over_n0

    def get_snr(self, p=None):
        if p == self.p and self.snr is not None:
            return self.snr
        if p is not None:
            _, _, _, _, _, _, _, _ = self.get_link_attenuation(p)
        else:
            _, _, _, _, _, _, _, _ = self.get_link_attenuation(self.p)

        self.snr = self.get_c_over_n0(p) - 10 * np.log10(self.b_util * (10 ** 6))

        return self.snr

    def get_availability(self, margin=0, relaxation=0.1):
        target = self.get_reception_threshold() + margin
        p = 0.0012
        speed = 0.000005
        speed_old = 0
        delta_old = 1000000000
        p_old = 10000000
        delta = self.get_snr(0.001) - target
        # relaxation = 0.1
        if delta >= 0:
            return 99.999

        for i in range(1, 5000):
            delta = abs(self.get_snr(p) - target)
            if delta < relaxation:
                self.availability = 100 - p
                return truncate(self.availability, 3)

            if delta_old < delta:
                if (abs(p_old - p) < 0.001) and (speed_old * speed < 1):
                    self.availability = 100 - p
                    return truncate(self.availability, 3)

                speed_old = speed
                speed = -1 * speed / 10
                p_old = p
                p += speed
            else:
                speed_old = speed
                speed = speed * 1.5
                p_old = p
                p += speed

            if p < 0.001:
                p_old = 100
                p = 0.001 + np.random.choice(np.arange(0.001, 0.002, 0.000005))
                speed_old = 1
                speed = 0.000005
                delta = abs(self.get_snr(p) - target)
            if p > 50:
                p_old = 100
                p = 50 - np.random.choice(np.arange(0.01, 2, 0.01))
                speed_old = 1
                speed = 0.000005

            if speed > 2:
                speed = 2
                speed_old = 1

            delta_old = delta

            # if i % 500 == 0:
            #     relaxation += 0.1

        sys.exit(
            'Can\'t reach the required SNR. You can change the modulation settings or the required snr relaxation!!!')
