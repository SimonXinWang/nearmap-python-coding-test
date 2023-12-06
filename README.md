# python plotting tool

## Constraints

* written in Python
* Use Python 3.11
* Use matplotlib.pyplot for visualisation
* Logfiles:
    * gps.txt: an ASCII text file that contains the GPGGA, GPRMC and GPVTG messages
    * future enhancement: imu.dat: a binary file that contains the CORRIMUDATAS messages (with short binary HEADER)
* Use pdf documentation in resources

## Problem : Plot of flight route

 a tool which is plotting the flight route of a plane.
* Interpret gps.txt file, read GPGGA message
* Plot longitude and latitude on a 2-dimensional plot with x-axis = longitude and y-axis = lattitude
* Longitude and latitude shall be displayed in degrees ranging from -180...180 degrees. For example, position of Sydney is 150 Deg E, 31 Deg S. This shall be displayed as 150.00 for longitude and -31.00 for latitude (log of GPGGA is storing the values in a different format!)
* diagram and axis titles