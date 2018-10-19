This directory is for storing all code used in this project.  It contains both my final Python Notebook, and final shell script.

Solar_Calcu.ipynb is the ipython notebook that I developed my code in.

solar_panel_calc.py calculates the energy that a solar array will generate in one year and saves a graph of the predicted average energy generation over one year.
How to run: python solar_panel_calc.py Latitude Longitude Area Panel_Efficiency
Assumptions: There are no buildings, trees, or mountains that block sun at any point during the day.
Inputs: 1. Latitude must be a number from -90 through 90. Negative latitudes indicate southern hemisphere, while positive latitudes indicate northern hemisphere.
2. Longitude must be a number from -180 through 180. Negative longitudes indicate
western hemisphere, while positive longitudes indicate eastern.
3. Area must be a number.  It is the number of square meters of your solar panel array. One average 255 watt panel is about 1.64 square meters.
4. Panel_Efficiency must be a number between 0 and 1, and indicates the efficiency of the solar panels. 0.16 is currently standard, but some panels have efficiencies of up to 0.3.
Output: 1. Average energy generation for a year in Kilowatt hours (kWh).
2. Graph of average energy generation over a year, saved in the results directory.


solar_power_calc.py calculates the power (w) the sun is radiating on one square meter of the earth when it is sunny in any location in the world at any time.
How to run: python solar_power_calc.py Day_of_year, Latitude, Hour_of_Day
Inputs: 1. Day_of_year must be a whole number from 1 through 365.
2. Latitude must be a number from -90 through 90. Negative latitudes indicate southern hemisphere.
3. Hour_of_Day must be a number from 0 through 24.
Output: Power in watts

