"""
Functions to calculate field data using currents.

Hardie Pienaar
Cavendish Lab
March 2018
"""

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