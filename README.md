# Acoustic Beamforming experiments

This repository contains all the ressources for my acoustic beamforming experiment using Arduino. This original article is here: WORK IN PROGRESS

Various pieces of code/ressource are sorted by folder.

## Code_Pattern

This folder contains code to compute beamforming patterns.

The main script is beamforming_pattern_gen.py. Usage: `python3 beamforming_pattern_gen.py -h` (shows the help and options)

Sample output (`python3 beamforming_pattern_gen.py -f 1000 -a 10`):
![Sample output for the beamforming pattern generator](https://raw.githubusercontent.com/CGrassin/acoustic_beamforming/master/Code_Pattern/sample_output/sample.png)

Also included is a geogebra file for uniform amplitude law pattern simulation.

## Code_Arduino

This folder contains the code generator and the libraries to program the Arduino. It computes the timing to get the proper frequncy and phase between the elements. Usage:

```sh
python3 beamforming_code_gen.py -f 1000 -a 10
```

Output: Arduino code for the generation of a 1000Hz frequency wave, steered to +10 degrees.

Note: there is also a fully working, but deprecated Java version of this script that I created prior to the python version.

## Electronics

This folder contains the 12 channels signal generator PCB based around the FM62429 chips and the Arduino Nano microcontroller board. I used the open-source EDA KiCad.

## Experiments_Data

*WORK IN PROGRESS* This folder contains the data collected for each measurement, in CSV format. The first line of each CSV file contains all information to figure out it content.
