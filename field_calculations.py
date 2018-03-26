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

def calc_e_field_from_wire_currents(theta_grid, phi_grid, wire_current_dataset):
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
  currents_x = wire_current_dataset["Data"]["Current_X"]
  currents_y = wire_current_dataset["Data"]["Current_Y"]
  currents_z = wire_current_dataset["Data"]["Current_Z"]
  segment_length = wire_current_dataset["Data"]["Length"]

  E_theta = np.zeros(theta_grid.shape)
  E_phi = np.zeros(theta_grid.shape)
  

  # Add the contribution of every current to the e-field at given coords
  for i in range(no_wire_currents):
      # General scaling factor
      scaling_factor = (segment_length[i]*1j*w*mu)/(4*np.pi)

      # Position factor
      dist = np.sqrt(pos_x[i]**2 + pos_y[i]**2 + pos_z[i]**2)
      relative_position = np.array([pos_x[i], pos_y[i], pos_z[i]])/dist
      relative_position = relative_position.reshape((len(relative_position),1,1))
      print(relative_position.shape)
      relative_position = relative_position*np.ones(theta_grid.shape)
      print(relative_position.shape)
      coord_vector = np.array([np.sin(theta_grid)*np.cos(phi_grid), 
                               np.sin(theta_grid)*np.sin(phi_grid), 
                               np.cos(theta_grid)])
      dist_in_coord = np.dot(coord_vector[:,], relative_position)
      position_factor = np.exp(1j*dist_in_coord*k)
      print(position_factor)
      
      # Add x-oriented currents
      strength = currents_x[i]*scaling_factor
      E_theta = E_theta + strength*-1*np.cos(theta_grid)*np.cos(phi_grid)
      E_phi = E_phi + strength*np.sin(phi_grid)

      # Add y-oriented currents
      strength = currents_y[i]*scaling_factor
      E_theta = E_theta + strength*-1*np.cos(theta_grid)*np.cos(phi_grid+np.pi/2)
      E_phi = E_phi + strength*np.sin(phi_grid+np.pi/2)

      # Add z-oriented currents
      strength = currents_z[i]*scaling_factor
      E_theta = E_theta + strength*-1*np.sin(theta_grid)
      E_phi = E_phi + 0


  return {"Theta":theta_grid, "Phi":phi_grid, "E_Theta":E_theta, "E_Phi":E_phi}