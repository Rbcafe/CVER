#!/usr/bin/python

import sys
import struct
from util import hexdump
from util import ensure 
from xlRecs import recDict
from manualRecPrinters import extraPrinters

# when doing error recovery, the number of valid records to encounter
# before declaring successful recovery. a valid record is defined as
# one we have a handler for, and whose length is within bounds of stream
RECOVER_COUNT = 5

XL_HDRLEN = 4


#
def printRec(rType, rLen, rData, rCount, rOffset):
    
    #attempt to lookup the description for this record
    try:
        rec = recDict[rType]
        rName, rDesc, rFmt, rFNames = rec

        print "[%d]Record %s [%#x (%d)] offset %#x (%d), len %#x (%d) (%s)" % (
                rCount, rName, rType, rType, rOffset, rOffset, rLen, rLen, rDesc)
        
        fieldCount = offset = 0
        
        #skip last element due to trailing '%' in format string
        for fmt in rFmt.split("%")[:-1]:

            nLeft = rLen - offset
            fieldName = rFNames[fieldCount]

            if fmt == "1":
                if ensure(fieldName, 1, nLeft):
                    val = struct.unpack("B", rData[offset:offset+1])[0]
                    print "        BYTE %s = %#x (%d)" % (fieldName, val, val)
                    offset += 1
            elif fmt == "2":
                if ensure(fieldName, 2, nLeft):
                    val = struct.unpack("H", rData[offset:offset+2])[0]
                    print "        WORD %s = %#x (%d)" % (fieldName, val, val)
                    offset += 2
            elif fmt == "4":
                if ensure(fieldName, 4, nLeft):
                    val = struct.unpack("I", rData[offset:offset+4])[0]
                    print "        DWORD %s = %#x (%d)" % (fieldName, val, val)
                    offset += 4
            elif fmt[0] == "f":
                dataLen = int(fmt[1:])
                if dataLen > nLeft:
                    print "        Warning, field %s is longer (%d) than data left (%d). Dumping what's left:" % \
                                (fieldName, dataLen, nLeft)
                    sys.stdout.write(hexdump(rData[offset:], indent=12))
                else:
                    print "        Field %s is %#x (%d) bytes, dumping:" % (fieldName, dataLen,
                                                                        dataLen)
                    sys.stdout.write(hexdump(rData[offset:offset+dataLen], indent=12))
                
                offset += dataLen
            elif fmt == "v":
                print "        Field '%s' is variable length, dumping rest of record:" % (fieldName)
                sys.stdout.write(hexdump(rData[offset:], indent=12))
                break
            elif fmt[0] == "[":
                try:
                    handler = extraPrinters[fmt]
                    o = handler(rData[offset:], nLeft)
                    if o == -1:
                        break
                    else:
                        offset += o
                except KeyError:
                    print "Error: no handler defined for custom format '%s'" % (fmt)
            else:
                print "ERROR:Invalid format in record format string [%s]. Developer error!!" % (f)
                sys.exit(1)
            
            fieldCount += 1
    except KeyError:
        print "WARNING:No record description for id %#x (%d) len %#x (%d)" % (rType, rType, rLen, rLen)
        sys.stdout.write(hexdump(rData, indent=8))
    
    return

# attempt to recover from an invalid record length by finding the boundary of next record
# very very experimental atm
def recover(buf, wbLen, offset):

    validRecs = goodOffset = 0
    while offset + XL_HDRLEN <= wbLen and validRecs < RECOVER_COUNT:

        rType, rLen = struct.unpack("<HH", buf[offset:offset + XL_HDRLEN])
        nLeft = wbLen - offset - XL_HDRLEN

        if rLen > nLeft:
            offset += 1
        else:

            #check and see if we have a handler for this alleged record id
            try:
                rec = recDict[rType]
                if validRecs == 0:
                    goodOffset = offset
                offset += XL_HDRLEN + rLen
                validRecs += 1
            except KeyError:
                offset += 1
                validRecs = 0
        
    return validRecs == RECOVER_COUNT, goodOffset

#
def dump(ole):

    #
    wb = ole.openstream("Workbook")
    buf = wb.read()
    wbLen = len(buf)
    print ("*"*80+ "\n[*]Dumping Workbook stream %#x (%d) bytes...\n") % (wbLen, wbLen)

    bofCount = offset = count = 0
    while offset + XL_HDRLEN <= wbLen:

        rType, rLen = struct.unpack("<HH", buf[offset:offset + XL_HDRLEN])
        nLeft = wbLen - offset - XL_HDRLEN

        if rLen > nLeft:
            print "!!Invalid record length (%#x, %d) only have %#x (%d) left" % (rLen, rLen, nLeft,
                    nLeft)
            print "!!Attempting to recover from error"
            
            #assume 0 length record and advance past type/len
            oOff = offset
            success, offset = recover(buf, wbLen, offset + XL_HDRLEN)
            if success:
                print "!!Recovered from error, skipped %#x (%d) bytes\n" % (offset - oOff, offset -
                        oOff)
            else:
                print "!!Couldn't recover from length error, hexdumping rest of stream"
                sys.stdout.write(hexdump(buf[oOff:]))
                return False
        else:
            if rType == 0x809:
                bofCount += 1
                print "[ii]BOF record: current count %d" % bofCount
            elif rType == 0xa:
                bofCount -= 1
                print "[ii]EOF record: current count %d" % bofCount
            printRec(rType, rLen, buf[offset+XL_HDRLEN:offset+XL_HDRLEN+rLen], count, offset)
        
            offset += XL_HDRLEN + rLen
            count += 1

    return True
