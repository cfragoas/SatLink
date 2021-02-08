# SatCalc

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

SatCalc is a python based application that runs speciffic satellite downlink calcullations. It has a GUI and his main functions are:

  - Atmospheric attenuation calcullation (via itur (https://pypi.org/project/itur/))
  - Single and multi-point avaiability calcullation (input and output csv file)
  - Save and load parameters for satellites, ground stations and reception characteristics
  - Totally free !!!

# GUI Interface
For those that dont like code writing

![N|Solid](https://i.imgur.com/ZMpcxgH.png)

  - Simple Qt Gui made for simple usage
  - Drop lists can be edited via model folder

# Using SatCalc via python commands 
 SatCalc consists of three main classes 
 
  - Satellite class
  - Ground Station class
  - Reception class

You need to define those three objects and set their relationship
```sh
# creating the objects
station = GroundStation(site_lat, site_long)
sat = Satellite(sat_long, freq, eirp_max, hsat, b_transponder, b_util, _, _, mod, rolloff, fec)
receptor = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_noise_temp, cable_loss, desfoc_max)

# relating the objets to the satellite
sat.set_grstation(station)
sat.set_reception(receptor) 

# example - calcullating the link availability
availability = sat.get_availability()
print(availability)  # 0 - 100 percentage

# example - calcullating the power flux density in the reception point and the antenna noise in rain conditions
pw_flx = sat.get_power_flux_density()
print(pw_flx)  # watts/m²
ant_noise = sat.reception.get_antenna_noise_rain()
print(ant_noise)  # Kelvin
```

The other functions are detailed in the [READMEFILE]
