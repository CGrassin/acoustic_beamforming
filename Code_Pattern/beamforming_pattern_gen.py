#!/usr/bin/env python3

"""This module plots and outputs beamforming pattern.

Example usage: python3 beamforming_pattern_gen.py

Author: CGrassin (http://charleslabs.fr)
License: MIT
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import argparse

def dBtoLinear(db):
    """Converts a log value to a linear value."""
    return 10**(db/20);

def lineartodB(lin):
    """Converts a log value to a linear value."""
    return 20*math.log10(lin);

# Get amplitude law
def get_amplitude_law(N, law = 'constant', minAmp = 1):
    """Computes an amplitude law given N (number of elements),
    law (type of law) and minAmp (minimum amplitude).
    """
    amp_law = [];
    
    for n in range(N):
        if law == 'constant':
            amp_law.append(1);
        elif law == 'linear':
            beta = 0 if N%2!=0 else (1-minAmp)/(N-1)
            amp_law.append((minAmp-1-beta) * 2/(N-1) * abs(n - (N-1) / 2) + 1 + beta);
        elif law == 'log_linear':
            beta = 0 if N%2!=0 else (1-lineartodB(minAmp))/(N-1)
            amp_law.append(dBtoLinear((lineartodB(minAmp)-beta) * 2/(N-1) * abs(n-(N-1)/2) + beta));
        elif law == 'poly2':
            beta = 0 if N%2!=0 else (1-minAmp)/(N-1)
            amp_law.append((minAmp-1-beta) * (2/(N-1))**2 * (n-(N-1)/2)**2 + 1 + beta**2);
        elif law == 'poly3':
            beta = 0 if N%2!=0 else (1-minAmp)/(N-1)
            amp_law.append((minAmp-1-beta) * (2/(N-1))**3 * abs(n-(N-1)/2)**3 + 1 + beta**3);    
    return amp_law;

# Get phase law
def get_phase_law(N, d, wavelength, phi):
    """Computes a phase law given N (number of elements),
    d (spacing between elements in m), wavelength (in m)
    and phi (beam steering angle).
    """
    phase_law = [];
    for n in range(N):
        phase_law.append(-2 * math.pi * n * d / wavelength * math.sin(math.radians(phi)));
    return phase_law;   
    
# Compute antenna pattern
def get_pattern(N, d, wavelength, phi, amplitude_law, minimum_amplitude, logScale=True):
    """Computes an array pattern given N (number of elements),
    d (spacing between elements in m), wavelength (in m),
    phi (beam steering angle), amplitude_law (type of law)
    and minAmp (minimum amplitude).
    """
    # Compute phase and amplitudes laws
    amp_law = get_amplitude_law(N, amplitude_law, minimum_amplitude);
    phase_law = get_phase_law(N, d, wavelength, phi);
    
    theta = np.arange(-90,90,0.1);
    mag = [];
    for i in theta:
        im=0; re=0;
        # Phase shift due to off-boresight angle
        psi = 2 * math.pi * d / wavelength * math.sin(math.radians(i));
        # Compute sum of effects of elements
        for n in range(N):
            im += amp_law[n] * math.sin(n*psi + phase_law[n]);
            re += amp_law[n] * math.cos(n*psi + phase_law[n]);
        magnitude = math.sqrt(re**2 + im**2)/N
        if logScale:
            magnitude = 20*math.log10(magnitude)
        mag.append(magnitude)
        
    return theta, mag, amp_law, phase_law

def plot_pattern(theta, mag, amp_law, phase_law, polar=False, output_file=None):
    """Plots a magnitude pattern, amplitude law and phase law.
    Optionnally, it can export the pattern to output_file. 
    """
    # Plot pattern
    if polar:
        ax = plt.subplot(131, polar=True)
        ax.plot(math.radians(theta), mag)
        ax.set_theta_zero_location("N")
        ax.set_thetalim(-math.pi/2,math.pi/2)
    else:
        ax = plt.subplot(131)
        ax.plot(theta,mag)
        ax.grid(True)
        ax.set_xlim([-90, 90])
    plt.ylim(top=0)
    plt.title("Antenna pattern");
    
    # Plot amplitude law
    ax = plt.subplot(132)
    ax.plot(range(len(amp_law)), amp_law, marker='o');
    ax.set_ylim([0,1])
    plt.title("Amplitude law");
    print("Amplitude law:")
    print(amp_law)
    
    # Plot phase law
    ax = plt.subplot(133)
    plt.title("Phase law");
    ax.plot(range(len(phase_law)),np.rad2deg(phase_law), marker='o')
    print("Phase law:")
    print(phase_law)
    
    # Show and save plot
    plt.show();
    if output_file is not None:
        plt.savefig(output_file + '.png')
        np.savetxt(output_file + '.txt', np.transpose([theta,mag]),
                   delimiter='\t', header="Angle [deg]\tMagnitude [dB]")

def main():
    # TODO allow arbitrary amp and phase laws as args
    parser = argparse.ArgumentParser(description="Generates BF pattern.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n","--number-elements", type=int, default=12,
                        help="number of elements")
    parser.add_argument("-c","--wave-celerity", type=float, default=340,
                        help="celerity of the wave in m/s (3.00E8 for light in vaccum, 340 for sound in air)")
    parser.add_argument("-d","--elements-spacing", type=float, default=0.15,
                        help="spacing between the elements in m")
    parser.add_argument("-f","--frequency", type=float, default=1000,
                        help="waveform frequency in Hz")
    parser.add_argument("-a","--steering-angle", type=float, default=0,
                        help="beam steering angle in deg")
    parser.add_argument("--amplitude-law", choices=['constant', 'linear', 'log_linear', 'poly2', 'poly3'],
                        default='log_linear', help="amplitude law type")
    parser.add_argument("--minimum-amplitude", type=float,
                        default=dBtoLinear(-5), help="minimum normalized amplitude of the law")
    parser.add_argument("--polar", action="store_true",
                        help="display beam in polar graph")
    parser.add_argument("--log-scale", action="store_false",
                        help="display pattern in logarithmic scale")
    parser.add_argument("-s","--save-output", action="store_true",
                        help="save the output pattern and data in current folder")
    args = parser.parse_args();
    
    # Check parameters
    if args.number_elements <= 0:
         raise parser.error('The number of elements must be a positive integer.')
    if args.wave_celerity <= 0:
         raise parser.error('The wave celerity must be positive.')
    if args.elements_spacing <= 0:
         raise parser.error('The elements spacing must be positive.')
    if args.frequency <= 0:
         raise parser.error('The frequency must be positive.')
    if args.steering_angle < -90 or args.steering_angle > 90:
         raise parser.error('The steering angle must be in interval [-90;90].')
    if args.minimum_amplitude < 0 or args.minimum_amplitude > 1:
         raise parser.error('The minimum amplitude must be in interval [0;1].')
         
    # Parameters
    N = args.number_elements; # Elements
    c = args.wave_celerity; #m/s
    d = args.elements_spacing; #m
    f = args.frequency; #Hz
    phi = args.steering_angle; #deg
    polar = args.polar; #True=polar patter, False=cartesian pattern
    logScale = args.log_scale; #True=output in dB, False=linear output
    amplitude_law = args.amplitude_law; #Amplitude law type
    minimum_amplitude = args.minimum_amplitude; #normalized amplitude
    
    output_file = 'pattern_' + str(N) + '_' + amplitude_law if args.save_output else None;
    wavelength = c/f; #m

    theta, mag, amp_law, phase_law = get_pattern(N, d, wavelength, phi, amplitude_law, minimum_amplitude, logScale)
    plot_pattern(theta, mag, amp_law,phase_law,polar,output_file=output_file)

if __name__ == '__main__':
    main()
