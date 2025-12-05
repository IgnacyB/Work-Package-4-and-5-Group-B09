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
    v_cruise = case[1]
    mass_aircraft =  case[2]
    load_factor = case[3]
    rho = case[4]
    mass_fuel = case[5]

    # set per-case operating conditions in the module (no circular import)
    load_calculations.set_operating_conditions(v_cruise, mass_aircraft, load_factor, rho, mass_fuel)

    M_case = (load_calculations.M())[0]
    T_case = (load_calculations.T())[0]
    Bending_moment_list.append(M_case)
    Torsion_list.append(T_case)

print("Load cases analysed completely.")
max_bending_moment = max(Bending_moment_list)
max_torsion = max(Torsion_list)
min_bending_moment = min(Bending_moment_list)
min_torsion = min(Torsion_list)
print("Maximum positive Bending Moment across load cases:", max_bending_moment, "[Nm], load case:", Load_cases_list[Bending_moment_list.index(max_bending_moment)][0])
print("Maximum positive Torsion across load cases:", max_torsion, "[Nm], load case:", Load_cases_list[Torsion_list.index(max_torsion)][0])
print("Maximum negative Bending Moment across load cases:", min_bending_moment, "[Nm], load case:", Load_cases_list[Bending_moment_list.index(min_bending_moment)][0])
print("Maximum negative Torsion across load cases:", min_torsion, "[Nm], load case:", Load_cases_list[Torsion_list.index(min_torsion)][0])

# Plot internal-load diagrams for the most constraining cases
import internal_load_diagrams as ild
import Deflection_Graphs as defl
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
    v_cruise = case[1]
    mass_aircraft =  case[2]
    load_factor = case[3]
    rho = case[4]
    mass_fuel = case[5]
    
    # configure load_calculations for this case and precompute grid for speed
    load_calculations.set_operating_conditions(v_cruise, mass_aircraft, load_factor, rho, mass_fuel)

    # build descriptive title indicating why this case is critical
    reasons = []
    if idx == idx_max_b:
        reasons.append("maximum positive bending moment")
    if idx == idx_min_b:
        reasons.append("maximum negative bending moment")
    if idx == idx_max_t:
        reasons.append("maximum positive torsion")
    if idx == idx_min_t:
        reasons.append("maximum negative torsion")
    reason_str = "; ".join(reasons) if reasons else "critical case"

    title = f"Load case {case[0]} — {reason_str}"
    print(f"Plotting internal loads for case {case[0]} (index {idx}): {reason_str}")
    ild.plot_internal_loads(title=title)
    # pass the descriptive title to deflection plots so they indicate the load case
    defl.plot_lateral_deflection(title=title)
    defl.plot_twist_distribution(title=title)

from internal_load_diagrams import plot_all_cases_internal_distributions

# Example usage: plot all cases
if __name__ == "__main__":
    # call after Load_cases_list and load_calculations are ready
    plot_all_cases_internal_distributions(Load_cases_list, load_calculations)