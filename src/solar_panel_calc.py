# Jonah Golden, 2015-11-18
# For a solar panel array defined by your inputs, this script returns how much energy it
# will generate in a year on average, saves a graph of your average energy generation over
# one year.
# How to run: python solar_panel_calc.py Latitude Longitude Area Panel_Efficiency
# Assumptions: There are no buildings, trees, or mountains that block sun at any point during
# the day
# Inputs: 1) Latitude must be a number from -90 through 90. Negative latitudes indicate
#			 southern hemisphere, while positive latitudes indicate northern hemisphere.
#		  2) Longitude must be a number from -180 through 180. Negative longitudes indicate
#			 western hemisphere, while positive longitudes indicate eastern.
#		  3) Area must be a number.  It is the number of square meters of your solar
#		     panel array. One average 255 watt panel is about 1.64 square meters.
#		  4) Panel_Efficiency must be a number between 0 and 1, and indicates the efficiency
#			 of the solar panels.  0.16 is standard.
# Output: 1) Average energy generation for a year in Kilowatt hours (kWh).
#		  2) Graph of average energy generation over a year, saved in the results directory.

# Import Libraries
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab


# Defining Variables
latitude = float(sys.argv[1])
longitude = float(sys.argv[2])
area = float(sys.argv[3])
panel_efficiency = float(sys.argv[4])

# Load and clean cloud data
cloud_dat = pd.read_csv('../data/weather.txt',sep='\s+')
cloud_dat = cloud_dat.transpose()
cloud_dat = cloud_dat.reset_index()
cloud_dat.columns=['cloud_ratio']
clouds = pd.read_excel('../data/blank_weather.xlsx',sep='\s+')
clouds['cloud_ratio'] = cloud_dat['cloud_ratio']


def main():

	# Using ThetaD_list and variables, create list of solar panel output without clouds
	Watts = Solar_Energy_Calculator(latitude, panel_efficiency, area)

	# Use input coordinates to find radiation for given location
	radiation = find_sun(latitude,longitude)

	# Apply radiation for specific location to Watts without cloud data to make final
	# data
	final = apply_clouds(Watts,radiation)
	kWh = sum(final)/1000
	final = pd.DataFrame(final)
	final = final.reset_index()
	final.columns=['Day','Power']
	final['Day'] = final['Day']/24

	# Plot
	plot(final['Day'],final['Power'])

	# Print
	print('This solar panel array will generate an average of',kWh,'kWh every year')

def Solar_Energy_Calculator(latitude, panel_efficiency, area):
    '''This function calculates the energy that can be generated in any given place in the
    world over one year sans clouds.
    Inputs: latitude, panel_efficiency (a number between 0 and 1), and area (of solar panels
    in square meters).
    Output: List of average watts generated every hour for the year.'''

    # Define some constants
    radians = np.pi/180*latitude
    S0 = 1367.63 # Solar constant
    Dis_n = [0,1,2]
    Dis_an = [1.00011,0.034221,0.000719]
    Dis_bn = [0,0.00128,0.000077]
    Dec_n = [0,1,2,3]
    Dec_an = [0.006918,-0.399912,-0.006758,-0.002697]
    Dec_bn = [0,0.070257,0.000907,0.00148]
    Atm = .75 # Proportion of solar energy that makes it to the earth's surface
    radiation_through_clouds = 0.7 # Proportion of solar energy the gets through clouds

    # Create some variables and lists
    Hours = [12,11,10,9,8,7,6,5,4,3,2,1,0,1,2,3,4,5,6,7,8,9,10,11] # A list of all the hours of the day
    Solar_Flux = 0 # Energy generated from given area of solar panels in one hour
    Watts_Every_Hour = [] # A list that will become the Wh/m^2 every hour for a year
    kWh = 0 # A number that will become the total kWh in one place in one year.

    # Make a list of ThetaD values for each day of the year
    year = list(range(1,366))
    ThetaD_list = []
    for i in year:
        ThetaD_list.append((2*np.pi*i)/365)

    # Make Distance and Dec_radians lists for each day of the year
    for i in ThetaD_list:
        # Calculate the Distance
        Dis1 = Dis_an[0]*np.cos(Dis_n[0]*i)+Dis_bn[0]*np.sin(Dis_n[0]*i)
        Dis2 = Dis_an[1]*np.cos(Dis_n[1]*i)+Dis_bn[1]*np.sin(Dis_n[1]*i)
        Dis3 = Dis_an[2]*np.cos(Dis_n[2]*i)+Dis_bn[2]*np.sin(Dis_n[2]*i)
        Distance = Dis1+Dis2+Dis3

        # Calculate the Declination
        Dec1 = Dec_an[0]*np.cos(Dec_n[0]*i)+Dec_bn[0]*np.sin(Dec_n[0]*i)
        Dec2 = Dec_an[1]*np.cos(Dec_n[1]*i)+Dec_bn[1]*np.sin(Dec_n[1]*i)
        Dec3 = Dec_an[2]*np.cos(Dec_n[2]*i)+Dec_bn[2]*np.sin(Dec_n[2]*i)
        Dec4 = Dec_an[3]*np.cos(Dec_n[3]*i)+Dec_bn[3]*np.sin(Dec_n[3]*i)
        Dec_radians = Dec1+Dec2+Dec3+Dec4
        Dec_degrees = (np.degrees(Dec_radians))

        # Calculate the Hour Angle, CSZA, and Solar Flux for each hour of the day
        for i in Hours:
            Hour_angle = np.radians(i*15)
            CSZA = (np.sin(radians)*np.sin(Dec_radians)) + (np.cos(radians)*np.cos(Dec_radians)*np.cos(Hour_angle))
            if CSZA < 0:
                CSZA = 0
            Solar_Flux = (S0)*Distance*CSZA*Atm*panel_efficiency*area

            # Create a list of the watts being generated every hour
            Watts_Every_Hour.append(Solar_Flux)
    return(Watts_Every_Hour)

def find_sun(lat,long):
    '''This function finds the ratio of clouds for any lattitude and longitude and converts
    it into the ratio of radiation that reaches the earth.
    inputs: lattitude, longitude
    output: radiation ratio'''
    x = clouds.loc[(clouds['lattitude'] <= lat) & (clouds['lattitude'] > (lat-2.5)) & (clouds['longitude'] <= long) & (clouds['longitude'] > (long-2.5))]
    radiation_ratio = 1-((float(x.iloc[0,2])*0.6)/100)
    return(radiation_ratio)

def apply_clouds(watts,radiation):
    '''This function takes a list of watts without clouds and radiation ratio due to clouds
    and gives you a list of the real solar generation prediction.'''
    energy = []
    for i in watts:
        energy.append(i*radiation)
    return(energy)


def plot(x,y):
	# Format graph
	plt.title('Power Output',fontsize=24)
	plt.xlim(0,365)
	plt.ylabel('Average Power Generation (Watts)',fontsize=16)
	plt.xlabel('Day of Year',fontsize=16)
	# Plot data
	plt.plot(x,y)
	# Save plot
	plt.savefig('../results/Power_Graph.pdf')
	# Show plot
	#plt.show()

main()
