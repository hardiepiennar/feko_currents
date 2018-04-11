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
farfield_coords = np.zeros((len(farfields[0]["Data"]["Theta"]),2))
farfield_coords[:, 0] = farfields[0]["Data"]["Theta"]
farfield_coords[:, 1] = farfields[0]["Data"]["Phi"]
print(farfield_coords.shape)

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
# Grab the currents from our dataset
pos_x = wire_currents[0]["Data"]["X"]
pos_y = wire_currents[0]["Data"]["Y"]
pos_z = wire_currents[0]["Data"]["Z"]
pos = np.array([pos_x, pos_y, pos_z]).transpose()

fc.calc_position_phase_offsets(pos, farfield_coords, wire_currents[0]["Frequency"])

# Calculate far-fields
calced_farfield = fc.calc_e_field_from_wire_currents(farfield_coords, 
                                                     wire_currents[0])

if False:
    plt.figure()
    plt.contourf(theta_grid, phi_grid, np.abs(calced_farfield["E_Theta"]))
    plt.figure()
    plt.contourf(theta_grid, phi_grid, np.abs(calced_farfield["E_Phi"]))

theta_c = calced_farfield["Theta"][calced_farfield["Phi"]==0]
e_theta_c = np.abs(calced_farfield["E_Theta"][calced_farfield["Phi"]==0])
theta_s = farfields[0]["Data"]["Theta"][farfields[0]["Data"]["Phi"] == 0]
e_theta_s = np.abs(farfields[0]["Data"]["E_Theta"][farfields[0]["Data"]["Phi"] == 0])

if False:
	plt.figure()
	plt.plot(theta_s, e_theta_s, linewidth=5, alpha=0.5, color='red')
	plt.plot(theta_c, e_theta_c, linewidth=2.5, alpha=1, color='black')
	plt.show()

# Calculate the full 3d pattern and compare with feko results
error = np.sum(np.abs(calced_farfield["E_Theta"] - farfields[0]["Data"]["E_Theta"]))

print("Checking field calculation accuracy...")
assert(error < 0.6)
print("[PASS]")
