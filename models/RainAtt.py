import numpy as np
from numpy import log as ln
from models.spec_att import specific_attenuation
from sat import satellite
from GrStat import ground_station


# VARIÁVEIS DE ENTRADA

site_lat = -3.7
site_long = -45.9
sat_long = -70
f = 3.5
tau = 90 #H=0, V = 90, circ = 45
hS = 0.447 #altura da estação terrena
ant_diam = 1.2
p = 0.01

station = ground_station(site_lat, site_long, ant_diam)
# primeiro passo - determinar R0,01

R001 = station.get_R001()

# segundo passo - calcular a altura efetiva da chuva hR

hR = station.get_hR()

# terceiro passo - calcular o percurso inclinado na chuva LS
# hs - altura da estação terrena
# E - angulo de elevação

sat = satellite(sat_long, f)
E = sat.get_elevation(site_lat, site_long)
LS = (hR - hS) / np.sin(np.radians(E))

# quarto passo - calcular a projeção no plano horizontal (LG) do percurso inclinado

LG = LS * np.cos(np.radians(E))

# quinto passo - calular a atenuação específica gamaR
# isto é feito através da classe specific_attenuation (ref. ITU P.838-3)

gamaR = specific_attenuation().get_gamaR(R001, f, E, tau)

# sexto passo - calcular o fator de redução horizontal r001

r001 = (1 + 0.078 * np.sqrt(LG * gamaR / f) - 0.38 * (1 - np.exp(-2 * LG))) ** (-1)

# sétimo passo - calcular o fator de ajuste vertical v001
# para se obter o v001, é necessário calcular outras variáveis - zeta, LR e chi

# zeta (graus)
zeta = np.tan(np.radians((hR - hS) / (LG * r001))) ** (-1)

# LR (km)
if zeta > E:
    LR = LG * r001 / np.cos(np.radians(E))
else:
    LR = (hR - hS) / np.sin(np.radians(E))
# chi
if abs(site_lat) < 36:
    chi = 36 - abs(site_lat)
else:
    chi = 0

v001 = (1 + np.sqrt(np.sin(np.radians(E))) * (
            31 * (1 - np.exp(-E / (1 + chi))) * (np.sqrt(LR * gamaR) / f ** 2) - 0.45)) ** (-1)

# oitavo passo - calcular a distância LE do percurso (km)

LE = LR * v001

# nono passo - finalmente, a atenuação excedida para 0,01% da média anual A001

A001 = gamaR * LE

# CONVERSÃO PARA OUTROS VALORES DO PROBABILIDADE p DA CHUVA ALÉM DE 0,01% (menor que 5%)

if p > 0.0001:
    # determinação de beta

    if p >= 0.01 or abs(site_lat) > 36:
        beta = 0
    elif p <= 0.01 and abs(site_lat) < 36 and E > 25:
        beta = -0.005 * (abs(site_lat) - 36)
    else:
        beta = -0.005 * (abs(site_lat) - 36) + 1.8 - 4.25 * np.sin(np.radians(E))

    # convertendo o balor de A001 para o valor Ap de um p diferente

    Ap = A001 * (p / 0.01) ** -(0.655 + 0.033 * ln(p) - 0.045 * ln(A001) - beta * (1 - p) * np.sin(np.radians(E)))

else:

    Ap = A001
print('E ', E)
print('hR ', hR)
print('LS ', LS)
print('LG ', LG)
print('zeta ', zeta)
print('chi ', chi)
print('gamaR ', gamaR)
print('r001 ', r001)
print('vv001 ', v001)
print('LE ', LE)
print('AP ', Ap)
print('A001 ', A001)

