# Python implementation of CCSDS Recommendation 131.0-b-3 scrambler using 
# generator polynomial x^8+x^7+x^5+x^3+1
# input message is a byte string, output message is a byte string
# 2020 Oakman Aerospace, Inc.
# Author: andrew.johnson@oak-aero.com

import struct

def scrambler(message):
    accumulator = 0b0
    polynomial = 0b11111111
    outMask = 0b1
    outMessage = b''
    for ii in range(len(message)*8):
        xIn = polynomial & outMask
        xOut = xIn
        xIn = xIn ^ ((polynomial >> 3) & outMask)
        xIn = xIn ^ ((polynomial >> 5) & outMask)
        xIn = xIn ^ ((polynomial >> 7) & outMask)
        polynomial >>= 1
        polynomial |= (xIn << 7)
        accumulator <<= 1
        accumulator |= xOut
        if ii > 0 and ((ii+1)%8)==0:
            unpackedByte = struct.unpack('>B',message[int(ii/8):int((ii/8)+1)])[0]
            unpackedByte ^= accumulator
            outMessage += struct.pack('>B',unpackedByte)
            accumulator = 0b0
    return outMessage