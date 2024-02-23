#!/usr/bin/python

import sys
import re
import BeautifulSoup

#
typeDict = {
    #primitiv%e types
    'uint4':'4%', 'sint4':'4%', 'var':'v%', 'ubyte1':'1%', 'ubyte':'1%', 'sbyte1':'1%', 'sint2':'2%',
    'uint2':'2%', 'bool1':'1%', 'string':'s%', 'wstring':'u%',
    #complex types
    'CF Run':"4%2%2%2%2%2%2%2%1%1%1%1%",
    'PF Run':"2%4%2%2%2%2%1%1%1%1%2%2%2%2%2%2%2%2%2%2%2%2%2%",
    'SI Run':"4%2%2%2%",
    'CF2002 Run':"4%2%2%4%",
    'SI2003 Run':"4%4%4%4%",
    'PF2000 Run':"4%2%2%v%",
    'CF2000 Run':"4%4%",
    'SI2000 Run':"4%4%2%",
    'tabStops':"2%2%2%",
    'GrColorAtom':"1%1%1%1%",
    'ColorEntry[]':"2%2%2%2%1%1%2%2%2%2%",
    'PSR_GPointAtom':"4%4%",
    'PSR_DateTimeAtom':"4%1%",
    'GRatioAtom':"4%4%",
    'PSR_GScalingAtom':"4%4%4%4%",
    'GPointAtom':"4%4%",
    'PSR_GRatioAtom':"4%4%"
}


#
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: %s [ record HTML file ]"
        sys.exit(1)

    htmlFile = sys.argv[1]
    f = open(htmlFile, "rb")
    html = f.read()
    f.close()
    soup = BeautifulSoup.BeautifulSoup(html)

    #
    tables = soup.findAll("table")

    for table in tables:

        firstRow = 2
        rows = table.findAll("tr")
        
        #record name/desc/id
        rName = rows[0].contents[0].string.strip()
        rId = int(rows[0].contents[1].string.strip(), 0)
        rKind = rows[0].contents[2].string.strip()
        if rKind == "atom":
            atom = True
        elif rKind == "cont":
            atom = False
            firstRow = 1
        else:
            print "ERROR in record kind %s" % rKind
            sys.exit(1)

        #field members
        #print "Record " + rName
        fmt = ""
        names = []
        for field in rows[firstRow:]:
            
            cols = field.findAll("td")

            if atom:
                fType = cols[0].string.strip()

                #get type format string
                try:
                    fieldFmt = typeDict[fType]
                except:
                    m = re.match("(\w+)\[(\d+)\]", fType)
                    if m:
                        aType = m.group(1)
                        aCount = m.group(2)
                        try:
                            fieldFmt = typeDict[aType]*int(aCount)
                        except:
                            print "ERROR: can't find type %s in dict" % fType
                            raise
                    else:
                        print "ERROR: can't find type %s in dict" % fType
                        raise
                fName = cols[1].string.strip()
                try:
                    fDesc = cols[2].string.strip()
                except:
                    fDesc = "Unknown"
                #names.append(fType + "__" + fName + "__" + fDesc)
                #names.append("(\"%s\", \"%s\", \"%s\")" % (fType, fName, fDesc))

                #
                repeat = len(fieldFmt) / 2
                names.append((fType, fName, fDesc))
                for i in xrange(1, repeat):
                    names.append((fType, fName + "." + str(i), fDesc))
                fmt += fieldFmt
            else:
                subType = cols[0].string.strip()
                subInst = cols[1].string.strip()
                try:
                    subVer = cols[2].string.strip()
                except:
                    subVer = "0"
                names.append((subType, int(subInst), int(subVer)))
                #names.append("(\"%s\", %s, %s)" % (subType, subInst, subVer))

        print "recDict[%#x] = [\"%s\", %s, \"%s\", %s]" % (rId, rName, str(atom), fmt, names)
