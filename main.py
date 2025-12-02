
from internal_load_diagrams import plot_internal_loads
plot_internal_loads()

#=================Load cases extraction=================#

def parse_loadcases(path):
    import csv, re
    def to_float(s):
        s = s.replace(',', '.')
        s = re.sub(r'[^\d\.\-eE]', '', s)
        return float(s)

    cases = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if not row:
                continue
            # handle lines that came in as a single string
            parts = row if len(row) > 1 else row[0].split()
            # skip header / comment lines
            head0 = parts[0].strip().lower()
            if head0.startswith('case') or head0.startswith('//') or head0 == '':
                continue
            # require at least 6 columns (case, speed, weight, load, altitude, density)
            if len(parts) < 6:
                continue
            try:
                case = parts[0].strip()
                speed = to_float(parts[1])
                weight = to_float(parts[2])
                load_factor = to_float(parts[3])
                density = to_float(parts[5])   # skip altitude (parts[4])
                fuel = to_float(parts[6])
            except Exception:
                continue
            cases.append([case, speed, weight, load_factor, density, fuel])
    return cases

Load_cases_list = parse_loadcases('Loadcases.txt')
Bending_moment_list = []
Torsion_list = []
for case in Load_cases_list:
    mass_aircraft = case[2] * case[3]
    v_cruise = case[1]
    rho = case[4]
    mass_fuel = case[5]
    from load_calculations import M, T
    M_case = M(0)
    T_case = T(0)
    Bending_moment_list.append(M_case)
    Torsion_list.append(T_case)

max_bending_moment = max(Bending_moment_list)
max_torsion = max(Torsion_list)
print("Maximum Bending Moment across load cases:", max_bending_moment)
print("Maximum Torsion across load cases:", max_torsion)


