import numpy as np

def load_wire_currents(feko_filename):
    """
    Reads a feko .out file and extracts the wire currents. The wire currents
    are stored in a dictionary dataset. 
    
    arguments:
        feko_filename

    returns: 
        dataset - list of {Frequency, Data}(see dictionary layout below)

    Data = {Segment, X, Y, Z, Current_X, Current_Y, Current_Z}
    Frequency - frequency in Hz
    Segment - Wire segment number
    X,Y,Z - spatial coordinates in m
    Current_X,Y,Z - complex currents in each axis
    """

    # Initialise logic
    found_currents_start = False

    # Create storage structures
    frequency = 0
    dataset = []


    # Open file and start reading
    f = open(feko_filename,'r')

    # Loop over every row in the file
    with open(feko_filename) as f:
        for line in f:
            # Filter empty strings
            row_raw = line.split(' ')
            row = list(filter(None, row_raw))

            # Read the currents into the current frequency object
            if found_currents_start and len(row) != 1:
                seg_no.append(int(row[0]))
                pos_x.append(float(row[1]))
                pos_y.append(float(row[2]))
                pos_z.append(float(row[3]))
                curr_x.append(float(row[4])*np.exp(1j*np.pi/180*float(row[5])))
                curr_y.append(float(row[6])*np.exp(1j*np.pi/180*float(row[7])))
                curr_z.append(float(row[8])*np.exp(1j*np.pi/180*float(row[9])))

            # Logic to detect certain parts of the file
            if "Frequency" in row and frequency != float(row[5]):
                frequency = float(row[5])
                print("Reading freq: "+str(frequency/1e6)+" MHz", end="\r")
            if "x/m" in row and len(row) == 10:
                found_currents_start = True
                 # Create intemedietary storage variables
                seg_no = []
                pos_x = []
                pos_y = []
                pos_z = []
                curr_x = []
                curr_y = []
                curr_z = []
            elif found_currents_start and len(row) == 1:
                found_currents_start = False

                # Create the data block and append it to our dataset
                data = {"Segment":np.array(seg_no), 
                        "X":np.array(pos_x), 
                        "Y":np.array(pos_y), 
                        "Z":np.array(pos_z),
                        "Current_X":np.array(curr_x), 
                        "Current_Y":np.array(curr_y), 
                        "Current_Z":np.array(curr_z)}
                dataset.append({"Frequency":frequency, "Data":data.copy()})


                frequency == None

    return dataset