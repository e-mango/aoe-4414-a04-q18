# eci_to_ecef.py
#
# Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km
#  Text explaining script usage
# Parameters:
#  year: year of the time instant
#  month: month of the time instant
#  day: day of the time instant
#  hour: hour of the time instant
#  minute: minute of the time instant
#  second: second of the time instant
#  eci_x_km: x component of ECI frame in km
#  eci_y_km: y component of ECI frame in km
#  eci_z_km: z component of ECI frame in km
#
# Output:
#  Prints the x , y , z components of the ECEF frame in km
#
# Written by Evan Schlein
# Other contributors: None

import math # math module
import sys # argv
import numpy as np

# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456
w = 7.292115e-5

# initialize script arguments
year = float('nan')     # year of the time instant
month = float('nan')    # month of the time instant
day = float('nan')      # day of the time instant
hour = float('nan')     # hour of the time instant
minute = float('nan')   # minute of the time instant
second = float('nan')   # second of the time instant
eci_x_km = float('nan') # x component of ECI frame in km
eci_y_km = float('nan') # y component of ECI frame in km
eci_z_km = float('nan') # z component of ECI frame in km


# parse script arguments
if len(sys.argv) == 10:
    year = float(sys.argv[1])
    month = float(sys.argv[2])
    day = float(sys.argv[3])
    hour = float(sys.argv[4])
    minute = float(sys.argv[5])
    second = float(sys.argv[6])
    eci_x_km = float(sys.argv[7])
    eci_y_km = float(sys.argv[8])
    eci_z_km = float(sys.argv[9])
else:
    print(
        'Usage: '
        'python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'
    )
    exit()

# write script below this line

#Calculate the Frac. Julian Date
JD = math.floor(day-32075 + 1461*(year+4800+(month-14)/12)/4 + 367*(month-2-(month-14)/12*12)/12 - 3*((year+4900+(month-14)/12)/100)/4)
JD_midnight = JD - 0.5
D_frac = ((second + 60*(minute+60*hour))/86400)
jd_frac = JD_midnight + D_frac

#Calculate the GMST Angle
T_ut1 = (jd_frac - 2451545.0)/36525
Theta_GMST_sec = 67310.54841 + (876600*60*60 + 8640184.812866)*T_ut1 + 0.093104*(T_ut1**2) + (-6.2e-6 * (T_ut1**3))
GMST_rad = (Theta_GMST_sec % 86400) * w 

# Rotate ECI to ECEF
R_z = np.array([
    [np.cos(-GMST_rad), -np.sin(-GMST_rad), 0],
    [np.sin(-GMST_rad), np.cos(-GMST_rad), 0],
    [0, 0, 1]])

ECI_vec = np.array([eci_x_km, eci_y_km, eci_z_km])

ECEF_vec = np.dot(R_z,ECI_vec)

ecef_x_km = ECEF_vec[0]
ecef_y_km = ECEF_vec[1]
ecef_z_km = ECEF_vec[2]

print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)