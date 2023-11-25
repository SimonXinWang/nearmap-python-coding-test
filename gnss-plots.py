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
GNSS__TURE = 1
GNSS__FALSE = 0

# GPGGA log data header
GNSS_GPGGA_LOG_HEADER = "$GPGGA"
# GPGGA log data format
GNSS_GPGGA_LOG_FIELD__LATITUDE_IDX           = 2
GNSS_GPGGA_LOG_FIELD__LATITUDE_DIRECTION_IDX = 3
GNSS_GPGGA_LOG_FIELD__LONGITUDE_IDX          = 4
GNSS_GPGGA_LOG_FIELD__LONGITUDE_DIRECTION_IDX= 5


class Const:
    """Constants used as inputs gnss data."""
    # 
    TEST_DATA_INPUT_LOCAL_PATH = r"data\gps_test_input.txt"
    EXPECTED_TEST_DATA_OUTPUT_PATH = r"data\expected_gps_test_output.txt"
    DATA_LOCAL_PATH = r"data\gps.txt"


# Delimiters used to separate data and labels. Used for the parse_all function.
# DEFAULT_DELIMS = (",", ":", " ", "=")
DEFAULT_DELIMS = (",")

# Delimiters used to isolate labels. Used for the parse_labels function.
LABEL_DELIMS = ("-", ":")

# Delimiters used to isolate labels. Used for the parse_labels function.
DATA_DELIMS = (" ", ",")

# Output .xlsx file name.
OUTPUT_FILE_NAME = "Parsed_Logs.xlsx"

# 
# Parse an individual line from a log file.
# Args:
#     line: Individual line of a log file.
#     delims: Delimiters used to separate labels and data.
# Returns:
#     List of parsed labels and data with leading/trailing whitespace removed.
# 
def parse(line: str, delims: tuple) -> list:

    extract =[]
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
        print("each extracted Long Lati data in GPGGA logs:")
        print(extract)
    return extract
    
# """
# Parse everything in a log file. return a list of lists where each "sub-list"
# represents a parsed line in the log file.
# Args:
#     log_file: Full path of the log file to be parsed.
#     delims: Tuple conaining delimiter characters. If multiple sections, this will be a list
#         of tuples.
#     section_keys: Tuple containing unique words or phrases that denote the last line of a
#         section within the log file.
# Returns:
#     List of lists where each "sub-list" represents a parsed line in the log file.
# """
def parse_all(log_file=None, delims=None, section_keys=None):
    ret = []

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
        if section_keys is None:
            # No separate sections.
            for line in file:
                ret.append(parse(line, delims))
        else:
            # Parse each section of the log file separately.
            section_num = 0
            for line in file:
                ret.append(parse(line, delims[section_num]))
                if section_num < len(section_keys):
                    if section_keys[section_num] in line:
                        section_num += 1
            print("extracted list of Long Lati data in GPGGA logs:")
            print(ret)
    return ret


# """
# plot 2-D data
# Args:
#     Lattitude: x-axis values 
#     Longitude: y-axis values
# Returns:
#     GNSS__TRUE - Success
#     GNSS__FALSE - Failure
# """
def data_plot(Lattitude=None, Longitude=None):
    # np.array(ret)

    # generating dummy Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    # plotting
    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='Plot of flight route')
    ax.grid()

    fig.savefig("flight_route.png")
    plt.show()
    #
    # Debug print
    #
    print("Plotted successfully")
    print("created my own exercise Git repository for practice python")
    print("---------------------------------------------")
    return GNSS__TURE


# """
# test parse_all function
# Args:
#     test_input: test input file
#     expected_output: expected output file
# Returns:
#     GNSS__TRUE - Success
#     GNSS__FALSE - Failure
# """
def test_parse_all(Lattitude=None, Longitude=None):
    ret = []

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
        if section_keys is None:
            # No separate sections.
            for line in file:
                ret.append(parse(line, delims))
        else:
            # Parse each section of the log file separately.
            section_num = 0
            for line in file:
                ret.append(parse(line, delims[section_num]))
                if section_num < len(section_keys):
                    if section_keys[section_num] in line:
                        section_num += 1
            print("extracted list of Long Lati data in GPGGA logs:")
            print(ret)    
    return GNSS__TURE

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
    # folder = fd.askdirectory(title="Choose a folder containing log files")
    
    # os.path.directoryname
    # 
    # files = os.walk(folder)    
    log_files = []
    results = []
    data_file = os.path.abspath(Const.DATA_LOCAL_PATH)
    # for root, directories, filenames in os.walk(folder):
    #     for filename in filenames:
    #         if filename.endswith(".txt"):
    #             log.debug(filename)
    #             log_files.append(os.path.join(root, filename))

    #     log.info(f"Number of log files to parse: {len(log_files)}")

    # number of files to be parsed
    # start_time = time.time()
    # for file in log_files:
    results.append(parse_all(data_file, DEFAULT_DELIMS))

    data_plot()
#turn py to exe pyinstaller