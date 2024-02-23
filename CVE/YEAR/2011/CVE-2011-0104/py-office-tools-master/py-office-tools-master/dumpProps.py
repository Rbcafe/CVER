#!/usr/bin/python
from util import hexdump
import struct
import binascii


#property set values
propTypes = {}
propTypes[0] = "VT_EMPTY"
propTypes[1] = "VT_NULL"
propTypes[2] = "VT_I2"
propTypes[3] = "VT_I4"
propTypes[4] = "VT_R4"
propTypes[5] = "VT_R8"
propTypes[6] = "VT_CY"
propTypes[7] = "VT_DATE"
propTypes[8] = "VT_BSTR"
propTypes[9] = "VT_DISPATCH"
propTypes[10] = "VT_ERROR"
propTypes[11] = "VT_BOOL"
propTypes[12] = "VT_VARIANT"
propTypes[13] = "VT_UNKNOWN"
propTypes[14] = "VT_DECIMAL"
propTypes[16] = "VT_I1"
propTypes[17] = "VT_UI1"
propTypes[18] = "VT_UI2"
propTypes[19] = "VT_UI4"
propTypes[20] = "VT_I8"
propTypes[21] = "VT_UI8"
propTypes[22] = "VT_INT"
propTypes[23] = "VT_UINT"
propTypes[24] = "VT_VOID"
propTypes[25] = "VT_HRESULT"
propTypes[26] = "VT_PTR"
propTypes[27] = "VT_SAFEARRAY"
propTypes[28] = "VT_CARRAY"
propTypes[29] = "VT_USERDEFINED"
propTypes[30] = "VT_LPSTR"
propTypes[31] = "VT_LPWSTR"
propTypes[36] = "VT_RECORD"
propTypes[37] = "VT_INT_PTR"
propTypes[38] = "VT_UINT_PTR"
propTypes[64] = "VT_FILETIME"
propTypes[65] = "VT_BLOB"
propTypes[66] = "VT_STREAM"
propTypes[67] = "VT_STORAGE"
propTypes[68] = "VT_STREAMED_OBJECT"
propTypes[69] = "VT_STORED_OBJECT"
propTypes[70] = "VT_BLOB_OBJECT"
propTypes[71] = "VT_CF"
propTypes[72] = "VT_CLSID"
propTypes[73] = "VT_VERSIONED_STREAM"
propTypes[0xfff] = "VT_BSTR_BLOB"

VT_VECTOR = 0x1000
VT_ARRAY = 0x2000
VT_BYREF = 0x4000
VT_RESERVED = 0x8000

#
def clsidStr(clsid):
    return binascii.hexlify(clsid)

#
def dumpPropSetStream(ole, streamName):
        
    stream = ole.openstream(streamName)
    data = stream.read()
    dLen = len(data)
    if streamName[0] == "\x05":
        streamName = "\\x05" + streamName[1:]

    print "*"*80, "\n[*]Dumping '%s' stream %#x (%d) bytes\n" % (streamName, dLen, dLen)
    
    #get the header
    (wByteOrder, wFormat, dwOsVer, clsid, cSections) = struct.unpack("HHI16sI", data[:28])
    curOffset = 28
    
    print "\nDumping property set header:\n"
    print "wByteOrder %#hx, wFormat %#hx, dwOsVer %#x" % (wByteOrder, wFormat, dwOsVer)
    print "CLSID [%s] cSections %#x (%d)\n" % (clsidStr(clsid), cSections, cSections)

    #get each section header
    sections = []
    for i in xrange(cSections):
        
        #fmtid/offset
        (fmtid, dwOffset) = struct.unpack("16sI", data[curOffset:curOffset + 20])
        sections.append((fmtid, dwOffset))
        curOffset += 20
     
    #for each section
    print "Dumping sections:\n"
    for (sectionID, sectionOffset) in sections:
        
        props = []
        (cbSection, cProps) = struct.unpack("II", data[sectionOffset:sectionOffset + 8])
        print "Section\tFMTID [%s] sectionOffset %#x (%d)" % (clsidStr(fmtid), sectionOffset, sectionOffset)
        print "\tcbSection %#x (%d) cProps %#x (%d)" % (cbSection, cbSection, cProps, cProps)

        #get the offset/length of each property
        curOffset = sectionOffset + 8
        last = None
        for i in xrange(cProps):
        
            (propid, offset) = struct.unpack("II", data[curOffset:curOffset + 8])
        
            cur = [propid, offset]
            props.append(cur)

            #fill in length of last property
            if last:
                last.append(offset - last[1])
            last = cur
            curOffset += 8

        #fill in the last offset
        last.append(len(data) - sectionOffset - last[1])

        #display the properties
        for prop in props:
            pId = prop[0]
            pOff = prop[1]
            pSz = prop[2]

            #take into account the section start
            realOffset = pOff + sectionOffset
            pType = struct.unpack("I", data[realOffset:realOffset + 4])[0]
            try:
                origType = pType
                pType = pType & 0xfff
                pName = ""
                if pType & VT_VECTOR:
                    pName = "VECTOR|"
                    pType &= ~VT_VECTOR
                if pType & VT_ARRAY:
                    pName = "ARRAY|"
                    pType &= ~VT_ARRAY
                if pType & VT_BYREF:
                    pName = "BYREF|"
                    pType &= ~VT_BYREF
                if pType & VT_RESERVED:
                    pName = "RESERVED|"
                    pType &= ~VT_RESERVED
                pName += propTypes[pType]
            except KeyError:
                pName = "!!UNKNOWN"
            
            print "    Prop ID %#x (%d) Masked Type %#x (%s) (Orig Type %#x), offset %#x (%d) size %#x (%d)" % \
                    (pId, pId, pType, pName, origType, pOff, pOff, pSz, pSz)
            pData = data[realOffset + 4:realOffset + 4 + pSz - 4]
            print hexdump(pData, indent=8)


