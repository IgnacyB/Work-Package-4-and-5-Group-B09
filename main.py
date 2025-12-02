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
import load_calculations

for case in Load_cases_list:
    mass_aircraft = case[2] * case[3]
    v_cruise = case[1]
    rho = case[4]
    mass_fuel = case[5]

    # set per-case operating conditions in the module (no circular import)
    load_calculations.set_operating_conditions(mass_aircraft, v_cruise, rho, mass_fuel)

    # PRECOMPUTE grid for this case to make M/T/V queries fast
    load_calculations.precompute_internal_loads(n=600)  # increase n for accuracy if needed

    M_case = load_calculations.M(0)
    T_case = load_calculations.T(0)
    Bending_moment_list.append(M_case)
    Torsion_list.append(T_case)

print("Load cases analysed completely.")
max_bending_moment = max(Bending_moment_list)
max_torsion = max(Torsion_list)
min_bending_moment = min(Bending_moment_list)
min_torsion = min(Torsion_list)
print("Maximum Bending Moment across load cases:", max_bending_moment, "[Nm], load case:", Load_cases_list[Bending_moment_list.index(max_bending_moment)][0])
print("Maximum Torsion across load cases:", max_torsion, "[Nm], load case:", Load_cases_list[Torsion_list.index(max_torsion)][0])
print("Minimum Bending Moment across load cases:", min_bending_moment, "[Nm], load case:", Load_cases_list[Bending_moment_list.index(min_bending_moment)][0])
print("Minimum Torsion across load cases:", min_torsion, "[Nm], load case:", Load_cases_list[Torsion_list.index(min_torsion)][0])

# Plot internal-load diagrams for the most constraining cases
import internal_load_diagrams as ild
idx_max_b = Bending_moment_list.index(max_bending_moment)
idx_max_t = Torsion_list.index(max_torsion)
idx_min_b = Bending_moment_list.index(min_bending_moment)
idx_min_t = Torsion_list.index(min_torsion)
critical_idxs = []
for idx in (idx_max_b, idx_max_t, idx_min_b, idx_min_t):
    if idx not in critical_idxs:
        critical_idxs.append(idx)

for idx in critical_idxs:
    case = Load_cases_list[idx]
    mass_aircraft = case[2] * case[3]
    v_cruise = case[1]
    rho = case[4]
    mass_fuel = case[5]

    # configure load_calculations for this case and precompute grid for speed
    load_calculations.set_operating_conditions(mass_aircraft, v_cruise, rho, mass_fuel)
    load_calculations.precompute_internal_loads(n=600)

    print(f"Plotting internal loads for case {case[0]} (index {idx})")
    ild.plot_internal_loads(title=f"Load case {case[0]}")