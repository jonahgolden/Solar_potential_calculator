Solar Calculator
Jonah Golden, 2015-11-08

10-Minute Plan: This plan is meant to give readers and contributors a general layout of the code and documents contained within this project.

The overarching goal is to make a function that provides solar panel energy generation potential for any solar panel array, anywhere on earth.

The current iteration is the function solar_panel_calc.py which is located in the src folder of this project. This function takes latitude, longitude, area of installed panels (m^2), and the efficiency of those panels as inputs. It returns the calculated energy generation potential over one year and saves a graph of the predicted average energy generation over one year as outputs.

How to run: python solar_panel_calc.py Latitude Longitude Area Panel_Efficiency

Assumptions: There are no buildings, trees, or mountains that block sun at any point during the day.

Inputs: 1. Latitude must be a number from -90 through 90. Negative latitudes indicate southern hemisphere, while positive latitudes indicate northern hemisphere.
2. Longitude must be a number from -180 through 180. Negative longitudes indicate
western hemisphere, while positive longitudes indicate eastern.
3. Area must be a number.  It is the number of square meters of your solar panel array. One 255 watt panel is about 1.64 square meters.
4. Panel_Efficiency must be a number between 0 and 1, and indicates the efficiency of the solar panels. 0.16 is currently standard, but some panels have efficiencies of up to 0.3.

Outputs: 1. Average energy generation for a year in Kilowatt hours (kWh).
2. Graph of average energy generation over a year, saved in the results directory.

Another function located in the src folder of this project is called solar_power_calc.py. It calculates the power (w) the sun is radiating on one square meter of the earth when it is sunny in any location in the world at any time.

How to run: python solar_power_calc.py Day_of_year, Latitude, Hour_of_Day

Assumptions: There is no cloud cover.

Inputs: 1. Day_of_year must be a whole number from 1 through 365.
2. Latitude must be a number from -90 through 90. Negative latitudes indicate southern hemisphere.
3. Hour_of_Day must be a number from 0 through 24.

Output: Power in watts

Any plots or tables that come from analysis will be contained in the results directory.

Final manuscripts can be found in the doc directory.


