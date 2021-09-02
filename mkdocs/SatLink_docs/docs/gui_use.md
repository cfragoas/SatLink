# Graphical User Interface

To use Satlink's graphical interface, the user must run **main_window.py** via python.

From there, the user has 4 list options [File](#file), [Single Point Calculation](#single-point-calculation), 
[List Calculation](#list-calculation) and [Help](#help).

![home](..\images\home.png)

&NewLine;

## File
Same as Satlink's main classes, the graphical user interface uses 3 types of parameters: [satellite parameters](#satellite), 
[reception parameters](#reception) and [ground station parameters](#ground-station). Each one has a unique file extension and can be saved/loaded. 
The File menu lists page options to manage these files outside of calculation windows.

See [save/load dialog](#saveload-dialog-boxes) window for more details in these options and [file types](#file-types).

![file menu](..\images\file_menu.png)

### Satellite

To create a satellite, one user must fill the following fields:

* Name: satellite identification name 
* Longitude: geostationary satellite longitude in degrees
* Frequency: frequency in GHz
* E.I.R.P: transponder maximum E.I.R.P. in dBW
* Altitude: satellite height in Km
* Transponder's max bandwidth: transponder bandwidth in MHz
* Effective bandwidth: actual used transponder bandwidth
* back_off: decrease in transmitted power to avoid non-linear amplification
* Modulation: modulations and FEC combinations from the available list of modulations/FECs
* Roll-off: factor of spectral efficiency, ROF (Roll-Off Factor)
* Polarization: horizontal, vertical or circular polarization

![satellite page](..\images\satellite_page.png)

Click on "Save" button to save satellite parameters to a .sat file. 

Click on "Load" button to load satellite parameters from a .sat file.

Click on "Clear" button to clear all fields on the screen.

### Ground Station

To create a ground station, one user must fill the following fields:

* Name: ground station identification name 
* Latitude: site latitude in decimal degrees
* Longitude: site longitude in decimal degrees

![grpund station page](..\images\grd_station_page.png)

Click on "Save" button to save satellite parameters to a .gst file. 

Click on "Load" button to load satellite parameters from a .gst file.

Click on "Clear" button to clear all fields on the screen.

### Reception

To create a reception system, one user must fill the following fields:

* Name: reception identification name 
* Antenna size: antenna diameter in meters
* Antenna efficiency: antenna efficiency (between 0 and 1)
* LNB gain: LNB (Low Noise Block) in dB
* LNB noise temp.: LNB noise temperature in Kelvin
* Additional losses: connection and any other losses considered at reception in dB
* Cable loss: cable loss in dB
* Maximum depointing: maximum depointing angle between transmission and reception (degrees)

![reception page](..\images\reception_page.png)

Click on "Save" button to save satellite parameters to a .rcp file. 

Click on "Load" button to load satellite parameters from a .rcp file.

Click on "Clear" button to clear all fields on the screen.

## Single Point Calculation

Single point calculations consists in 3 types of functionalities: [Atmospheric Attenuation](#atmospheric-attenuation), 
[Downlink Performance](#downlink-performance) and [Antenna Size](#antenna-size). This type of operation returns a complete analysis in a report type format.

![single point menu](..\images\single_menu.png)

### Atmospheric Attenuation

In this screen, the user can estimate complete atmospheric attenuation data with minimum parameters.

#### Inputs

* **Reception parameters** (ground station coordinates + reception antenna parameters):
    * Latitude: site longitude in decimal degrees
    * Longitude: site longitude in decimal degrees
    * Antenna size: antenna diameter in meters
    * Antenna efficiency: antenna efficiency (between 0 and 1)    
* **Satellite parameters**:
    * Longitude: geostationary satellite longitude in degrees
    * Frequency: frequency in GHz
    * Polarization: horizontal, vertical or circular polarization
* Excess % of time per year: percentage of time the values are exceeded
* Method: exact or approximate calculation methods from ITU 676
  
Default Satellites box has a satellite list that sets the longitude coordinates accordingly.

#### Buttons

* Load Ground Station: loads latitude and longitude from a .gst file.
* Load Reception: loads antenna size and antenna efficiency from a .rcp file.
* Load Satellite: loads satellite parameters from a .sat file.



![single point atm](..\images\single_atm_calc.png)

#### Outputs

* Earth's radius in lat/long (km)
* Elevation angle (degrees)
* Link length (km)
* Ground noise temperature (K)
* Sky brightness temperature (K)
* Antenna noise temperature (K)
* Antenna noise temperature w/ rain (K)
* Total noise temperature (K)
* Reception antenna gain (dBi)
* Reception antenna 3dB beamwidth (degrees)
* Figure of Merit (dB/K)
* Gaseous attenuation (dB)
* Cloud attenuation (dB)
* Rain attenuation (dB)
* Scintillation attenuation (dB)
* Total atmospheric attenuation (dB)
* Free space attenuation (dB)
* Free space + atmospheric + depointing attenuation (dB)


### Downlink Performance

In this screen, the user can estimate a link budget and availability of a satellite downlink.

#### Inputs

* **Ground Station parameters**
    * Name: ground station identification name 
    * Latitude: site latitude in decimal degrees
    * Longitude: site longitude in decimal degrees
* **Satellite parameters**
    * Name: satellite identification name 
    * Longitude: geostationary satellite longitude in degrees
    * Frequency: frequency in GHz
    * E.I.R.P: transponder maximum E.I.R.P. in dBW
    * Altitude: satellite height in Km
    * Transponder's max bandwidth: transponder bandwidth in MHz
    * Effective bandwidth: actual used transponder bandwidth
    * back_off: decrease in transmitted power to avoid non-linear amplification
    * Modulation: modulations and FEC combinations from the available list of modulations/FECs
    * Roll-off: factor of spectral efficiency, ROF (Roll-Off Factor)
    * Polarization: horizontal, vertical or circular polarization
* **Reception parameters**
    * Name: reception identification name 
    * Antenna size: antenna diameter in meters
    * Antenna efficiency: antenna efficiency (between 0 and 1)
    * LNB gain: LNB (Low Noise Block) in dB
    * LNB noise temp.: LNB noise temperature in Kelvin
    * Additional losses: connection and any other losses considered in the reception in dB
    * Cable loss: cable loss in dB
    * Maximum depointing: maximum depointing angle between transmission and reception (degrees)
* **Calculation parameters**
    * SNR target relaxation: (+-) relaxation over the error between the target value and actual snr in availability
      calculation
    * Margin: summed value over the modulation threshold to be considered. If margin = 0, 
      the calculation target equals the modulation threshold.
    
Default Satellites box has a satellite list that sets the longitude coordinates accordingly.

#### Buttons

* **Ground Station buttons**
    * Clear: clears ground station fields
    * Load: loads ground station parameters from a .gst file.
    * Save: loads ground station parameters into a .gst file.
* **Reception buttons**
    * Clear: clears reception fields
    * Load Reception: loads reception parameters from a .rcp file.
    * Save: loads reception parameters into a .rcp file.
* **Satellite buttons**
    * Clear: clears satellite fields
    * Load Reception: loads satellite parameters from a .rcp file.
    * Save: loads satellite parameters into a .rcp file.
* Calculate: runs the link performance calculation.

![single point atm](..\images\single_down_perf.png)

#### Outputs

* Link budget at 0.001% of the year
    * C/N0 (dB)
    * SNR (dB)
* Actual SNR target's availability (year%)
* Reception characteristics:
    * Earth's radius in lat/long (km)
    * Elevation angle (degrees)
    * Link length (km)
    * Ground noise temperature (K)
    * Sky brightness temperature (K)
    * Antenna noise temperature (K)
    * Antenna noise temperature w/ rain (K)
    * Total noise temperature (K)
    * Reception antenna gain (dBi)
    * Reception antenna 3dB beamwidth (degrees)
    * Figure of Merit (dB/K)
* Link budget Analysis:
    * Gaseous attenuation (dB)
    * Cloud attenuation (dB)
    * Rain attenuation (dB)
    * Scintillation attenuation (dB)
    * Total atmospheric attenuation (dB)
    * Free space attenuation (dB)
    * Free space + atmospheric + depointing attenuation (dB)
    * Reception threshold (SNR) (dB)
  
### Antenna Size

In this screen, the user can estimate the availability for multiple antenna sizes of a satellite downlink.

#### Inputs

* **Ground Station parameters**
    * Name: ground station identification name 
    * Latitude: site latitude in decimal degrees
    * Longitude: site longitude in decimal degrees
* **Satellite parameters**
    * Name: satellite identification name 
    * Longitude: geostationary satellite longitude in degrees
    * Frequency: frequency in GHz
    * E.I.R.P: transponder maximum E.I.R.P. in dBW
    * Altitude: satellite height in Km
    * Transponder's max bandwidth: transponder bandwidth in MHz
    * Effective bandwidth: actual used transponder bandwidth
    * back_off: decrease in transmitted power to avoid non-linear amplification
    * Modulation: modulations and FEC combinations from the available list of modulations/FECs
    * Roll-off: factor of spectral efficiency, ROF (Roll-Off Factor)
    * Polarization: horizontal, vertical or circular polarization
* **Reception parameters**
    * Name: reception identification name
    * Antenna efficiency: antenna efficiency (between 0 and 1)
    * LNB gain: LNB (Low Noise Block) in dB
    * LNB noise temp.: LNB noise temperature in Kelvin
    * Additional losses: connection and any other losses considered in the reception in dB
    * Cable loss: cable loss in dB
    * Maximum depointing: maximum depointing angle between transmission and reception (degrees)
* **Calculation parameters**
    * Ant. min. size: minimum antenna diameter to be calculated in meters
    * Ant. max. size: maximum antenna diameter to be calculated in meters
    * Margin: summed value over the modulation threshold to be considered. If margin = 0, 
      the calculation target equals the modulation threshold.
    
Default Satellites box has a satellite list that sets the longitude coordinates accordingly.

#### Buttons

* **Ground Station buttons**
    * Clear: clears ground station fields
    * Load: loads ground station parameters from a .gst file.
    * Save: loads ground station parameters into a .gst file.
* **Reception buttons**
    * Clear: clears reception fields
    * Load Reception: loads reception parameters from a .rcp file.
    * Save: loads reception parameters into a .rcp file.
* **Satellite buttons**
    * Clear: clears satellite fields
    * Load Reception: loads satellite parameters from a .rcp file.
    * Save: loads satellite parameters into a .rcp file.
* Calculate button: runs the link performance calculation.
* Export graph button: save the displayed graph in a .png image file.

![single ant size](..\images\single_ant_sz_calc.png)

#### Outputs

There are two outputs in this operation: a list in text format containing antenna size vs. availability and 
a matplotlib graph will also be displayed.

## List Calculation  

Multiple point calculations consists in 2 functionalities: **Downlink Performance** and **Antenna Size**. 
These operations use a .csv file as input and return a new .csv file with a result column.

![multi point menu](..\images\list_menu.png)

### Downlink Performance

In this screen, the user can estimate the availability of satellite downlink for multiple points.

##### Inputs
* Path: path to the input .csv file 
  * .csv file columns: Name, Lat, Long, Delta Footprint (optional)
    * Name: point name
    * Lat: point latitude in decimal degrees
    * Longitude: point longitude in decimal degrees
    * Delta Footprint: optional argument. Represents the difference between the maximum power 
      received and the received one in the chosen coordinate (in case of footprint differences between coordinates)
    * a .csv example can be found in **input examples** folder
* **Satellite parameters**
    * Name: satellite identification name 
    * Longitude: geostationary satellite longitude in degrees
    * Frequency: frequency in GHz
    * E.I.R.P: transponder maximum E.I.R.P. in dBW
    * Altitude: satellite height in Km
    * Transponder's max bandwidth: transponder bandwidth in MHz
    * Effective bandwidth: actual used transponder bandwidth
    * back_off: decrease in transmitted power to avoid non-linear amplification
    * Modulation: modulations and FEC combinations from the available list of modulations/FECs
    * Roll-off: factor of spectral efficiency, ROF (Roll-Off Factor)
    * Polarization: horizontal, vertical or circular polarization
* **Reception parameters**
    * Name: reception identification name 
    * Antenna size: antenna diameter in meters
    * Antenna efficiency: antenna efficiency (between 0 and 1)
    * LNB gain: LNB (Low Noise Block) in dB
    * LNB noise temp.: LNB noise temperature in Kelvin
    * Additional losses: connection and any other losses considered in the reception in dB
    * Cable loss: cable loss in dB
    * Maximum depointing: maximum depointing angle between transmission and reception (degrees)
* **Calculation parameters**
    * SNR target relaxation: (+-) relaxation over the error between the target value and actual SNR in availability
      calculation
    * Margin: summed value over the modulation threshold to be considered. If margin = 0, 
      the calculation target equals the modulation threshold.
    * Threads: number of simultaneous executed calculations. The maximum number o threads depends on the user's processor. 
    
Default Satellites box has a satellite list that sets the longitude coordinates accordingly.

#### Buttons

* Browse button: opens a dialog box to select the .csv file used as input for the calculations.
* **Reception buttons**
    * Clear: clears reception fields
    * Load Reception: loads reception parameters from a .rcp file.
    * Save: loads reception parameters into a .rcp file.
* **Satellite buttons**
    * Clear: clears satellite fields
    * Load Reception: loads satellite parameters from a .rcp file.
    * Save: loads satellite parameters into a .rcp file.
* Calculate: runs the link performance calculation.

![multi point menu](..\images\multi_down_perf.png)

#### Outputs

A progress bar will appear when the process is started. When the process is completed, the progress bar will 
disappear, and a 'Complete!' message will show up. After that, the user can see the .csv output file in **results** folder. 

### Antenna Size

In this screen, the user can estimate the availability of satellite downlink for multiple points.

##### Inputs
* Path: path to the input .csv file 
  * .csv file columns: Name, Lat, Long, Delta Footprint (optional)
      * Name: point name
      * Lat: point latitude in decimal degrees
      * Longitude: point longitude in decimal degrees
      * Delta Footprint: optional argument. Represents the difference between the maximum power 
        received and the received one in the chosen coordinate (in case of footprint differences between coordinates)
    * a .csv example can be found in **input examples** folder
* **Satellite parameters**
    * Name: satellite identification name 
    * Longitude: geostationary satellite longitude in degrees
    * Frequency: frequency in GHz
    * E.I.R.P: transponder maximum E.I.R.P. in dBW
    * Altitude: satellite height in Km
    * Transponder's max bandwidth: transponder bandwidth in MHz
    * Effective bandwidth: actual used transponder bandwidth
    * back_off: decrease in transmitted power to avoid non-linear amplification
    * Modulation: modulations and FEC combinations from the available list of modulations/FECs
    * Roll-off: factor of spectral efficiency, ROF (Roll-Off Factor)
    * Polarization: horizontal, vertical or circular polarization
* **Reception parameters**
    * Name: reception identification name
    * LNB gain: LNB (Low Noise Block) in dB
    * LNB noise temp.: LNB noise temperature in Kelvin
    * Additional losses: connection and any other losses considered in the reception in dB
    * Cable loss: cable loss in dB
    * Maximum depointing: maximum depointing angle between transmission and reception (degrees)
    * Antenna efficiency: antenna efficiency (between 0 and 1)
* **Calculation parameters**
    * Availability target: availability to be achieved in calculations (% - between 0 and 99.999). 
      Satlink will choose the minimum atenna size for the chosen availability.
    * SNR target relaxation: (+-) relaxation over the error between the target value and actual SNR in availability
      calculation
    * Margin: summed value over the modulation threshold to be considered. If margin = 0, 
      the calculation target equals the modulation threshold.
    * Threads: number of simultaneous executed calculations. The maximum number o threads depends on the user's processor. 
    
Default Satellites box has a satellite list that sets the longitude coordinates accordingly.

#### Buttons

* Browse button: opens a dialog box to select the .csv file used as input for the calculations.
* **Reception buttons**
    * Clear: clears reception fields
    * Load Reception: loads reception parameters from a .rcp file.
    * Save: loads reception parameters into a .rcp file.
* **Satellite buttons**
    * Clear: clears satellite fields
    * Load Reception: loads satellite parameters from a .rcp file.
    * Save: loads satellite parameters into a .rcp file.
* Calculate: runs the link performance calculation.

![multi point menu](..\images\multi_ant_sz_calc.png)

#### Outputs

A progress bar will appear when the process is started. When the process is completed, the progress bar will 
disappear, and a 'Complete!' message will show up. After that, the user can see the .csv output file in **results** folder.

## Save/load dialog boxes

When every save/load/export button is clicked, a dialog box will open with file path, name and type as options.

![dialog_save](..\images\dialog_save.png)

![dialog_load](..\images\dialog_load.png)

Trying to load a different type of file extension might crash the software.

## File types

For file input examples, please check **inputs_examples** folder.

* **.sat** - satellite characteristics file
* **.rcp** - reception characteristics file
* **.gsp** - ground station characteristics file
* **.csv** - list calculation functions input/output format

## Help


