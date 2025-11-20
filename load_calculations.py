#Importing necessary constants
from constants import g, rho_air

#=========WEIGHT CALCULATIONS=========#

#WEIGHT DISTRIBUTION (HALF OF SPAN)
def weight_distribution(mass_wing, span, y_0):
    A = 3 / 2 * mass_wing*g / 2 / (y_0**3-(y_0 - span/2)**3)

    def w_dist(y):
        return A * (y_0 - y)**2
    
    return w_dist

    