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
import field_calculations as fc

# Global variables
filename = "test_models/dipole.out"

# Load wire currents from our dataset
print("Loading currents...")
wire_currents = feko_outfile.load_wire_currents(filename)

# Load farfields to test against
farfields = feko_outfile.load_farfield(filename)

# Plot the currents on the x-aligned dipole
if False:
    pos_x = wire_currents[0]["Data"]["X"]
    current_x = wire_currents[0]["Data"]["Current_X"]
    plt.figure()
    plt.plot(pos_x, np.real(current_x), label="Real")
    plt.plot(pos_x, np.imag(current_x), label="Imag")
    plt.grid(True)
    plt.legend()


# Plot the farfield
if False:
    plt.figure()
    plt.scatter(farfields[0]["Data"]["Theta"], farfields[0]["Data"]["Phi"], 
        c=np.abs(farfields[0]["Data"]["E_Phi"]),s=100)
    plt.figure()
    plt.scatter(farfields[0]["Data"]["Theta"], farfields[0]["Data"]["Phi"], 
        c=np.abs(farfields[0]["Data"]["E_Theta"]),s=100)


# Calculate E-Field position_factor
# Loop over all wire segments and calculate electric field at zenith
theta = np.linspace(0,np.pi,21)
phi = np.linspace(0,0,1)

theta_grid, phi_grid = np.meshgrid(theta, phi)

# Calculate far-fields
calced_farfield = fc.calc_e_field_from_wire_currents(theta_grid, phi_grid, 
                                                     wire_currents[0])

if False:
    plt.figure()
    plt.contourf(theta_grid, phi_grid, np.abs(calced_farfield["E_Theta"]))
    plt.figure()
    plt.contourf(theta_grid, phi_grid, np.abs(calced_farfield["E_Phi"]))

print(theta_grid)
theta_c = theta_grid[0]
e_theta_c = np.abs(calced_farfield["E_Theta"][0])
theta_s = farfields[0]["Data"]["Theta"][farfields[0]["Data"]["Phi"] == 0]
e_theta_s = np.abs(farfields[0]["Data"]["E_Theta"][farfields[0]["Data"]["Phi"] == 0])

plt.figure()
plt.plot(theta_c, e_theta_c)
plt.plot(theta_s, e_theta_s)
plt.show()