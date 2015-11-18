# Jonah Golden, 2015-11-18
# Take inputs and tell you how much power the sun is radiating on one square meter of the 
# earth when it is sunny in any location in the world at any time.
# How to run: python solar_power_calc.py Day_of_year, Latitude, Hour_of_Day
# Inputs: 1) Day_of_year must be a whole number from 1 through 365.
#		  2) Latitude must be a number from -90 through 90. Negative latitudes indicate
#			southern hemisphere.
#		  3) Hour_of_Day must be a number from 0 through 24.
# Output: Power in watts

# Import Libraries
import sys
import numpy as np

# Define Variables
Day_of_Year = float(sys.argv[1])
Latitude = float(sys.argv[2])
Hour_of_Day = float(sys.argv[3])

def main():
	
	# Run calculator on inputs
	watts = Solar_Power_Calculator(Day_of_Year,Latitude,Hour_of_Day)
	
	# Print output
	print('The power delivered from the sun to your location at your time with a clear sky is',watts,'watts per square meter')
	
def Solar_Power_Calculator(Day_of_Year,Latitude,Hour_of_Day):
	# Define constants for solar constant, atmosphere, distance, declination
	S0 = 1367.63
	Atm = 0.75
	Dis_n = [0,1,2]
	Dis_an = [1.00011,0.034221,0.000719]
	Dis_bn = [0,0.00128,0.000077]
	Dec_n = [0,1,2,3]
	Dec_an = [0.006918,-0.399912,-0.006758,-0.002697]
	Dec_bn = [0,0.070257,0.000907,0.00148]

	# Make some assertions about the inputs of the function.
	assert 0 < Day_of_Year <= 365, 'Day of year must be between 1 and 365.'
	assert -90 <= Latitude <= 90, 'Latitude must be between -90 and 90.'
	assert 0<= Hour_of_Day <= 24, 'Hour of day must be between 0 and 24.'

	# Hour_of_Day input is from 0 through 24, but we need hours in a different form for our 
	# calculations.
	if Hour_of_Day >= 12:
		hour = Hour_of_Day - 12
	elif Hour_of_Day < 12:
		hour = 12 - Hour_of_Day

	# Calculating Theta D
	ThetaD = (2*np.pi*Day_of_Year)/365

	# Calculating distance
	Dis1 = Dis_an[0]*np.cos(Dis_n[0]*ThetaD)+Dis_bn[0]*np.sin(Dis_n[0]*ThetaD)
	Dis2 = Dis_an[1]*np.cos(Dis_n[1]*ThetaD)+Dis_bn[1]*np.sin(Dis_n[1]*ThetaD)
	Dis3 = Dis_an[2]*np.cos(Dis_n[2]*ThetaD)+Dis_bn[2]*np.sin(Dis_n[2]*ThetaD)
	Distance = Dis1+Dis2+Dis3

	# Calculate declination
	Dec1 = Dec_an[0]*np.cos(Dec_n[0]*ThetaD)+Dec_bn[0]*np.sin(Dec_n[0]*ThetaD)
	Dec2 = Dec_an[1]*np.cos(Dec_n[1]*ThetaD)+Dec_bn[1]*np.sin(Dec_n[1]*ThetaD)
	Dec3 = Dec_an[2]*np.cos(Dec_n[2]*ThetaD)+Dec_bn[2]*np.sin(Dec_n[2]*ThetaD)
	Dec4 = Dec_an[3]*np.cos(Dec_n[3]*ThetaD)+Dec_bn[3]*np.sin(Dec_n[3]*ThetaD)
	Dec_radians = Dec1+Dec2+Dec3+Dec4

	# Calculate hour angle
	hour_angle = np.radians(hour*15)

	# Calculate radians
	radians = (np.pi/180)*Latitude

	#Calculate the Cos of Solar Zenith Angle
	CSZA = np.sin(radians)*np.sin(Dec_radians)+np.cos(radians)*np.cos(Dec_radians)*np.cos(hour_angle)# Cos Solar Zenith Angle
	# When the sun is down, CSZA is negative, but we want it to be zero (because when the sun
	# is down, it isn't radiating inn that location.
	if CSZA < 0:
		CSZA = 0
	# Calculate Energy/Area (W/m^2)
	Watts_Per_SqMeter = S0*Distance*CSZA*Atm

	return(Watts_Per_SqMeter)
	
main()