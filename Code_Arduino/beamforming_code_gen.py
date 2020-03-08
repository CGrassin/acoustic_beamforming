#!/usr/bin/env python3

"""This module is an Arduino beamforming code generator, designed to work with
the CharlesLabs SG PCB (12 channel with M62429 for software amplitude control).
It schedules the pin toggles to achieve the frequency and beam steering angle.

The resulting code requires A328_PINS.h and FM62429.h in the same folder to be
compiled and runned on Arduino.

Example usage: python3 beamforming_code_gen.py > bf_code.ino

Author: CGrassin (http://charleslabs.fr)
License: MIT
"""

import math
import argparse

class Channel:
    """Internal class to group information on a channel."""
    def __init__(self,initStatus,deadline,pinName):
        self.deadline = deadline;
        self.status = initStatus;
        self.pinName = pinName;
    
    def toggle_pin(self,next_deadline):
        """Toggle a pin status and change to next deadline."""
        self.status = not self.status;
        self.deadline = next_deadline;
        return "_PIN_WRITE( _" + self.pinName + " , " + ("1" if self.status else "0") + " );\n";
        
# Compute antenna pattern
def generate_code(pins, c, d, phi, f):
    """Generate loop() Arduino code.
    
    :param pins: a list of pins
    :param c: wave celerity in m/s
    :param d: elements spacing in m
    :param f: frequency in Hz
    :param phi: beam steering angle in rads
    :returns: a string containing the loop() code
    """
    code = "";
    
    # Physics constants
    duty_cycle = 0.5;
    wavelength = c/f; # m
    period = 1.0 / f * 1e6; # us
    psi = 2.0 * math.pi * d * math.sin(phi) / wavelength; # rad
    psi_delta_t = psi / ( 2.0 * math.pi * f) * 1e6; # us
    
    # Sanity checks on parameters
    if len(pins) < 1:
        raise Exception("Array should contain at least one pin.");
    if c<=0 or d<=0 or f<=0:
        raise Exception("c, d and f must be > 0.");
    if d > wavelength / (1 + abs(math.sin(phi))):
        code += "/* WARNING: grating lobes will be present (reduce phi or f)! */\n";
    if 0 < psi_delta_t < 5:
        code += "/* WARNING: time between pin toggles is very short (increase phi or reduce f)! */\n";
    
    # Prepare pins array with t=0 states
    channels = [];
    for i in range(len(pins)):
        delta_t = ((i * psi_delta_t) % period + period) % period;
        # Two cases: either initially high or initially low
        if delta_t - duty_cycle * period > 0:
            channels.append(Channel(True, delta_t - duty_cycle * period, pins[i])); 
        else:
            channels.append(Channel(False, delta_t, pins[i]));
            
    # Code generation (from t=0 to t=period)
    currenttime=0;
    while currenttime < period:
        # Pin status and next deadline
        delay = channels[0].deadline;
        for i in range(len(channels)):
            # If some deadline is reached
            if channels[i].deadline <= 0:
                code += "\t" + channels[i].toggle_pin(duty_cycle*period);
            
            # Look for next smallest deadline
            delay = min(delay, channels[i].deadline);
        
        # Apply delay
        currenttime += delay;
        if round(delay) > 0:
            code += "\t" + "delayMicroseconds( "+str(round(delay))+ " );\n";
        for i in range(len(channels)):
            channels[i].deadline -= delay;
    
    return code;

def main():
    parser = argparse.ArgumentParser(description="Generates BF pattern code.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c","--wave-celerity", type=float, default=340,
                        help="celerity of the wave in m/s (3.00E8 for light in vaccum, 340 for sound in air)")
    parser.add_argument("-d","--elements-spacing", type=float, default=0.15,
                        help="spacing between the elements in m")
    parser.add_argument("--attenuation", type=int, default=20,
                        help="attenuation")
    parser.add_argument("-f","--frequency", type=float, default=750,
                        help="waveform frequency in Hz")
    parser.add_argument("-a","--steering-angle", type=float, default=0,
                        help="beam steering angle in deg")
    parser.add_argument("-p","--pins", nargs='+', default=["D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","D12","D13"],
                        help="pins list, from left to right")
    args = parser.parse_args();
    
    # Check parameters
    if args.wave_celerity <= 0:
         raise parser.error('The wave celerity must be positive.')
    if args.elements_spacing <= 0:
         raise parser.error('The elements spacing must be positive.')
    if args.frequency <= 0:
         raise parser.error('The frequency must be positive.')
    if args.steering_angle < -90 or args.steering_angle > 90:
         raise parser.error('The steering angle must be in interval [-90;90].')

    # Parameters
    c = args.wave_celerity; #m/s
    d = args.elements_spacing; #m
    f = args.frequency; #Hz
    phi = args.steering_angle; #deg
    pins = args.pins;
    def_att = args.attenuation;
    
    # Print input parameters
    print("/* Generated by beamforming_code_gen.py. Parameters:");
    print("* phi = "+str(phi)+" deg");
    print("* c = "+str(c)+" m/s");
    print("* d = "+str(d)+" m");
    print("* f = "+str(f)+" Hz");
    # Fraunhofer distance for accoustic = D^2 / (4*lambda)
    wavelength = c/f;
    print("* far_field_d = "+str((d * len(pins))**2 / wavelength / 4)+" m */\n"); 
    # Includes/Defines
    print("#include \"A328_PINS.h\"");
    print("#include \"FM62429.h\"\n");
          
    # Setup
    print("void setup() {");
    for pin in pins:
        print("\t_PIN_CONFIG_OUT( _"+pin+ " );");
    print("\t// Extra setup code");
    extra_setup_code = ("\tinitFM62429("+str(def_att)+", "+str(def_att)+", "+str(def_att)+", "+str(def_att)+", "+str(def_att)+", "+str(def_att)+", "
                                  ""+str(def_att)+", "+str(def_att)+", "+str(def_att)+", "+str(def_att)+", "+str(def_att)+", "+str(def_att)+");");
    print(extra_setup_code);
    print("}\n");
        
    # Loop
    print("void loop() {");
    print(generate_code(pins, c, d, math.radians(phi), f), end="");
    print("}");
    
if __name__ == '__main__':
    main()
