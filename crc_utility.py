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
   Copyright (c) 2020, Genesys Electronics Design Pty Ltd
   All Rights Reserved
   Unit 5/33 Ryde Road
   Pymble NSW 2073
   Australia
   Telephone # +61-2-9496 8900

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
    Revision By         : MC
    Date                : 14-Apr-21
    Description         : This module is used for performing the cyclic redundancy check algorithm
  **************************************************************************************************
"""

# CRC polynomials
CRC_UTILITY__CRC_8_CCITT_NORMAL = 0x07
CRC_UTILITY__CRC_8_CCITT_REVERSED = 0xE0
CRC_UTILITY__CRC_8_TH_SHT4X = 0x31

# Error Codes
CRC_UTILITY__ERROR_INVALID_PARAMETER = 2


# @brief    Function to calculate CRC8 checksum of given data, least significant bit first,
#           both in terms of the algorithm and the polynomial to be used,
#           which is the so called "reverse polynomial". The reverse polynomial
#           CRC_UTILITY__CRC_8_CCITT_REVERSED should be used as crc_polynomial parameter.
# @param    data_ro         - buffer containing the data
# @param    crc_polynomial  - To use for CRC Calculation
# @return   error           - error result of funciton
# @return   crc_accumulator - CRC value result
#
def calculate_crc8_lsb(data_ro, crc_polynomial):
    error = 0
    byte_counter = 0
    # original
    crc_accumulator = 0       
    # crc_accumulator = 0xFF

    #check inputs data not empty
    if ((not data_ro) or (not crc_polynomial)):
        error = CRC_UTILITY__ERROR_INVALID_PARAMETER
        print('Invalid Data or CRC Accumulator.')
    else:
        if ((len(data_ro) == 0) or (crc_polynomial == 0)):
            error = CRC_UTILITY__ERROR_INVALID_PARAMETER
            print('Invalid Length or Polynomial.')
        else:
            byte_counter = 0

            for _ in range(len(data_ro)):
                data_byte = data_ro[byte_counter]
                crc_accumulator = (crc_accumulator ^ data_byte)
                crc_accumulator &= 0xFF
                for _ in range(8):
                    # if rightmost (most significant) bit is set
                    if crc_accumulator & 0x01 != 0:
                        # (right shift by 1) XOR polynomial
                        crc_accumulator = crc_polynomial ^ (crc_accumulator >> 1)
                    else:
                        # right shift by 1
                        crc_accumulator = (crc_accumulator >> 1)
                    crc_accumulator &= 0xFF
                byte_counter = byte_counter + 1

    return error, crc_accumulator

def calculate_crc16(data_ro):
    crc_accumulator = 0
    byte_counter = 0
    for _ in range(len(data_ro)):
        data_byte = data_ro[byte_counter]
        crc_accumulator = crc_accumulator ^ data_byte
        crc_accumulator &= 0xFFFF
        crc_polynomial = 0x8408
        for _ in range(8):
            if (crc_accumulator & 0x1) != 0:
                crc_accumulator = crc_polynomial ^ (crc_accumulator >> 1)
            else:
                crc_accumulator = crc_accumulator >> 1
            crc_accumulator &= 0xFFFF
        byte_counter = byte_counter + 1

    return crc_accumulator


#
# CRC calc for TempHumidity Sensor samples
#
print("CRC8 for real samples")
error, crc = calculate_crc8_lsb([0x10, 0xC5], CRC_UTILITY__CRC_8_TH_SHT4X)
print(hex(crc))
print("error is:", error)


print("CRC8 for example")
error, crc = calculate_crc8_lsb([0xEF, 0xBF], CRC_UTILITY__CRC_8_TH_SHT4X)
print(hex(crc))
error, crc = calculate_crc8_lsb([0xBF, 0xEF], CRC_UTILITY__CRC_8_TH_SHT4X)
print(hex(crc))
error, crc = calculate_crc8_lsb([0xBF, 0xEF], CRC_UTILITY__CRC_8_CCITT_REVERSED)
print(hex(crc))

print("created my own exercise Git repository for practice python")
print("---------------------------------------------")
#
# verify CRC result by inserting the result into end of data array
#
print(calculate_crc16([0, 1, 2, 1, 0, 1, 0 ,0, 0xC61B]))

print("Simon tried himself here") 
print(hex(calculate_crc16([0x00, 0x01, 0x02, 4, 0, 1, 0, 0])))


#
# all data are in Hex
#
print('Hex of Caclulated CRC16:', hex(calculate_crc16([0x7E,0x10, 0x00, 0x01, 0x02, 0x01, 0x00, 0x01, 0x00, 0x00, 0x1B, 0xC6])))

#
# all data are in decimal
#
print('Caclulated CRC16 in decimal:', calculate_crc16([0, 1, 2, 1, 0, 1, 0 ,0, 125, 1782]))
