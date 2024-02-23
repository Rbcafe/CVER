import struct

#
def ensure(field, n, nLeft):
    if nLeft < n:
        print "WARNING: field '%s', not enough data left (want %d, have %d). Perhaps optional field." % \
                (field, n, nLeft)
        return False
    return True

#stolen
#http://code.activestate.com/recipes/142812/
FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def hexdump(src, length=16, indent=0, addr=0):
    N=addr; result=''
    while src:
       s,src = src[:length],src[length:]
       hexa = ' '.join(["%02X"%ord(x) for x in s])
       s = s.translate(FILTER)
       result += (" "*indent) + "%010X   %-*s   %s\n" % (N, length*3, hexa, s)
       N+=length
    return result

#
def dprint(depth, args):
    print " "*(depth*4) + args

#the record printers in dumpXl.py and dumpPPT.py need to be merged to use this
#new generic function
def printFmt(rData, dLen, rFmt, rFNames, depth):

    fieldCount = offset = 0

    #skip last element due to trailing '%' in format string
    for fmt in rFmt.split("%")[:-1]:

        nLeft = dLen - offset
        fieldName = rFNames[fieldCount]

        if fmt == "1":
            if ensure(fieldName, 1, nLeft):
                val = struct.unpack("B", rData[offset:offset+1])[0]
                dprint(depth, "BYTE %s = %#x (%d)" % (fieldName, val, val))
                offset += 1
        elif fmt == "2":
            if ensure(fieldName, 2, nLeft):
                val = struct.unpack("H", rData[offset:offset+2])[0]
                dprint(depth, "WORD %s = %#x (%d)" % (fieldName, val, val))
                offset += 2
        elif fmt == "4":
            if ensure(fieldName, 4, nLeft):
                val = struct.unpack("I", rData[offset:offset+4])[0]
                dprint(depth, "DWORD %s = %#x (%d)" % (fieldName, val, val))
                offset += 4
        elif fmt[0] == "f":
            dataLen = int(fmt[1:])
            if dataLen > nLeft:
                print "Warning, field %s is longer (%d) than data left (%d). Dumping what's left:" % \
                        (fieldName, dataLen, nLeft)
                sys.stdout.write(hexdump(rData[offset:], indent=12))
            else:
                dprint(depth, "Field %s is %#x (%d) bytes, dumping:" % (fieldName, dataLen,
                        dataLen))
                sys.stdout.write(hexdump(rData[offset:offset+dataLen], indent=12))

            offset += dataLen
        elif fmt == "v":
            dprint(depth, "Field '%s' is variable length, dumping rest of record:" % (fieldName))
            sys.stdout.write(hexdump(rData[offset:], indent=12))
            break
        else:
            print "ERROR:Invalid format in record format string [%s]. Developer error!!" % (f)
            sys.exit(1)

        fieldCount += 1
