#!/usr/bin/python

import OleFileIO_PL
import sys
import dumpXL
import dumpPPT
from dumpProps import dumpPropSetStream
import getopt
import util

#
def usage(prog):
    print("Usage: %s [ -f OLE file ] [ -h help ] [ -d debug ] [ -x extract stream (use -o for output file)]\n"
            "\t[ -o output file ] [ -O offset into stream (extraction) ] [ -v verbose stream dumping ]\n"
            "\t[ -X extract ole objects from ppt ]\n\n"
            "#For -x, use a Unix path to your stream: -x 'ObjectPool/_1363433832/Contents'\n"
            "#DO NOT use the 'Root Storage' in the path, it is assumed already\n"
            %
            (prog))
    sys.exit(1)

#
if __name__ == "__main__":

    extractOLE = verbose = False
    streamOffset = 0
    outputFile = fName = extractStream = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:dx:o:O:vX")
    except getopt.GetoptError, err:
        print str(err)
        usage(sys.argv[0])

    for o, a in opts:
        if o == "-h":
            usage(sys.argv[0])
        if o == "-O":
            streamOffset = int(a)
        elif o == "-x":
            extractStream = a
        elif o == "-f":
            fName = a
        elif o == "-o":
            outputFile = a
        elif o == "-v":
            verbose = True
        elif o == "-d":
            OleFileIO_PL.set_debug_mode(True)
        elif o == "-X":
            extractOLE = True
        else:
            usage(sys.argv[0])

    if not fName:
        usage(sys.argv[0])

    # Test if a file is an OLE container:
    if not OleFileIO_PL.isOleFile(fName):
        print "File %s is not an OLE file" % (fName)
        sys.exit(1)

    print "[*]Opening file %s" % (fName)

    # Open OLE file:
    ole = OleFileIO_PL.OleFileIO(fName)

    # Get list of storages/streams
    objs = ole.listdir()
    print "[*]Listing streams/storages:\n"
    ole.dumpdirectory()

    #
    if extractStream is not None:
        if outputFile is None:
            print "ERROR: extracting a stream requires output file [ -o  file ]"
            sys.exit(1)
        
        stream = ole.openstream(extractStream)
        buf = stream.read()
        outFile = open(outputFile, "wb")
        outFile.write(buf[streamOffset:])
        outFile.close()

        print "Extracted stream %s (%d of %d available bytes) to file %s" % \
                    (extractStream, len(buf) - streamOffset, len(buf), outputFile)
        sys.exit(0)

    #
    if ole.exists("Workbook"):
        print "\n[**]Detected Excel file %s" % fName
        dumpXL.dump(ole)
    
    #
    if ole.exists("PowerPoint Document"):
        print "\n[**]Detected PowerPoint file %s" % fName
        dumpPPT.dump(ole, xole=extractOLE)

    #
    if ole.exists("\x05SummaryInformation"):
        dumpPropSetStream(ole, "\x05SummaryInformation")
    
    #
    if ole.exists("\x05DocumentSummaryInformation"):
        dumpPropSetStream(ole, "\x05DocumentSummaryInformation")

    #
    if verbose:
        paths = ole.getPaths()
        for path in paths:

            #dont try to read a storage
            if path[-1] != "/":
                print "Opening %s" % (path)
                stream = ole.openstream(path)
                buf = stream.read()
                sys.stdout.write(util.hexdump(buf, indent=4))
