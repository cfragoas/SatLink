#Code-based usage
SatLink is structured with three main classes [Satellite](#satellite), [Reception](#reception) and 
[GroundStation](#groundstation). For the most functions, 
the user needs to instance an object of each class and relate these objects with a **set-type** function. 
Please check the [example](#examples) files.

For example, to calculate one link availability, execute the following steps:

Import the modules:

    from GrStat import GroundStation, Reception
    from sat import Satellite

Instanciate the objects of each class:

    station = GroundStation(site_lat, site_long)
    sat = Satellite(sat_long, freq, eirp_max, hsat, b_transponder, b_util, _, _, mod, rolloff, fec)
    receptor = Reception(ant_size, ant_eff, coupling_loss, polarization_loss, lnb_gain, lnb_noise_temp, cable_loss, desfoc_max)

Use the set functions:

    sat.set_grstation(station)
    sat.set_reception(receptor)

Use the link availability function with default values:

    availability = sat.get_availability()
    print(availability)

# Examples
Code-based examples can be found in Satlink main folder as **single_point_example.py**, **multi_point_example.py**,
**example_single_point_ant_size.py** and **example_multi_point_ant_size.py**. These examples use the majority of class functions
 and emulate the GUI calculations.

#Classes
##Satellite
Satellite is the code's main class. It has the majority of functions. Its parameters are:

###Parameters

* sat_long: geostationary satellite longitude in degrees
* freq: frequency in GHz
* eirp_max: transponder maximun E.I.R.P. in dBW
* h_sat: satellite height in Km
* b_transp: transponder bandwidth in MHz
* b_util: actual used transponder bandwidth
* back_off: decrease in transmitted power to avoid non-linear amplification
* modulation: please check **Modulation_dB.csv** in **models** folder to see the available modulations
* fec: please check **Modulation_dB.csv** in **models** folder to see the available options
* roll_off: factor of spectral efficiency, ROF (Roll-Off Factor)

### Functions
Satellite class functions are:

* to set the GroundStation object of the link the user wants to compute

        .set_grstation(grstation: GroundStation)

* to set the Reception object of the link the user wants to compute

        .set_reception(reception: Reception)

* to return the elevation angle between satellite and ground station (degrees)
  
        .get_elevation() # need set_grstation()


* to return the azimuth angle between satellite and ground station (degrees)
  
        .get_azimuth() # need set_grstation()


 * to return the distance between satellite and ground station (km)
   
        .get_distance() # need set_grstation()


 * to return the threshold for a given modulation and FEC
   
        .get_reception_treshold()


* to return multiple attenuation values: a_fs, depointing_loss, a_g, a_c, a_r, a_s, a_t, a_tot
  
        .get_link_attenuation(p=0.001, method='approx') # need set_grstation() and set_reception()


    * a_fs: free-space attenuation (dB)
    * depointing_loss: depointing for a given max. align mismatch (dB)
    * a_g: gaseous attenuation (dB)
    * a_c: cloud attenuation (dB)
    * a_r: rain attenuation (dB)
    * a_s: scintillation or tropospheric attenuation (dB)
    * a_t: total atmospheric attenuation (dB)
    * a_tot: total attenuation (free-space + atmospheric) (dB)

&NewLine;

* to return total attenuation values: a_t, a_tot and depoint_loss
  
        .get_total_attenuation(p= None) # need set_grstation() and set_reception()

    * a_t: total atmospheric attenuation (dB)
    * a_tot: total attenuation (free-space + atmospheric) (dB)
    * depoint_loss: depointing for a given max. align mismatch (dB)

&NewLine;

* to return the power flux density at the reception (W/m²)
  
        .get_get_power_flux_density(p=None) # need set_grstation() and set_reception()


* to return the antenna noise temperature under rain conditions (K)
  
        .get_antenna_noise_rain(p=None) # need set_grstation() and set_reception()

* to return reception's total noise temperature (K)
    
        .get_total_noise_temp(p=None) # need set_grstation() and set_reception()

* to return the link's figure of merit (G/T) (dB/K)
  
        .get_figure_of_merit(p=None) # need set_grstation() and set_reception()


* to return the carrier over noise per bandwidth unit (dB-Hz)
  
        .get_c_over_n0(p=None) # need set_grstation() and set_reception()

* to return the signal over noise (dB)
  
        .get_snr(p=None) # need set_grstation() and set_reception()

* to return the link availability (%/year) for a SNR + a given margin (dB) with a relaxation (dB) over the target value
    
        .get_availability(margin=0, relaxation=0.1) # need set_grstation() and set_reception()
  
    * margin: summed value over the modulation threshold to be considered. If margin = 0, the calculation target equals the modulation threshold.
    * relaxation: (+-) relaxation over the error between the target value and actual SNR in availability calculation
  

##Reception

###Parameters

* ant_size: antenna diameter in meters
* ant_eff: antenna efficiency (between 0 and 1)
* coupling_loss: coupling losses in dB
* polarization_loss: polarization loss in dB
* lnb_gain: LNB gain in dB
* lnb_noise_temp: LNB noise temperature in Kelvin
* cable_loss: cable loss in dB
* max_depoint: maximum depointing angle between transmission and reception (degrees)

###Functions

Reception class functions are:

* to return the calculated antenna gain (dB)
  
        .get_antenna_gain()

* to return the antenna 3dB beamwidth (degrees)
    
        .get_beamwidth():

* to return the calculated maximum depoint loss based on the maximum depointing angle (dB)
  
        .get_depoint_loss()

* to return the ground temperature received in the antenna (Kelvin)
  
        .get_ground_temp(self):

* to return the sky brightness temperature received in the antenna (Kelvin)
  
        .get_brightness_temp():

* to return the total antenna noise temperature (Kelvin)
  
        .get_antenna_noise_temp(self):


##GroundStation

###Parameters

* site_lat: site latitude in decimal degrees
* site_long: site longitude in decimal degrees

###Functions
Reception class functions are:

* to return the earth radius from lat, long (km)
  
        .get_earth_radius(self)

* to  return a nearest value from a point of a table. It is used in get_R001, get_h0 and get_hR.
 Its an auxiliary function and should be moved to another class in the future.
  
        getnearpos(self, array, value)

* to return the R001 (rain exceedance in 0.01% of year) value from ITU 837-7
  
        get_R001(self)

* to return h0 (isometric height) from ITU 839-4
  
        get_h0(self)

* to return hR (annual rain height) from ITU 839-4
    
        get_hR(self)












































































