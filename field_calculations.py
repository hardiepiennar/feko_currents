"""
Functions to calculate field data using currents.

Hardie Pienaar
Cavendish Lab
March 2018
"""

import numpy as np

def calc_farfield(currents, calc_coords):
    """
    Calculates the electric field at requested points given a dictionary
    containing data on the currents.

    arguments:
        currents - {"Current":current, "Position:":coordinate)}
        current - Nx3 numpy array of complex currents where N is the number of 
                  currents
                  current[N] = [current_x, current_y, current_z] 
                  units in A*m
        coordinate - Nx3 numpy array of the current positions
                     coordinate[N] = [pos_x, pos_y, pos_z]
                     units in m

        calc_coords - Kx2 numpy array where K is the number of requested
                      field coordinates [theta, phi] 
                      theta - angle from z in rad
                      phi - angle from +x towards +y in rad
        
    returns:
        {"Coordinates":coords, "E_field":e_field}
        coords - calc_coords
        e_field - Kx2 numpy array of complex field values [e_theta, e_phi]
                  e_theta - E-field in theta direction V/m
                  e_phi - E-field in phi direction V/m
    """
    # TODO: Write this function
    print("Error: Not implemented!")
    assert(False)


def calc_gain(farfield):
    """
    Write documentation
    """
    print("Error: Not implemented!")
    assert(False)

def calc_e_field_from_wire_currents(farfield_coords, wire_current_dataset):
  """
  Calculates the e-field at the given fieldpoints from the currents contained
  in the given wire current dataset. The function returns a dataset with 
  e-field and corosponding spherical coordinate values.

  arguments:
      field_points - Nx2 numpy array of [theta, phi] coordinates where fields
                     need to be calculated
      current_dataset - dictionary created using feko_outfile wire current  
                        loading function. 
                        {Frequency, Data}   
  returns:
    Farfield - dictionary of the form {Theta, Phi, E_Theta, E_Phi} where
               Theta and Phi are the given farfield coordinates.
               E_Theta and E_Phi are the electric fields in V/m
  """
  # Calculate some general variables
  mu = 4*np.pi*1e-7
  f = wire_current_dataset["Frequency"]
  w = 2*np.pi*f

  # Lets move the data into more legible variables
  no_wire_currents = len(wire_current_dataset["Data"]["Segment"])
  pos_x = wire_current_dataset["Data"]["X"]
  pos_y = wire_current_dataset["Data"]["Y"]
  pos_z = wire_current_dataset["Data"]["Z"]
  pos = np.array([pos_x, pos_y, pos_z]).transpose()
  currents_x = wire_current_dataset["Data"]["Current_X"]
  currents_y = wire_current_dataset["Data"]["Current_Y"]
  currents_z = wire_current_dataset["Data"]["Current_Z"]
  segment_length = wire_current_dataset["Data"]["Length"]
  theta = farfield_coords[:, 0]
  phi = farfield_coords[:, 1]

  # Create a storage structure for the fields [E_theta, E_phi]
  E_theta = np.zeros(farfield_coords.shape[0])
  E_phi = np.zeros(farfield_coords.shape[0])

  # Position factor 
  phase_offsets = calc_position_phase_offsets(pos, farfield_coords, f)
  pf = np.exp(1j*phase_offsets)

  # Add the contribution of every current to the e-field at given coords
  for i in range(no_wire_currents):
      # General scaling factor
      scaling_factor = (segment_length[i]*1j*w*mu)/(4*np.pi)

      # Add x-oriented currents
      strength = currents_x[i]*scaling_factor*pf[:,i]
      E_theta = E_theta + strength*-1*np.cos(theta)*np.cos(phi)
      E_phi = E_phi + strength*np.sin(phi)

      # Add y-oriented currents
      strength = currents_y[i]*scaling_factor*pf[:,i]
      E_theta = E_theta + strength*-1*np.cos(theta)*np.cos(phi+np.pi/2)
      E_phi = E_phi + strength*np.sin(phi+np.pi/2)

      # Add z-oriented currents
      strength = currents_z[i]*scaling_factor*pf[:,i]
      E_theta = E_theta + strength*-1*np.sin(theta)
      E_phi = E_phi + 0

  return {"Theta":theta, "Phi":phi, "E_Theta":E_theta, "E_Phi":E_phi}


def calc_position_phase_offsets(positions, farfield_coords, frequency):
  """
  Calculates the phase offset with reference to the (0,0) position for every current
  to every requested farfield coordinate.

  arguments:
    positions - [Cx3] numpy array of [x,y,z] positions for the currents in m
    farfield_coords - [Nx2] numpy array of [theta, phi] coordinates in the farfield in radians
    frequency - frequency for phase calculation

  returns:
    phase_offsets - [NxC] numpy array of phase offsets where N is the number of farfied coords
                    and C the number of currents. Unit is radians
  """ 
  # Calculate the directions from the origin to the farfield coordinates
  theta = farfield_coords[:, 0]
  phi = farfield_coords[:, 1]
  coord_vector = np.array([np.sin(theta)*np.cos(phi), 
                           np.sin(theta)*np.sin(phi), 
                           np.cos(theta)])
  coord_vector = coord_vector.transpose()

  # Calculate the relative position in the direction of the farfield coord 
  dist_in_coord_direction = np.zeros((farfield_coords.shape[0], positions.shape[0]))
  for fc in range(farfield_coords.shape[0]):
    for p in range(positions.shape[0]):
      dist_in_coord_direction[fc,p] = np.dot(coord_vector[fc,:], positions[p,:])

  # Calculate the phase offset
  lambd = 299792458/frequency
  k = (2*np.pi)/lambd
  phase_offsets = dist_in_coord_direction*k

  return phase_offsets

def gen_gridlist_from_values(theta, phi):
  """
    Generates farfield list of coordinates at the given theta phi values

    arguments:
      theta - [Nx1] numpy array of angle values in radians
      phi -   [Nx1] numpy array of angle values in radians

    returns:
      gridlist - [Nx2] numpy array of coordinates for the given theta phi values
  """
  # Create grid of coordinates
  theta_grid, phi_grid = np.meshgrid(theta, phi)
  # Flatten the grid to form lists of farfield theta and phi coordinates
  theta_coords = theta_grid.flatten()
  theta_coords = theta_coords.reshape(len(theta_coords),1)
  phi_coords = phi_grid.flatten()
  phi_coords = phi_coords.reshape(len(phi_coords),1)
  # Create a Nx2 array of theta phi farfield coordinates where N is the number of farfield points
  gridlist = np.zeros((theta_coords.shape[0], theta_coords.shape[1]*2)) 
  gridlist[:, 0] = theta_coords[:,0]
  gridlist[:, 1] = phi_coords[:,0]

  return gridlist