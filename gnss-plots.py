#!/usr/bin/python3.6

"""
  **************************************************************************************************
  * @file    crc_utility.py
  * @author  Genesys Electronics Design Team
  * @version V1.0.0
  * @date    14-Apr-21
  * @brief   This module is used for performing the cyclic redundancy check algorithm.
  *
  @verbatim
  **************************************************************************************************
   Copyright (c) 2023, Simon Wang
   All Rights Reserved

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
   IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
   FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
   IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
   OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

# GPGGA log data header
GNSS_GPGGA_LOG_HEADER = "$GPGGA"
# GPGGA log data format
GNSS_GPGGA_LOG_FIELD__LATITUDE_IDX           = 2
GNSS_GPGGA_LOG_FIELD__LATITUDE_DIRECTION_IDX = 3
GNSS_GPGGA_LOG_FIELD__LONGITUDE_IDX          = 4
GNSS_GPGGA_LOG_FIELD__LONGITUDE_DIRECTION_IDX= 5

# If parsing more than EFFICIENCY_THRESH number of log files, process using multiprocessing.
# Otherwise if parsing less log files, it is more efficient to parse sequencially.
EFFICIENCY_THRESH = 5

# Section keys used to denote the last line of text in a log file "section" where formatting
# is very different in the following section. These should be unique words or phrases. Tuple
# items are in order of the section number. i.e. SECTION_KEYS[0] relates to the end of
# the first section in the log file. The last section at the end of the log file does not need a
# section delimiter.
SECTION_KEYS = (" 2023", "Device Chemistry")
SECTION_DELIMS = [(" ", ","), ("=",)]

# Delimiters used to separate data and labels. Used for the parse_all function.
# DEFAULT_DELIMS = (",", ":", " ", "=")
DEFAULT_DELIMS = (",")

# Delimiters used to isolate labels. Used for the parse_labels function.
LABEL_DELIMS = ("-", ":")

# Delimiters used to isolate labels. Used for the parse_labels function.
DATA_DELIMS = (" ", ",")

# Output .xlsx file name.
OUTPUT_FILE_NAME = "Parsed_Logs.xlsx"


def parse(line: str, delims: tuple) -> list:
    """
    Parse an individual line from a log file.

    Args:
        line: Individual line of a log file.
        delims: Delimiters used to separate labels and data.

    Returns:
        List of parsed labels and data with leading/trailing whitespace removed.

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
        print("each extracted Long Lati data in GPGGA logs:")
        print(extract)
    # [x.strip() for x in ret]  # x.strign remove any trailing white space
    return extract
    

# @brief    Function to calculate CRC8 checksum of given data, least significant bit first,
#           both in terms of the algorithm and the polynomial to be used,
#           which is the so called "reverse polynomial". The reverse polynomial
#           CRC_UTILITY__CRC_8_CCITT_REVERSED should be used as crc_polynomial parameter.
# @param    data_ro         - buffer containing the data
# @param    crc_polynomial  - To use for CRC Calculation
# @return   error           - error result of funciton
# @return   crc_accumulator - CRC value result
#
def parse_all(log_file=None, delims=None, section_keys=None):
    """
    Parse everything in a log file. return a list of lists where each "sub-list"
    represents a parsed line in the log file.

    Args:
        log_file: Full path of the log file to be parsed.
        delims: Tuple conaining delimiter characters. If multiple sections, this will be a list
            of tuples.
        section_keys: Tuple containing unique words or phrases that denote the last line of a
            section within the log file.

    Returns:
        List of lists where each "sub-list" represents a parsed line in the log file.

    """
    ret = []
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



# generating dummy Data for plotting 

# np.array(ret)
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)


# plotting
fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()


#
# CRC calc for TempHumidity Sensor samples
#
print("CRC8 for real samples")
print("created my own exercise Git repository for practice python")
print("---------------------------------------------")


if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)

    root = tk.Tk()
    root.withdraw()
    folder = fd.askdirectory(title="Choose a folder containing log files")

    if not folder:
        log.info("No folder selected.")
        time.sleep(2)
        quit()
    
    # os.path.directoryname
    files = os.walk(folder)
    log_files = []
    results = []

    for root, directories, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(".log") or filename.endswith(".txt"):
                log.debug(filename)
                log_files.append(os.path.join(root, filename))

        log.info(f"Number of log files to parse: {len(log_files)}")

    # Based on number of files to be parsed, determine the most efficient processing method.
    start_time = time.time()
    for file in log_files:
        results.append(parse_all(file, DEFAULT_DELIMS))



#turn py to exe pyinstaller