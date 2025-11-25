def wing_geometry(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    line40_values = lines[39].split()   
    line48_values = lines[47].split()  

    cr = line40_values[3]
    b = 2*line48_values[1]
    ct = line48_values[3]

    return cr, b, ct