# nearmap-python-coding-test

## Constraints

* Must be written Python
* Use Python 3.6 or higher
* Use matplotlib.pyplot for visualisation
* Logfiles:
    * gps.txt: an ASCII text file that contains the GPGGA, GPRMC and GPVTG messages
    * imu.dat: a binary file that contains the CORRIMUDATAS messages (with short binary HEADER)
* Use pdf documentation in resources + do your own research online if required

## Problem 1: Plot of flight route

Create a tool which is plotting the flight route of a plane.
* Interpret gps.txt file, read GPGGA message
* Plot longitude and lattitude on a 2-dimensional plot with x-axis = longitude and y-axis = lattitude
* Longitude and lattitude shall be displayed in degrees ranging from -180...180 degrees. For example, position of Sydney is 150 Deg E, 31 Deg S. This shall be displayed as 150.00 for longitude and -31.00 for lattitude (be aware that GPGGA is storing the values in a different format!)
* Set diagram and axis titles

## Problem 2: Plot of IMU measurement

Create a tool which is plotting the IMU data from a flight.
* Interpret IMU.dat, read CORRIMUDATAS (binary short header) message
* Calculate average sampling rate of the CORRIMUDATAS message in samples per second
* Plot 20 seconds of pitch, roll and yaw data as soon IMU is turned on (as long IMU is off rates will be 0.0)
* Plot all three rates in same diagram, use legend to indicate which graph corresponds to which measurement

## Submission instructions

* A zip file containing the following - submitted to your agent or nearmap contact.
  * All python files created by you to solve the problem(s)

* DO NOT send pull requests against this repository for two reasons:
  * We don't want executables checked into source control
  * We don't want other candidates to see your solution
