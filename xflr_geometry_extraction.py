def wing_geometry(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    line40_values = lines[39].split()   
    line48_values = lines[47].split()  

    cr = float(line40_values[3])
    b = 2*float(line48_values[1])
    ct = float(line48_values[3])

    return b, cr, ct