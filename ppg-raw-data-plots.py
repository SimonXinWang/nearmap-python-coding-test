#!/usr/bin/python3.11
# 
#   **************************************************************************************************
#   * @file    gnss-plots.py
#   * @author  Simon Wang
#   * @version V1.0.0
#   * @date    25-Nov-23
#   * @brief   This module is a solution for plotting 2 D text file in CSV format
#   *
#   @verbatim
#   **************************************************************************************************
#    Copyright (c) 2023, Simon Wang
#   **************************************************************************************************
#     Revision Number     : 1.0.0
#     Revision By         : 
#     Date                : 25-Nov-23
#     Description         : 
#   **************************************************************************************************
# 

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
GNSS_GPGGA_LOG_FIELD__LATITUDE_MINUTES_START_IDX= 2
GNSS_GPGGA_LOG_FIELD__LATITUDE_MINUTES_END_IDX = 8
GNSS_GPGGA_LOG_FIELD__LONGITUDE_MINUTES_START_IDX= 3
GNSS_GPGGA_LOG_FIELD__LONGITUDE_MINUTES_END_IDX = 7
GNSS_GPGGA_LOG_FIELD__LATITUDE_DIRECTOR_SOUTH_CHAR = 'S'
GNSS_GPGGA_LOG_FIELD__LONGITUDE_DIRECTOR_WEST_CHAR = 'W'
GNSS_GPGGA_LOG_FIELD__MINUTE_DEGREE_CONVERSION_FACTOR = 60
# gnss plot tool unit test data file format
GNSS__TEST_FILE_FORMAT_LATITUDE_VALUE_LINE_NUMBER = 0

# gnss plot tool user interactive pause time
GNSS__USER_INTERACTIVE_SLEEP_BEFORE_QUIT_PROGRAM_SECOND = 2

# PATH for data log and test data log
class Const:
    """Constants used as gnss data inputs."""
    TEST_DATA_INPUT_LOCAL_PATH = r"data\only_ppg-raw-data_test_input.TXT"
    EXPECTED_TEST_DATA_OUTPUT_PATH = r"data\expected_only_ppg-raw-data_test_output.TXT"
    # DATA_LOCAL_PATH = r"data\only_ppg-raw-data_test_input.TXT"
    DATA_LOCAL_PATH = r"data\ppg-raw-data_ch3_6_12_2023_16-57-13.TXT"


# Delimiters used to separate data and labels. Used for the parse_all function.
DEFAULT_DELIMS = ("=", ",")
# DEFAULT_DELIMS = (",")
DEFAULT_DELIMS__GNSS_GPGGA_LOG_FIELD_DELIMITERS_INDEX = 0

# Output plot file name.
OUTPUT_FILE_NAME = "ppg_raw_plot.png"

# ============================part of progressive solutions============================
# following three functions contain progressive work during the task: 
# 1. parse GPS.txt data to single list of containing GPGGA logs' raw 4 tuple values
# 2. pass each line from a log file to parse function
# 3. unit test code for testing item 1 and 2 (i.e. verify if GPGGA items in GPS.txt 
#    is extracted correctly)
# 

def parse_raw(line: str, delims: tuple) -> list:
    """
    parse GPS.txt data to single list of containing GPGGA logs' raw 4 tuple values
    """
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
        print("each extracted Longitude Latitude data in GPGGA logs:")
        print(extract)
        return extract
    else:
        return GNSS__FALSE

    # Replace and split is faster than regex split method.
    for delim in delims:
        if delim == delims[0]:
            pass
        else:
            line = line.replace(delim, delims[0])
    ret = line.split(delims[0])
    return [x.strip() for x in ret]
    

def parse_all_raw(log_file=None):
    """
    pass each line from a log file to parse function
    """
    ret = []
    
    # try local file availability
    try:
        open(log_file, 'r')
    except:
        log.info("No data file.")
        print("ERROR:Could not find data log for use.")
        time.sleep(GNSS__USER_INTERACTIVE_SLEEP_BEFORE_QUIT_PROGRAM_SECOND)
        quit()

    with open(log_file, 'r') as file:
        # Read lines from the file, strip newline characters, and store them in an array
        lines_array = [line.strip() for line in file.readlines()]
        print("extracted array")
        print(lines_array)
    return lines_array


def parse_all_extract_raw(log_file=None, delims=None):
    """
    pass each line from a log file to parse function
    """
    ret = []
    # try local file availability
    try:
        open(log_file, 'r')
    except:
        log.info("No data file.")
        print("ERROR:Could not find data log for use.")
        time.sleep(GNSS__USER_INTERACTIVE_SLEEP_BEFORE_QUIT_PROGRAM_SECOND)
        quit()
        
    with open(log_file, 'r') as lf:
        file = lf.readlines()
        for line in file:
            ret.append(parse(line, delims))
        print("extracted list of Long Lati data in GPGGA logs:")
        print(ret)
    return ret


def test_parse_all_raw_data(test_input=None, expected_test_input=None, delims=None):
    test_input_list = []
    expected_data_list = []
    """
    3. unit test code for testing item 1 and 2 (i.e. verify if GPGGA items in GPS.txt
    is extracted correctly)
    """
    # try local file availability
    try:
        open(test_input, 'r')
        open(expected_test_input, 'r')
    except:
        log.info("No file.")
        print("ERROR:Could not find file for use.")
        time.sleep(GNSS__USER_INTERACTIVE_SLEEP_BEFORE_QUIT_PROGRAM_SECOND)
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



def data_plot(latitude=None, longitude=None):   
    """
    @brief plot 2-D data
    @param: 
        latitude in array values 
        longitude in array values
    @returns:
        GNSS__TRUE - Success
        GNSS__FALSE - Failure
    """   
    #     # generating dummy Data for plotting as example        
    #     t = np.arange(0.0, 2.0, 0.01)
    #     s = 1 + np.sin(2 * np.pi * t)
    #     # plotting
    #     fig, ax = plt.subplots()
    #     ax.plot(t, s)
    #     ax.plot(latitude, longitude)

    # debug print::
    # print(latitude)
    # print(longitude)
    
    # plotting
    fig, ax = plt.subplots()    
    ax.plot(latitude, longitude)

    ax.set(xlabel='time (discrete)', ylabel='ppg raw (adc steps)',
           title='Plot of ppg raw data')
    ax.grid()

    fig.savefig(OUTPUT_FILE_NAME)
    plt.show()
    return GNSS__TRUE

def test_parse_all(test_input=None, expected_test_input=None, delims=None):
    """
     @brief: test GPGGA data extraction function
     @param:
         test_input: test input file
         expected_output: expected output file
     @returns:
         GNSS__TRUE - Success
         GNSS__FALSE - Failure
    """    
    expected_data_latitude_list = []
    expected_data_longitude_list = []
    test_input_longitude_list = []
    test_input_latitude_list = []
    ret_longitude = []
    ret_latitude = []
    error = GNSS__FALSE
    # try local file availability
    try:
        open(test_input, 'r')
        open(expected_test_input, 'r')
    except:
        log.info("No file.")
        print("ERROR:Could not find file for use.")
        # sleep 2 seconds
        time.sleep(GNSS__USER_INTERACTIVE_SLEEP_BEFORE_QUIT_PROGRAM_SECOND)
        quit()
    
    # read local test files
    with open(test_input, 'r') as lf:
        file = lf.readlines()
        for line in file:
            error, ret_latitude, ret_longitude = parse(
                line, delims)
            if (error == GNSS__FALSE):
                log.info("Not a GPGGA")
            else:
                """
                Reviewer feedback:A lot of overhead in the code such as copying and moving data.
                """
                test_input_latitude_list.append(ret_latitude)
                test_input_longitude_list.append(ret_longitude)                
    # flatten returned nested list
    flat_test_input_latitude_List = sum(test_input_latitude_list, [])
    flat_test_input_longitude_List = sum(test_input_longitude_list, [])
    print("extracted from test input of Long Lati data in GPGGA logs:")
    print(flat_test_input_latitude_List)
    print(flat_test_input_longitude_List)

    # read expected result
    with open(expected_test_input, 'r') as lf:
        file = lf.readlines()
        for index, line in enumerate(file):            
            if index == GNSS__TEST_FILE_FORMAT_LATITUDE_VALUE_LINE_NUMBER:
                expected_data_latitude_list.append(float(line.strip()))
            else:                
                expected_data_longitude_list.append(float(line.strip()))
        print("expected test output list of Longitude Latitude data in GPGGA logs:")
        print(expected_data_latitude_list)
        print(expected_data_longitude_list)
    
    # check if extracted data list is as expected
    if expected_data_longitude_list == flat_test_input_longitude_List\
            and expected_data_latitude_list == flat_test_input_latitude_List:
        return GNSS__TRUE
    else:
        return GNSS__FALSE

def generate_incrementing_array(num_elements):
    return [i + 1 for i in range(num_elements)]


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
    

    print("proceed to main tool feature.")
    ppg_raw_list = parse_all_raw(
        data_file)

    """
    Reviewer feedback:A lot of overhead in the code such as copying and moving data.
    """
    # convert list to array
    ppg_array = np.array(ppg_raw_list)
    
    # using loop Converting all strings in list to integers Naive Method
    for i in range(0, len(ppg_raw_list)):
        ppg_raw_list[i] = int(ppg_raw_list[i])
    print(ppg_raw_list)

    # generating time line for plotting
    # t = np.arange(0.0, 2.0, 1)    

    # generating time line for plotting
    t = generate_incrementing_array(ppg_array.size)

    # Print the result
    print(t)
    if data_plot(t, ppg_array) == GNSS__TRUE:
        print("Plotting successfully")
    else:
        print("Plotting failed")
    print("------------------main end---------------------------")

