
from internal_load_diagrams import plot_internal_loads
plot_internal_loads()

#=================Loadcases extraction===================#
path = "loadcases.txt"
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
            except Exception:
                continue
            cases.append([case, speed, weight, load_factor, density])
    return cases

print(parse_loadcases(path))






