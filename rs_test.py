import reedsolo as rs
import struct

print('Initializing Tables')

rs.init_tables(prim=0x187)

asm = 0x1ACFFC1D # attached sync marker specified in CCSDS 131.0-B-3
n = 255  # length of total message+ecc making up an RS codeword(bytes)
k = 223  # length of total message  in an RS codeword(bytes)
i = 8   # interleaving depth
fcr = 112   # first consecutive root
prim = 11   # primitive element
nsym = n-k  # length of ecc symbols in RS codeword
mtu = 1784  #maximum transfer unit (message data)

mes = b'\x01\x00\x0b\x05\x00\x01\x7e\x70\x8e\x00\x52\x7d\x53\x51'

#for ii in range(k):
#    mes += struct.pack('>B', ii)

t = [[1,0,0,0,1,1,0,1],
     [1,1,1,0,1,1,1,1],
     [1,1,1,0,1,1,0,0],
     [1,0,0,0,0,1,1,0],
     [1,1,1,1,1,0,1,0],
     [1,0,0,1,1,0,0,1],
     [1,0,1,0,1,1,1,1],
     [0,1,1,1,1,0,1,1]]

tInv = [[1,1,0,0,0,1,0,1],
        [0,1,0,0,0,0,1,0],
        [0,0,1,0,1,1,1,0],
        [1,1,1,1,1,1,0,1],
        [1,1,1,1,0,0,0,0],
        [0,1,1,1,1,0,0,1],
        [1,0,1,0,1,1,0,0],
        [1,1,0,0,1,1,0,0]]

def interleaver(message, size):
    rsBlocks = []
    for kk in range(i):
        appension = b''
        for ii in range(size):
            appension += message[((ii*i)+kk):(ii*i+1)+kk]
        rsBlocks.append(appension)
    return rsBlocks

def deinterleaver(message, size):
    codeBlocks = []
    appension = b''
    for kk in range(size):
        for ii in range(i):
            appension += message[((ii*size)+kk):((ii*size+1)+kk)]
            printable = ''.join("{:02x}".format(ord(c)) for c in str(appension))
    for ii in range(i):
        codeBlocks.append(appension[(ii*size):((ii+1)*size)])
    return codeBlocks

def inverter(codeBlock, matrix):
    outBlock = b''
    for bb in range(len(codeBlock)):
        binArray = codeBlock[bb:bb+1]
        try:
            tempBin = struct.unpack('!B', binArray)
        except Exception as e:
            print('Error: %s, binary array value: %s' % (str(e), binArray))
        binArray = tempBin[0]
        bin_simp = []
        for ii in range(8):
            bin_simp.append((binArray>>(7-ii))&0b1)
        bin_out = 0b0
        for ii in range(8):
            adder = 0
            for kk in range(8):
                adder += bin_simp[kk]&matrix[kk][ii]
            bin_out <<= 1
            bin_out |= (adder%2)
        outBlock += struct.pack('!B', bin_out)
    return outBlock

printable = ''.join("{:02x} ".format(ord(c)) for c in str(mes))
print('Original message: %s' % printable)
print('Length of message: %s' % len(mes))
print('Adding fill to message')

# fill up to MTU size with zeros
def resizer(message):
    mesMkUp = mtu - len(message)
    message = message + b'\x00'*mesMkUp
    return message

#Print the original message to be encoded
printable = ''.join("{:02x} ".format(ord(c)) for c in str(mes))
print('Message to encode: %s' % (printable))
print('Length of message now: %s' % len(mes))
print('Generating polynomials')

# pregenerate polynomials
gen = rs.rs_generator_poly(nsym, fcr=fcr, prim=prim)
printable = ''.join("{:02x} ".format(ord(c)) for c in str(gen))
print('Code Generator Polynomial: %s' % printable)
print('Interleaving message blocks')

# break up message into eight 223-byte codeblocks
rsBlocks = interleaver(mes, k)
print('Encoding message blocks')

# encode the codeblocks
mesecc = []
for ii in range(i):
    inverted = inverter(rsBlocks[ii], tInv)
    mesecc.append(rs.rs_simple_encode_msg(inverted, nsym, gen=gen))

# pass the codeblocks through dual-basis inversion
outCode = []
for ii in range(i):
    outCode.append(inverter(mesecc[ii], t))

# prepare and deinterleave the codeblocks to return to original byte order
eccOut = b''
messOut = b''
for ii in range(i):
    byteThing = b''
    messThing = b''
    byteThing = outCode[ii][k:]
    messThing = outCode[ii][:k]
    for bb in range(len(byteThing)):
        eccOut += struct.pack('!c', byteThing[bb])
    for dd in range(len(messThing)):
        messOut += struct.pack('!c', messThing[dd])
mess = deinterleaver(messOut, k)
ecc = deinterleaver(eccOut, nsym)
codeWord = ''
eccOut = ''

# make the code blocks look pretty for printing
for qq in range(i):
    eccOut += ''.join("{:02x} ".format(ord(c)) for c in str(ecc[qq]))
    codeWord += ''.join("{:02x} ".format(ord(c)) for c in str(mess[qq]))
print('CodeWord: %s' % codeWord)
print('ECC: %s' % (eccOut))
print('Output size: %s' % (len(mesecc)*255))
