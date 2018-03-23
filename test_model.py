"""
Example code for feko current modules. Makes use of code_test_model.out to
verify our functions.

Hardie Pienaar
Cavendish
March 2018
"""

import numpy as np
import matplotlib.pyplot as plt
import feko_outfile

# Global variables
filename = "dipole.out"

# Load wire currents from our dataset
print("Loading currents...")
wire_currents = feko_outfile.load_wire_currents(filename)

# Plot the currents on the x-aligned dipole
if False:
    pos_x = wire_currents[0]["Data"]["X"]
    current_x = wire_currents[0]["Data"]["Current_X"]
    plt.figure()
    plt.plot(pos_x, np.real(current_x), label="Real")
    plt.plot(pos_x, np.imag(current_x), label="Imag")
    plt.grid(True)
    plt.legend()
    plt.show()

# Calculate E-Field 
# Loop over all wire segments and calculate electric field at zenith
E_theta = 0
E_phi = 0
mu = 4*np.pi*1e-7
f = wire_currents[0]["Frequency"]
w = 2*np.pi*f
theta = 45.1*np.pi/180
phi = 90*np.pi/180
no_wire_currents = len(wire_currents[0]["Data"]["Segment"])
currents_x = wire_currents[0]["Data"]["Current_X"]
segment_length = wire_currents[0]["Data"]["Length"]
for i in range(no_wire_currents):
    I0 = currents_x[i]
    dz = segment_length[i]
    
    sf = (I0*dz*1j*w*mu)/(4*np.pi) # Strength factor
    df = 1 # Distance factor (not used for farfield calculation)
    
    # Add x-oriented currents
    E_theta = E_theta + sf*df*-1*np.cos(theta)*np.cos(phi)
    E_phi = E_phi + sf*df*np.sin(phi)

    # Add y-oriented currents
    #TODO
    # Add z-oriented currents
    #TODO

print(E_theta)
print(E_phi)

# Loop over all rwg segments and calculate the electric field at zenith

# Add the fields together