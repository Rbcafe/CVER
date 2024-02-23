#!/usr/bin/python

import sys
import BeautifulSoup


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

        rows = table.findAll("tr")
        
        #record name/desc/id
        rName = rows[0].contents[0].string.strip()
        rDesc= rows[0].contents[1].string.strip()
        rId = int(rows[0].contents[2].string.strip(), 0x10)

        #field members
        #print "Record " + rName
        fmt = ""
        names = []
        for field in rows[1:]:
            cols = field.findAll("td")
            #print cols
            try:
                offset = cols[0].string.strip()
            except:
                offset = "unknown"
            try:
                name = cols[1].string.strip()
            except:
                name = "???"
            try:
                sz = cols[2].string.strip()
            except:
                sz = "var"
            try:
                desc = cols[3].string.strip()
            except:
                desc = ""

            names.append(name)
            if sz in ["1", "2", "4"]:
                fmt += sz
            elif sz == "var":
                fmt += "v"
            else:
                fmt += "f" + sz
            fmt += "%"

        print "recDict[%#x] = [\"%s\", \"%s\", \"%s\", %s]" % (rId, rName, rDesc, fmt, names)
