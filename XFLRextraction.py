
def extract_main_wing_data(filepath):
    y_span = []
    Cl = []
    Cm = []
    Cd_i = []

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Find the Cl of the whole wing
    line10 = lines[9].strip()
    CL_wing = float(line10.split("=")[1].strip())


    # Locate the "Main Wing" section
    i = 0
    while i < len(lines) and "Main Wing" not in lines[i]:
        i += 1

    # Skip the "Main Wing" line and the header line
    i += 2

    # Parse numerical table until a blank or non-numeric line is reached
    while i < len(lines):
        line = lines[i].strip()

        # Stop when reaching a blank line or next section
        if line == "" or not line[0].isdigit() and line[0] not in "-":
            break

        parts = line.split()
        if len(parts) >= 4:
            y_span.append(float(parts[0]))
            Cl.append(float(parts[3]))
            Cm.append(float(parts[7]))
            Cd_i.append(float(parts[5]))

        i += 1

    return y_span, Cl, Cm, Cd_i, CL_wing

'''
# Example usage:
file_path = "MainWing_a=10.00_v=10.00ms.txt"
y, cl, cm, cd_i = extract_main_wing_data(file_path)

print("y-span:", y)
print("Cl:", cl)
print("Cm:", cm)
print("Cd_i:", cd_i)
'''
