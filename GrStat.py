import numpy as np
import pandas as pd
from scipy import constants as const
from models import util
import sys


# retorn parâmetros tabelados referenciados as coordenadas da estação terrena
# lat/long em formato de graus

class GroundStation:

    def __init__(self, site_lat, site_long):
        self.site_lat = site_lat
        self.site_long = site_long

        # variáveis calculadas internamente na classe

    def get_earth_radius(self):
        a = 6378137  # m
        b = 6356752.3142  # m
        phi = self.site_lat
        radius = (np.sqrt((((a ** 2) * np.cos(phi)) ** 2 + ((b ** 2) * np.cos(phi)) ** 2) /  # km
                          ((a * np.cos(phi)) ** 2 + (b * np.cos(phi)) ** 2))) / 1000
        return radius

    def getnearpos(self, array, value):
        # função para buscar os índices mais próximos dos valores amostrados nas tabelas (h0 e R001)
        idx = (np.abs(array - value)).argmin()
        return idx

    def get_R001(self):
        # função que retorna o valor de R001 dadas as coordenadas da estação terrena (ref. ITU 837-7)
        # R001 - taxa de precipitação da chuva excedida em 0.01% do ano

        R001_table = pd.read_csv('R001.csv', sep=';', index_col=0)  # linha=lat, coluna=long

        linhas_R001 = R001_table.index.to_numpy()
        colunas_R001 = R001_table.columns.to_numpy().astype('int32')

        R001 = (R001_table.iloc[self.getnearpos(linhas_R001, self.site_lat * 1000), self.getnearpos(colunas_R001,
                                                                                                    self.site_long * 1000)]) / 1000
        # tem que dividir por mil pelo formato que os dados da planilha são formatados (sem casa decimais)

        return R001

    def get_h0(self):
        # função que retorna o valor de h0 dadas as coordenadas da estação terrena (ref. ITU 839-4)
        # h0 - altura isotérmica sobre o nível do mar

        h0_table = pd.read_csv('h0.csv', sep=';', index_col=0)  # linha=lat, coluna=long

        linhas_h0 = h0_table.index.to_numpy()
        colunas_h0 = h0_table.columns.to_numpy().astype('int32')

        h0 = h0_table.iloc[
            self.getnearpos(linhas_h0, self.site_lat * 1000), self.getnearpos(colunas_h0, self.site_long * 1000)]

        return h0

    def get_hR(self):
        # função que retorna o valor de hR dadas as coordenadas da estação terrena (ref. ITU 839-4)
        # hR - altura média anual da chuva sobre o nível do mar
        hR = self.get_h0() + 0.36
        return hR


class Reception:

    def __init__(self, ant_size=1.2, ant_eff=0.6, coupling_loss=0.5, polarization_loss=3, lnb_gain = 60, lnb_noise_temp=20,
                 cable_loss=5, max_depoint = 0):

        self.ant_size = ant_size
        self.ant_eff = ant_eff
        self.coupling_loss = coupling_loss  # perda do feeder
        self.polarization_loss = polarization_loss  # perda de polarizacao (3dB de linear para circular ou vice e versa)
        self.lnb_gain = lnb_gain
        self.lnb_noise_temp = lnb_noise_temp
        self.cable_loss = cable_loss
        self.max_depoint = max_depoint  # maximum depointing angle between transmission and reception

        # vairáveis para armazenar os parâmetros calculados internamente na classe
        self.gain = None
        self.t_ground = None
        self.t_sky = None
        self.t_ant = None
        self.total_noise_temp = None
        self.figure_of_merit = None  # G/T
        self.angle_3db = None  # 3 db or half-power angle
        self.a_dep = None

        # parâmetros de outras classes e não setados ou calculados em na classe Reception
        self.freq = None
        self.e = None
        self.a_rain = None

    def set_parameters(self, freq, e):
        self.freq = freq
        self.e = e
        pass

    def get_antenna_gain(self):
        if self.freq is None:
            sys.exit('Need to associate a reception to a satellite first. Try satellite.set_reception(reception)!!!')
        else:
            self.gain = (10 * np.log10(self.ant_eff * (np.pi * self.ant_size * self.freq * (10 ** 9) /
                                        (const.c)) ** 2))
        return self.gain

    def get_beamwidth(self):
        if self.angle_3db is not None:
            return self.angle_3db
        elif self.ant_size is None or self.freq is None:
            sys.exit('You need to set the antenna size and system frequency before this calculation!!!')
        else:
            self.angle_3db = 70 * (const.c / (self.freq * 10 ** 9 * self.ant_size))

        return self.angle_3db

    def get_depoint_loss(self):
        if self.a_dep is not None:
            return self.a_dep
        self.a_dep = 12 * ((self.max_depoint/self.get_beamwidth()) ** 2)

        return self.a_dep

    def get_ground_temp(self):
        if self.t_ground is not None:
            return self.t_ground
        else:
            if self.e < -10:
                self.t_ground = 290
            elif 0 > self.e > -10:
                self.t_ground = 150
            elif 10 > self.e > 0:
                self.t_ground = 50
            elif 90 > self.e > 10:
                self.t_ground = 10
            else:
                sys.exit('Ground temperature can only be calculated for elevation angles between -10 and 90!!!')
        return self.t_ground

    def get_brightness_temp(self, printer=False):
        if self.freq is None or self.e is None:
            sys.exit('Need to associate a reception to a satellite first. Try satellite.set_reception(reception)!!!')
        elif self.t_sky is not None:
            return self.t_sky
        else:
            data = pd.read_csv('models\\ClearSkyTemp ITU 372.csv', sep=';', index_col=0)
            self.t_sky = util.curve_interpolation(self.freq, self.e, data)
        if printer:
            print('elevation: ', self.e, ' freq: ', self.freq, ' Tsky (brightness temperature): ', self.t_sky)

        return self.t_sky

    def get_antenna_noise_temp(self):
        if self.t_ant is not None:
            return self.t_ant
        else:
            self.t_ant = self.get_brightness_temp() + self.get_ground_temp()
        return self.t_ant

