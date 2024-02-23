#!/usr/bin/python
import sys
import struct
from util import hexdump
from pptRecs import recDict
import zlib
import binascii

#
PPT_HDR_LEN = 8
CONTAINER_MASK = 0xf

#ghetto
REC_COUNT = 0
REC_OFFSET = 1

#
COMPLEX_TYPES = [
    'CF Run',
    'PF Run',
    'SI Run',
    'CF2002 Run',
    'SI2003 Run',
    'PF2000 Run',
    'CF2000 Run',
    'SI2000 Run',
    'tabStops',
    'GrColorAtom',
    'ColorEntry[]',
    'PSR_GPointAtom',
    'PSR_DateTimeAtom',
    'GRatioAtom',
    'PSR_GScalingAtom',
    'GPointAtom',
    'PSR_GRatioAtom',
]


#custom handler for PersistPtrIncrementalBlock (0x1772, 6002)
def printPersist(data):

    maxLen = len(data)
    startSheets = struct.unpack("I", data[:4])[0]
    offset = 4
    start = startSheets & 0xfffff
    ns = (startSheets & 0xfff00000) >> 20
    print "\tStart %#x (%d), nsheets #%x (%d)" % (start, start, ns, ns)

    while ns > 0 and offset < maxLen:

        sheet =  struct.unpack("I", data[offset:offset+4])[0]
        print "\tSheet offset %#x (%d)" % (sheet, sheet)
        offset += 4
        ns -= 1

    if ns != 0:
        print "!!WARNING: Still have %d sheets left in persist block" % (ns)


#some records are important and require manual printing
customPrinters = {0x1772:printPersist,}




#
def ensure(field, n, nLeft):
    if nLeft < n:
        #print "WARNING: field '%s', not enough data left (want %d, have %d). Perhaps optional field." % \
                #(field, n, nLeft)
        return False
    return True

#
def printAtom(rData, rLen, rDesc):
    
    #see if actual len is equal to real len
    if len(rData) != rLen:
        print "!!Warning: claimed len %#x (%d), actual %#x (%d)" % (rLen, rLen, len(rData), len(rData))
        rLen = len(rData)

    rFmt = rDesc[2]
    rFNames = rDesc[3]
    fieldCount = offset = 0
     
    #skip last element due to trailing '%' in format string
    for fmt in rFmt.split("%")[:-1]:
        
        nLeft = rLen - offset
        
        fieldType = rFNames[fieldCount][0]
        fieldName = rFNames[fieldCount][1]
        fieldDesc = rFNames[fieldCount][2]

        if fieldType in COMPLEX_TYPES:
            isComplex = True
        else:
            isComplex = False

        if fmt == "1":
            if ensure(fieldName, 1, nLeft):
                val = struct.unpack("B", rData[offset:offset+1])[0]
                if isComplex:
                    print "        %s.BYTE %s = %#x (%d)" % (fieldType, fieldName, val, val)
                else:
                    print "        BYTE %s = %#x (%d)" % (fieldName, val, val)
                offset += 1
        elif fmt == "2":
            if ensure(fieldName, 2, nLeft):
                val = struct.unpack("H", rData[offset:offset+2])[0]
                if isComplex:
                    print "        %s.WORD %s = %#x (%d)" % (fieldType, fieldName, val, val)
                else:
                    print "        WORD %s = %#x (%d)" % (fieldName, val, val)
                offset += 2
        elif fmt == "4":
            if ensure(fieldName, 4, nLeft):
                val = struct.unpack("I", rData[offset:offset+4])[0]
                if isComplex:
                    print "        %s.DWORD %s = %#x (%d)" % (fieldType, fieldName, val, val)
                else:
                    print "        DWORD %s = %#x (%d)" % (fieldName, val, val)
                offset += 4
        elif fmt == "s":
            print "        Field '%s' is variable length ASCIIZ, dumping rest of record:" % (fieldName)
            sys.stdout.write(hexdump(rData[offset:], indent=12))
            break
        elif fmt == "u":
            print "        Field '%s' is variable length UNICODE, dumping rest of record:" % (fieldName)
            sys.stdout.write(hexdump(rData[offset:], indent=12))
            break
        elif fmt == "v":
            print "        Field '%s' is variable length DATA, dumping rest of record:" % (fieldName)
            sys.stdout.write(hexdump(rData[offset:], indent=12))
            break
        else:
            print "ERROR:Invalid format in record format string [%s]. Developer error!!" % (f)
            sys.exit(1)
         
        fieldCount += 1

#
def getHdr(hdr):
    rVerInst, rType, rLen = struct.unpack("HHI", hdr)
    rVer = rVerInst & 0xf
    rInst = (rVerInst & 0xfff0) >> 4
    return (rVer, rInst, rType, rLen)

#
def printHdr(rVer, rInst, rType, rLen, recCount, depth, offset):

    #lookup the record
    rDesc = None
    try:
        rDesc = recDict[rType]
        rName = rDesc[0]
    except:
        rName = "Unknown"
    #
    if (rVer & 0xf) == 0xf:
        prefix = "["*depth + "Container"
    else:
        prefix = "{"*depth + "Atom"
    
    print "%s(%d) %s (%#x, %d) size %#x (%d), instance %#x version %#x [offset %#x (%d)]" % \
            (prefix,recCount,
            rName, rType, rType, rLen, rLen, rInst, rVer,
            offset, offset)

    return rDesc, rName

# print this one out by hand since we can't properly handle the length
# of the embedded strings in the autogen code
def dumpCurrentUser(buf):

    rVer, rInst, rType, rLen = getHdr(buf[:8])

    printHdr(rVer, rInst, rType, rLen, 1, 1, 0)
    
    (size, headerToken, offsetToCurrentEdit, lenUserName, docFileVersion,
            majorVersion, minorVersion, unused) = struct.unpack("IIIHHBBH", buf[8:28])
    ansiUserName = buf[28:28+lenUserName]
    relVersion = struct.unpack("I", buf[28+lenUserName:28+lenUserName+4])[0]
    uniUserName = buf[28+lenUserName+4:]
    
    print("\tDWORD size %#x (%d)\n\tDWORD headerToken %#x (%d)\n"
            "\tDWORD offsetToCurrentEdit %#x (%d)\n\tWORD lenUserName %#x (%d)\n"
            "\tWORD docFileVersion %#x (%d)\n\tBYTE majorVersion %#x (%d)\n"
            "\tBYTE minorVersion %#x (%d)\n\tWORD unused %#x (%d)\n"
            "\tASCIIZ AnsiUserName '%s'\n\tDWORD relVersion %#x (%d)\n"
            "\tUNICODE uniUserName:\n" % (
                    size, size, headerToken, headerToken, offsetToCurrentEdit,
                    offsetToCurrentEdit, lenUserName, lenUserName, docFileVersion,
                    docFileVersion, majorVersion, majorVersion, minorVersion,
                    minorVersion, unused, unused, ansiUserName,
                    relVersion, relVersion))
    print hexdump(uniUserName, indent=12)
    
# count_offset is a list with count and offset as elements
# ghetto pass by reference. sorry.
def dumpPPD(buf, maxLen, depth, count_offset, recList=None):

    nRead = 0
    while nRead  < maxLen:

        #read the header, check for atom/container
        rVer, rInst, rType, rLen = getHdr(buf[nRead:nRead + PPT_HDR_LEN])
        nRead += PPT_HDR_LEN
        
        if (rVer & 0xf) == 0xf:
            isAtom = False
            prefix = "["*depth + "Container"
        else:
            isAtom = True
            prefix = "{"*depth + "Atom"

        #try to look up record description
        try:
            rDesc = recDict[rType]
            rName = rDesc[0]
        except KeyError:
            rDesc = None
            rName = "!!!Unknown"

        #pretty print the header
        print "%s(%d) %s (%#x, %d) size %#x (%d), instance %#x version %#x [offset %#x (%d)]" % \
                (prefix, count_offset[REC_COUNT],
                rName, rType, rType, rLen, rLen, rInst, rVer,
                count_offset[REC_OFFSET], count_offset[REC_OFFSET])

        #update ghetoo reference parameters, record count and total offset
        count_offset[REC_COUNT] += 1
        count_offset[REC_OFFSET] += PPT_HDR_LEN

        if not isAtom:
            nRead += dumpPPD(buf[nRead:maxLen], min(maxLen - nRead, rLen), depth + 1, count_offset, recList)
            print "]"*depth, "End container %s" % rName
        else:

            #only save atoms
            if recList is not None:
                recList.append((rType, buf[nRead:nRead+(min(rLen, maxLen - nRead))]))

            if rDesc:
                printAtom(buf[nRead:nRead+(min(rLen, maxLen - nRead))], rLen, rDesc)

                #look for a manual rec printer
                try:
                    handler = customPrinters[rType]
                    handler(buf[nRead:nRead+(min(rLen, maxLen - nRead))])
                except KeyError:
                    pass
            else:
                print("No descriptor, dumping:\n",
                    hexdump(buf[nRead+PPT_HDR_LEN:nRead+PPT_HDR_LEN+rLen], indent=8))
            
            nRead += rLen
            count_offset[REC_OFFSET] += rLen

    return nRead

#
def dump(ole, **kwargs):

    recList = []
    
    #
    pcu = ole.openstream("Current User")
    buf = pcu.read()
    pcuLen = len(buf)
    print ("*"*80+ "\n[*]Dumping 'Current User' stream %#x (%d) bytes...\n") % (pcuLen, pcuLen)
    dumpCurrentUser(buf)

    #
    ppd = ole.openstream("PowerPoint Document")
    buf = ppd.read()
    ppdLen = len(buf)
    print ("*"*80+ "\n[*]Dumping 'PowerPoint Document' stream %#x (%d) bytes...\n") % (ppdLen, ppdLen)
    dumpPPD(buf, ppdLen, 1, [1, 0], recList)

    if "xole" in kwargs and kwargs["xole"]:
        oleCount = 0
        for (rType, rData) in recList:
            if rType == 0x1011:
                curFile = "ole_file_" + str(oleCount) + ".bin"
                dec = zlib.decompress(rData[4:])
                f = open(curFile, "wb")
                f.write(dec)
                f.close()
                print "!Extracted %d bytes of embedded OLE to file %s" % (len(dec), curFile)
                oleCount += 1
