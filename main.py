
mass_aircraft = int(input("Enter the mass of the aircraft in kg: "))
v_cruise = int(input("Enter the flight speed in m/s: "))
rho_air = float(input("Enter the air density in kg/m^3: "))
mass_fuel = int(input("Enter the fuel mass in kg: "))
mass_wing = int(input("Enter the wing mass in kg: "))


# set runtime inputs into load_calculations BEFORE importing plotting (breaks circular import)
from load_calculations import set_runtime_inputs
set_runtime_inputs(v_cruise, mass_aircraft, rho_air, mass_fuel, mass_wing)

# now import the plotting function and run it
from internal_load_diagrams import plot_internal_loads
plot_internal_loads()









