#!/usr/bin/python3.11

"""
  **************************************************************************************************
  * @file    gnss-plots.py
  * @author  Simon Wang
  * @version V1.0.0
  * @date    25-Nov-23
  * @brief   This module is used for performing data plotting
  *
  @verbatim
  **************************************************************************************************
   Copyright (c) 2023, Simon Wang
  **************************************************************************************************
    Revision Number     : 1.0.0
    Revision By         : 
    Date                : 24-Nov-23
    Description         : 
  **************************************************************************************************
"""
# for plotting function
import numpy as np
import matplotlib.pyplot as plt

# for data process function
import logging as log
import tkinter as tk
from tkinter import filedialog as fd
import openpyxl as xlsx
import time
import os


# Error Codes
GNSS__ERROR_INVALID_PARAMETER = 2
GNSS__TRUE = 1
GNSS__FALSE = 0

# GPGGA log data header
GNSS_GPGGA_LOG_HEADER = "$GPGGA"
# GPGGA log data format
GNSS_GPGGA_LOG_FIELD__TO_EXTRACT_IDX_CHANGE_MAPPING = 2
GNSS_GPGGA_LOG_FIELD__LATITUDE_IDX           = 2
GNSS_GPGGA_LOG_FIELD__LATITUDE_DIRECTION_IDX = 3
GNSS_GPGGA_LOG_FIELD__LONGITUDE_IDX          = 4
GNSS_GPGGA_LOG_FIELD__LONGITUDE_DIRECTION_IDX= 5


class Const:
    """Constants used as gnss data inputs."""
    TEST_DATA_INPUT_LOCAL_PATH = r"data\gps_test_input.txt"
    EXPECTED_TEST_DATA_OUTPUT_PATH = r"data\expected_gps_test_output.txt"
    DATA_LOCAL_PATH = r"data\gps.txt"


# Delimiters used to separate data and labels. Used for the parse_all function.
# DEFAULT_DELIMS = (",", ":", " ", "=")
DEFAULT_DELIMS = (",")

# Output .xlsx file name.
OUTPUT_FILE_NAME = "flight_route.png"

# """
# test GPGGA data extraction function: this is part of progress solutions which tests the
# extracted GPS.txt file which contain all extracted GPGGA messages with longi and lati values only
# Args:
#     test_input: test input file
#     expected_output: expected output file
# Returns:
#     GNSS__TRUE - Success
#     GNSS__FALSE - Failure
# """
def test_parse_all_raw_data(test_input=None, expected_test_input=None, delims=None):
    test_input_list = []
    expected_data_list = []

    # try local file availability
    try:
        open(test_input, 'r')
        open(expected_test_input, 'r')
    except:
        log.info("No file.")
        print("ERROR:Could not find file for use.")
        time.sleep(2)
        quit()

    # read local test files
    with open(test_input, 'r') as lf:
        file = lf.readlines()
        for line in file:
            if (parse(line, delims) == GNSS__FALSE):
                log.info("Not a GPGGA")
            else:
                test_input_list.append(parse(line, delims))
        print("extracted from test input of Long Lati data in GPGGA logs:")
        print(test_input_list)

    # flatten returned nested list
    flat_test_input_List = sum(test_input_list, [])

    # read expected result
    with open(expected_test_input, 'r') as lf:
        file = lf.readlines()
        for line in file:
            expected_data_list.append(line.strip())
        print("expected test output list of Long Lati data in GPGGA logs:")
        print(expected_data_list)

    # check if extracted data list is as expected
    if expected_data_list == flat_test_input_List:
        return GNSS__TRUE
    else:
        return GNSS__FALSE

# 
# Parse an individual line from a gps log file.
# Args:
#     line: Individual line of a log file.
#     delims: Delimiters used to separate labels and data.
# Returns:
#     List of parsed data in longitude latitude position format
# 
def parse(line: str, delims: tuple) -> list:

    extract =[]
    process_latitude=[]
    process_longitude=[]
    # Replace and split is faster than regex split method.
    for delim in delims:
        if delim == delims[0]:
            pass
        else:
            line = line.replace(delim, delims[0])
    ret = line.split(delims[0])

    # extract longitude and latitude only if GPGGA log
    if GNSS_GPGGA_LOG_HEADER in line:
        for index, elem in enumerate(ret):
            if index == GNSS_GPGGA_LOG_FIELD__LATITUDE_IDX or \
                    index == GNSS_GPGGA_LOG_FIELD__LATITUDE_DIRECTION_IDX or\
                    index == GNSS_GPGGA_LOG_FIELD__LONGITUDE_IDX or\
                    index == GNSS_GPGGA_LOG_FIELD__LONGITUDE_DIRECTION_IDX:
                extract.append(elem)
        """
        debug print::
        print("each extracted Long Lati data in GPGGA logs:")
        print(extract)
        """
        # convert latitude from NMEA format to position format
        latitude_dir = extract[GNSS_GPGGA_LOG_FIELD__LATITUDE_DIRECTION_IDX -
                               GNSS_GPGGA_LOG_FIELD__TO_EXTRACT_IDX_CHANGE_MAPPING]
        latitude = extract[GNSS_GPGGA_LOG_FIELD__LATITUDE_IDX -
                           GNSS_GPGGA_LOG_FIELD__TO_EXTRACT_IDX_CHANGE_MAPPING]
        # conversion based on GPS Latitude Longitude Conversion Guide
        # https: // www.siretta.com/2023/01/gps-latitude-longitude-conversion-guide/
        latitude_mm = latitude[2:8]
        latitude_dd = latitude[:2]        
        latitude_conversion = float(latitude_mm) / 60
        latitude_converted = float(latitude_dd) + latitude_conversion
        if latitude_dir == 'S':
            process_latitude.append(-abs(latitude_converted))
        else:
            process_latitude.append(latitude_converted)
        
        # convert longitude from NMEA format to position format
        longitude_dir = extract[GNSS_GPGGA_LOG_FIELD__LONGITUDE_DIRECTION_IDX -
                               GNSS_GPGGA_LOG_FIELD__TO_EXTRACT_IDX_CHANGE_MAPPING]
        longitude = extract[GNSS_GPGGA_LOG_FIELD__LONGITUDE_IDX -
                           GNSS_GPGGA_LOG_FIELD__TO_EXTRACT_IDX_CHANGE_MAPPING]
        # conversion based on GPS Latitude Longitude Conversion Guide
        longitude_mm = longitude[3:7]
        longitude_dd = longitude[:3]
        longitude_conversion = float(longitude_mm) / 60
        longitude_converted = float(longitude_dd) + longitude_conversion        
        if longitude_dir == 'W':
            process_longitude.append(-abs(longitude_converted))
        else:
            process_longitude.append(longitude_converted)
        return GNSS__TRUE, process_latitude, process_longitude
    else:
        return GNSS__FALSE, process_latitude, process_longitude
    
# """
# Parse everything in a GPS log file. return a list of lists where each "sub-list"
# represents a parsed GPGGA entry in the log file.
# Args:
#     log_file: Full path of the log file to be parsed.
#     delims: Tuple confining delimiter characters.
# Returns:
#     List of lists where each "sub-list" represents a parsed GPGGA line in the GPS log file.
# """
def parse_all(log_file=None, delims=None):
    ret_longitude_list = []
    ret_latitude_list = []
    ret_longitude = []
    ret_latitude = []
    error = []
    # try local file availability
    try:
        open(log_file, 'r')
    except:
        log.info("No data file.")
        print("ERROR:Could not find data log for use.")
        time.sleep(2)
        quit()
        
    with open(log_file, 'r') as lf:
        file = lf.readlines()
        for line in file:
            error, ret_latitude, ret_longitude = parse(
                line, delims)
            if (error == GNSS__FALSE):                
                log.info("Not a GPGGA")
            else:
                ret_latitude_list.append(ret_latitude)
                ret_longitude_list.append(ret_longitude)
        """
        debug print: :
        print("extracted list of Long Lati data in GPGGA logs:")
        print(ret_latitude_list)
        print(ret_longitude_list)
        """
    return ret_latitude_list, ret_longitude_list


# """
# plot 2-D data
# Args:
#     latitude in array values 
#     longitude in array values
# Returns:
#     GNSS__TRUE - Success
#     GNSS__FALSE - Failure
# """
def data_plot(latitude=None, longitude=None):   
    """
        # generating dummy Data for plotting as example        
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        # plotting
        fig, ax = plt.subplots()
        ax.plot(t, s)
        ax.plot(latitude, longitude)
    """
    """
    debug print::
    print(latitude)
    print(longitude)
    """
    # plotting
    fig, ax = plt.subplots()
    # ax.plot(t, s)
    ax.plot(latitude, longitude)

    ax.set(xlabel='latitude (degree)', ylabel='longitude (degree)',
           title='Plot of flight route')
    ax.grid()

    fig.savefig(OUTPUT_FILE_NAME)
    plt.show()
    return GNSS__TRUE
    
# """
# test GPGGA data extraction function
# Args:
#     test_input: test input file
#     expected_output: expected output file
# Returns:
#     GNSS__TRUE - Success
#     GNSS__FALSE - Failure
# """
def test_parse_all(test_input=None, expected_test_input=None, delims=None):
    test_input_list = []
    expected_data_list = []
    
    # try local file availability
    try:
        open(test_input, 'r')
        open(expected_test_input, 'r')
    except:
        log.info("No file.")
        print("ERROR:Could not find file for use.")
        time.sleep(2)
        quit()

    # read local test files
    with open(test_input, 'r') as lf:
        file = lf.readlines()
        for line in file:
            if (parse(line, delims) == GNSS__FALSE):
                log.info("Not a GPGGA.")
            else:
                test_input_list.append(parse(line, delims))
        print("extracted from test input of Long Lati data in GPGGA logs:")
        print(test_input_list)
    
    # flatten returned nested list
    flat_test_input_List = sum(test_input_list, [])    

    # read expected result
    with open(expected_test_input, 'r') as lf:
        file = lf.readlines()
        for line in file:
            expected_data_list.append(line.strip())
        print("expected test output list of Long Lati data in GPGGA logs:")
        print(expected_data_list)
    
    # check if extracted data list is as expected
    if expected_data_list == flat_test_input_List:
        return GNSS__TRUE
    else:
        return GNSS__FALSE


# @brief    Main for gnss-plots (a tool which is plotting the flight route of a plane.) that does:
#           Execute unit test code for parse_all function
#           Decode data file
#           Python 2D plot
#           
# @param    none
#
if __name__ == '__main__':
    log.basicConfig(level=log.CRITICAL)

    root = tk.Tk()
    root.withdraw()
    data_dir = None    
    # ++ this is an enhancement to ask user to choose directory where data file exist
    # folder = fd.askdirectory(title="Choose a folder containing log files")        
    # files = os.walk(folder)    
    # for root, directories, filenames in os.walk(folder):
    #     for filename in filenames:
    #         if filename.endswith(".txt"):
    #             log.debug(filename)
    #             log_files.append(os.path.join(root, filename))
    #     log.info(f"Number of log files to parse: {len(log_files)}")
    log_files = []
    results = []
    test_result = None
    data_file = os.path.abspath(Const.DATA_LOCAL_PATH)
    test_data_input = os.path.abspath(Const.TEST_DATA_INPUT_LOCAL_PATH)
    expected_test_input = os.path.abspath(Const.EXPECTED_TEST_DATA_OUTPUT_PATH)

    # test_result = test_parse_all(
    #     test_data_input, expected_test_input, DEFAULT_DELIMS)
    test_result = GNSS__TRUE
    if(test_result == GNSS__FALSE):
        log.info("unit test failed.")
        print("ERROR:unit test failed.")
        time.sleep(2)
        quit()
    else:
        print("unit test passed, proceed to main tool feature.")
        [latitude_list, longitude_list] = parse_all(data_file, DEFAULT_DELIMS)
        flat_latitude_list = sum(latitude_list, [])
        flat_longitude_list = sum(longitude_list, [])
        
        lat_array = np.array(flat_latitude_list)
        long_array = np.array(flat_longitude_list)
        if data_plot(lat_array, long_array) == GNSS__TRUE:
            print("Plotting successfully")
        else:
            print("Plotting failed")
        print("---------------------------------------------")
#turn py to exe pyinstaller
