# Jonah Golden, 2015-11-11
# Script that 

# Import Libraries
import sys
import numpy as np
import sympy as sp
from sympy import *
x, y, z, t, Day_Of_Year  = symbols('x y z t Day_Of_Year')
import pandas as pd
from pandas import set_option # Option to restrict display
set_option('display.max_rows',15)
import matplotlib.pyplot as plt

# Defining variables
latitude = float(sys.argv[1])
longitude = float(sys.argv[2])
area = float(sys.argv[3])
panel_efficiency = float(sys.argv[4])
save_path = sys.argv[5]
	
# Defining constants
S0 = 1367.63 # Solar constant
Dis_n = [0,1,2]
Dis_an = [1.00011,0.034221,0.000719]
Dis_bn = [0,0.00128,0.000077]
Dec_n = [0,1,2,3]
Dec_an = [0.006918,-0.399912,-0.006758,-0.002697]
Dec_bn = [0,0.070257,0.000907,0.00148]
radians = (np.pi/180)*latitude
radiation_through_clouds = 0.7
Atm = .75 # Proportion of solar energy that makes it to the earth's surface

# Loading and cleaning cloud data
cloud_dat = pd.read_csv('../../data/weather.txt',sep='\s+')
cloud_dat = cloud_dat.transpose()
cloud_dat = cloud_dat.reset_index()
cloud_dat.columns=['cloud_ratio']
clouds = pd.read_excel('../../data/blank_weather.xlsx',sep='\s+')
clouds['cloud_ratio'] = cloud_dat['cloud_ratio']
	
def main():

	# Running Solar_Energy_Calculator for given inputs
	Watts = Solar_Energy_Calculator(latitude, panel_efficiency, area)
	
	
	# Calling cloud data for latitude and longitude inputs
	radiation = find_sun(latitude,longitude)
	
	# Make final data set for one year of energy production
	final = apply_clouds(Watts,radiation)
	kWh = sum(final)/1000
	
	# Plot energy production
	plot(final,save_path)
	print('This solar installation will generate', kWh, 'kWh of energy every year.')

def Solar_Energy_Calculator(latitude,panel_efficiency, area):
    '''Now I'm going to take the above function and do the same thing except make it 
    print the number of Wh in one square meter for a year.'''
    # Making Distance and Dec_radians lists for each day of the year
    # constants
    radiation_through_clouds = 0.7
    Hours = [12,11,10,9,8,7,6,5,4,3,2,1,0,1,2,3,4,5,6,7,8,9,10,11] # A list of all the hours of the day
    Solar_Flux = 0 # Energy generated from given area of solar panels in one hour
    Watts_Every_Hour = [] # A list that will become the Wh/m^2 every hour for a year
    kWh = 0 # A number that will become the total kWh in one place in one year.
    year=list(range(1,366)) # Creating list of Theta D values for one year
    ThetaD_list = []
    for i in year:
    	ThetaD_list.append((2*np.pi*i)/365)
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
        for i in Hours:
            Hour_angle = np.radians(i*15)
            CSZA = (np.sin(radians)*np.sin(Dec_radians)) + (np.cos(radians)*np.cos(Dec_radians)*np.cos(Hour_angle))
            if CSZA < 0:
                CSZA = 0
            Solar_Flux = (S0)*Distance*CSZA*Atm*panel_efficiency*area
            Watts_Every_Hour.append(Solar_Flux)
    kWh = sum(Watts_Every_Hour)/1000
    return(Watts_Every_Hour)


def find_sun(lat,long):
    '''This function finds the ratio of clouds for any latitude and longitude and converts
    it into the ratio of radiation that reaches the earth.
    inputs: latitude, longitude
    output: radiation ratio'''
    x = clouds.loc[(clouds['latitude'] <= lat) & (clouds['latitude'] > (lat-2.5)) & (clouds['longitude'] <= long) & (clouds['longitude'] > (long-2.5))]
    radiation_ratio = 1-((float(x.iloc[0,2])*0.6)/100)
    return(radiation_ratio)


def apply_clouds(watts,radiation):
    '''This function takes a list of watts without clouds and radiation ratio due to clouds
    and gives you a list of the real solar generation prediction.'''
    energy = []
    for i in watts:
        energy.append(i*radiation)
    return(energy)


def plot(plot_data,savename):
	# Plot data
	plt.plot(plot_data)
	# Save plot
	plt.savefig(savename)
	# Show plot
	#plt.show()

main()

