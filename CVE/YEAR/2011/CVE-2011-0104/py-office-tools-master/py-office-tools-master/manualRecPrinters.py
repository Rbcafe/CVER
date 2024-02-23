#!/usr/bin/python

import struct
from util import hexdump
from util import printFmt

#i hacked this together on a whim to add some extra support, it's not pretty

#
# an object record consists of tlv data in teh same format as a normal excel record
# 2 bytes type
# 2 bytes len
# 'len' bytes data
# the following dictionary contains the basic subtypes, there are more sub-subtypes

#
def getCmoFlagStr(flags):

    flagStr = ""

    if flags & 1:
        flagStr += "|fLocked"
    if flags & 0x10:
        flagStr += "|fPrint"
    if flags & 0x20:
        flagStr += "|fHaveMaster"
    if flags & 0x2000:
        flagStr += "|fAutoFill"
    if flags & 0x4000:
        flagStr += "|fAutoLine"

    return flagStr

#
ftCmoTypeMap = {
0x0:"Group",
0x1:"Line",
0x2:"Rectangle",
0x3:"Oval",
0x4:"Arc",
0x5:"Chart",
0x6:"Text",
0x7:"Button",
0x8:"Picture",
0x9:"Polygon",
0xA:"(Reserved)",
0xB:"Check box",
0xC:"Option button",
0xD:"Edit box",
0xE:"Label",
0xF:"Dialog box",
0x10:"Spinner",
0x11:"Scroll bar",
0x12:"List box",
0x13:"Group box",
0x14:"Combo box",
0x15:"(Reserved)",
0x16:"(Reserved)",
0x17:"(Reserved)",
0x18:"(Reserved)",
0x19:"Comment",
0x1A:"(Reserved)",
0x1B:"(Reserved)",
0x1C:"(Reserved)",
0x1D:"(Reserved)",
0x1E:"Microsoft Office drawing",
}

def cmoPrinter(data, dLen, depth):

    if dLen != 0x12:
        print "Warning: ftCmo length (%d) != 0x12" % (dLen)
        return
    
    ot, oid, grbit, res1, res2, res3 = struct.unpack("<HHHLLL", data[:0x12])
    try:
        ots = ftCmoTypeMap[ot]
    except KeyError:
        ots = "UNDEF"

    print(" "*(depth*4) +
        "ftCmo.ot %#x (%s), ftCmo.id %#x (%d), ftCmo.grbit %#x (%s), ftCmo.res %#x.%#x.%#x" %
        (ot, ots, oid, oid, grbit, getCmoFlagStr(grbit), res1, res2, res3)
    )

#
objSubTypeMap = {
        0x00:["ftEnd", "End of OBJ Record", None],
        0x01:["(Reserved)", "(Reserved)", None],
        0x02:["(Reserved)", "(Reserved)", None],
        0x03:["(Reserved)", "(Reserved)", None],
        0x04:["ftMacro", "Fmla-style macro", None],
        0x05:["ftButton", "Command button", None],
        0x06:["ftGmo", "Group Marker", None],
        0x07:["ftCf", "Clipboard format", None],
        0x08:["ftPioGrbit", "Picture option flags", None],
        0x09:["ftPictFmla", "Picture fmla-style macro", None],
        0x0a:["ftCbls", "Checkboxlink", None],
        0x0b:["ftRbo", "Radio button", None],
        0x0c:["ftSbs", "Scroll bar", None],
        0x0d:["ftNts", "Note structure", None],
        0x0e:["ftSbsFmla", "Scroll bar fmla-style macro", None],
        0x0f:["ftGboData", "Group box data", None],
        0x10:["ftEdoData", "Edit control data", None],
        0x11:["ftRboData", "Radio button data", None],
        0x12:["ftCblsData", "Check box data", None],
        0x13:["ftLbsData", "List box data", None],
        0x14:["ftCblsFmla", "Check box link fmla-style macro", None],
        0x15:["ftCmo", "Common object data", cmoPrinter],
        }

def objSubPrinter(data, dLen, depth=2):

    off = 0
    while off <= dLen - 4:
        t, l = struct.unpack("<HH", data[off:off+4])
        try:
            desc = objSubTypeMap[t]
            print("        Subtype %s [%#x (%d)] offset %#x, len %#x (%d) (%s)" %
                    (desc[0], t, t, off, l, l, desc[1]))
            
            lenLeft = min(l, dLen - off - 4)
            
            if desc[2]:
                desc[2](data[off+4:off+4+lenLeft], lenLeft, depth + 1)
            else:
                print hexdump(data[off+4:off+4+lenLeft], indent=(depth + 1)*4),
        except KeyError:
            print "        obj.subtype %#x (%d) obj.sublen %#x (%d)" % (t, t, l, l)
        off += l + 4
    return -1

#
def optPrinter(data, dLen, propCount, depth):
    
    cProps = []
    off = 0
    
    #first we have an array of property descriptors packed together
    while off <= dLen - 6 and propCount > 0:
        try:
            pff, op = struct.unpack("<HL", data[off:off+6])
        except struct.error:
            return

        pid = pff & 0x3fff
        fBid = (pff & 0x4000) >> 14
        fComplex = (pff & 0x8000) >> 15

        #op contains the length
        if fComplex:
            cProps.append((op, pid))

        print(" "*(depth*4) + "Prop ID %#x (%d), Blip ID %#x (%d), Complex %#x, Op %#x (%#d)" %
                        (pid, pid, fBid, fBid, fComplex, op, op))
        
        off += 6
        propCount -= 1

    #dump the data for any complex properties
    if off < dLen:

        print("\n" + " "*(depth*4) + "Dumping data for %d complex props\n" % len(cProps))

        for (cLen, pid) in cProps:

            if off + cLen > dLen:
                print "Warning: breaking early, not enough to print remaining props"
                break
            
            lenLeft = min(cLen, dLen - off)
            print(" "*(depth*4) + "Dumping property %#x (%d)...\n" % (pid, pid))
            print hexdump(data[off:off+lenLeft], indent=(depth)*4)

            off += cLen

#
shapeTypeMap = {
0:"msosptMin",
1:"msosptRectangle",
2:"msosptRoundRectangle",
3:"msosptEllipse",
4:"msosptDiamond",
5:"msosptIsocelesTriangle",
6:"msosptRightTriangle",
7:"msosptParallelogram",
8:"msosptTrapezoid",
9:"msosptHexagon",
10:"msosptOctagon",
11:"msosptPlus",
12:"msosptStar",
13:"msosptArrow",
14:"msosptThickArrow",
15:"msosptHomePlate",
16:"msosptCube",
17:"msosptBalloon",
18:"msosptSeal",
19:"msosptArc",
20:"msosptLine",
21:"msosptPlaque",
22:"msosptCan",
23:"msosptDonut",
24:"msosptTextSimple",
25:"msosptTextOctagon",
26:"msosptTextHexagon",
27:"msosptTextCurve",
28:"msosptTextWave",
29:"msosptTextRing",
30:"msosptTextOnCurve",
31:"msosptTextOnRing",
32:"msosptStraightConnector1",
33:"msosptBentConnector2",
34:"msosptBentConnector3",
35:"msosptBentConnector4",
36:"msosptBentConnector5",
37:"msosptCurvedConnector2",
38:"msosptCurvedConnector3",
39:"msosptCurvedConnector4",
40:"msosptCurvedConnector5",
41:"msosptCallout1",
42:"msosptCallout2",
43:"msosptCallout3",
44:"msosptAccentCallout1",
45:"msosptAccentCallout2",
46:"msosptAccentCallout3",
47:"msosptBorderCallout1",
48:"msosptBorderCallout2",
49:"msosptBorderCallout3",
50:"msosptAccentBorderCallout1",
51:"msosptAccentBorderCallout2",
52:"msosptAccentBorderCallout3",
53:"msosptRibbon",
54:"msosptRibbon2",
55:"msosptChevron",
56:"msosptPentagon",
57:"msosptNoSmoking",
58:"msosptSeal8",
59:"msosptSeal16",
60:"msosptSeal32",
61:"msosptWedgeRectCallout",
62:"msosptWedgeRRectCallout",
63:"msosptWedgeEllipseCallout",
64:"msosptWave",
65:"msosptFoldedCorner",
66:"msosptLeftArrow",
67:"msosptDownArrow",
68:"msosptUpArrow",
69:"msosptLeftRightArrow",
70:"msosptUpDownArrow",
71:"msosptIrregularSeal1",
72:"msosptIrregularSeal2",
73:"msosptLightningBolt",
74:"msosptHeart",
75:"msosptPictureFrame",
76:"msosptQuadArrow",
77:"msosptLeftArrowCallout",
78:"msosptRightArrowCallout",
79:"msosptUpArrowCallout",
80:"msosptDownArrowCallout",
81:"msosptLeftRightArrowCallout",
82:"msosptUpDownArrowCallout",
83:"msosptQuadArrowCallout",
84:"msosptBevel",
85:"msosptLeftBracket",
86:"msosptRightBracket",
87:"msosptLeftBrace",
88:"msosptRightBrace",
89:"msosptLeftUpArrow",
90:"msosptBentUpArrow",
91:"msosptBentArrow",
92:"msosptSeal24",
93:"msosptStripedRightArrow",
94:"msosptNotchedRightArrow",
95:"msosptBlockArc",
96:"msosptSmileyFace",
97:"msosptVerticalScroll",
98:"msosptHorizontalScroll",
99:"msosptCircularArrow",
100:"msosptNotchedCircularArrow",
101:"msosptUturnArrow",
102:"msosptCurvedRightArrow",
103:"msosptCurvedLeftArrow",
104:"msosptCurvedUpArrow",
105:"msosptCurvedDownArrow",
106:"msosptCloudCallout",
107:"msosptEllipseRibbon",
108:"msosptEllipseRibbon2",
109:"msosptFlowChartProcess",
110:"msosptFlowChartDecision",
111:"msosptFlowChartInputOutput",
112:"msosptFlowChartPredefinedProcess",
113:"msosptFlowChartInternalStorage",
114:"msosptFlowChartDocument",
115:"msosptFlowChartMultidocument",
116:"msosptFlowChartTerminator",
117:"msosptFlowChartPreparation",
118:"msosptFlowChartManualInput",
119:"msosptFlowChartManualOperation",
120:"msosptFlowChartConnector",
121:"msosptFlowChartPunchedCard",
122:"msosptFlowChartPunchedTape",
123:"msosptFlowChartSummingJunction",
124:"msosptFlowChartOr",
125:"msosptFlowChartCollate",
126:"msosptFlowChartSort",
127:"msosptFlowChartExtract",
128:"msosptFlowChartMerge",
129:"msosptFlowChartOfflineStorage",
130:"msosptFlowChartOnlineStorage",
131:"msosptFlowChartMagneticTape",
132:"msosptFlowChartMagneticDisk",
133:"msosptFlowChartMagneticDrum",
134:"msosptFlowChartDisplay",
135:"msosptFlowChartDelay",
136:"msosptTextPlainText",
137:"msosptTextStop",
138:"msosptTextTriangle",
139:"msosptTextTriangleInverted",
140:"msosptTextChevron",
141:"msosptTextChevronInverted",
142:"msosptTextRingInside",
143:"msosptTextRingOutside",
144:"msosptTextArchUpCurve",
145:"msosptTextArchDownCurve",
146:"msosptTextCircleCurve",
147:"msosptTextButtonCurve",
148:"msosptTextArchUpPour",
149:"msosptTextArchDownPour",
150:"msosptTextCirclePour",
151:"msosptTextButtonPour",
152:"msosptTextCurveUp",
153:"msosptTextCurveDown",
154:"msosptTextCascadeUp",
155:"msosptTextCascadeDown",
156:"msosptTextWave1",
157:"msosptTextWave2",
158:"msosptTextWave3",
159:"msosptTextWave4",
160:"msosptTextInflate",
161:"msosptTextDeflate",
162:"msosptTextInflateBottom",
163:"msosptTextDeflateBottom",
164:"msosptTextInflateTop",
165:"msosptTextDeflateTop",
166:"msosptTextDeflateInflate",
167:"msosptTextDeflateInflateDeflate",
168:"msosptTextFadeRight",
169:"msosptTextFadeLeft",
170:"msosptTextFadeUp",
171:"msosptTextFadeDown",
172:"msosptTextSlantUp",
173:"msosptTextSlantDown",
174:"msosptTextCanUp",
175:"msosptTextCanDown",
176:"msosptFlowChartAlternateProcess",
177:"msosptFlowChartOffpageConnector",
178:"msosptCallout90",
179:"msosptAccentCallout90",
180:"msosptBorderCallout90",
181:"msosptAccentBorderCallout90",
182:"msosptLeftRightUpArrow",
183:"msosptSun",
184:"msosptMoon",
185:"msosptBracketPair",
186:"msosptBracePair",
187:"msosptSeal4",
188:"msosptDoubleWave",
189:"msosptActionButtonBlank",
190:"msosptActionButtonHome",
191:"msosptActionButtonHelp",
192:"msosptActionButtonInformation",
193:"msosptActionButtonForwardNext",
194:"msosptActionButtonBackPrevious",
195:"msosptActionButtonEnd",
196:"msosptActionButtonBeginning",
197:"msosptActionButtonReturn",
198:"msosptActionButtonDocument",
199:"msosptActionButtonSound",
200:"msosptActionButtonMovie",
201:"msosptHostControl",
202:"msosptTextBox",
203:"msosptMax",
0xffff:"msosptNil",
}

#
def getFlagStr(flags):

    flagStr = ""

    if flags & 1:
        flagStr += "|fGroup"
    if flags & 2:
        flagStr += "|fChild"
    if flags & 4:
        flagStr += "|fPatriarch"
    if flags & 8:
        flagStr += "|fDeleted"
    if flags & 0x10:
        flagStr += "|fOleShape"
    if flags & 0x20:
        flagStr += "|fHaveMaster"
    if flags & 0x40:
        flagStr += "|fFlipH"
    if flags & 0x80:
        flagStr += "|fFlipV"
    if flags & 0x100:
        flagStr += "|fConnector"
    if flags & 0x200:
        flagStr += "|fHaveAnchor"
    if flags & 0x400:
        flagStr += "|fHaveBackground"
    if flags & 0x800:
        flagStr += "|fHaveSpt"
    if flags & 0xfffff000:
        flagStr += "|RESERVED!!"

    return flagStr

#
def spPrinter(data, dLen, shapeType, depth):
    if dLen != 8:
        print "Warning: msofbtSp length (%d) != 8" % (dLen)
    else:
        spid, flags = struct.unpack("<LL", data[:8])
        try:
            sTypeStr = shapeTypeMap[shapeType]
        except KeyError:
            sTypeStr = "UNDEF"

        print(" "*(depth*4) + "Shape type %#x (%s), id %#x (%d), flags %#x (%s)" %
                    (shapeType, sTypeStr, spid, spid, flags, getFlagStr(flags)))

#
def dgPrinter(data, dLen, did, depth):
    if dLen != 8:
        print "Warning: msofbtDg length (%d) != 8" % (dLen)
    else:
        csp, spidCur = struct.unpack("<LL", data[:8])

        print(" "*(depth*4) +
                "Drawing group id %#x (%d),  # shapes %#x (%d), last spid %#x (%d)" %
                (did, did, csp, csp, spidCur, spidCur))


#
def dggPrinter(data, dLen, dummy, depth):
    if dLen < 0x10:
        print "Warning: msofbtDgg length (%d) < 0x10" % (dLen)
        return

    spidMax, cidcl, cspSaved, cdgSaved = struct.unpack("<LLLL", data[:0x10])

    print(" "*(depth*4) +
    "Max ShapeID %#x (%d), FIDCL count %#x (%d), # saved shapes %#x (%d), # saved drawings %#x (%d)" %
                    (spidMax, spidMax, cidcl, cidcl, cspSaved, cspSaved, cdgSaved, cdgSaved)
                    )

    #the spec seems to be wrong, cidcl == cluster size + 1 ??
    print " "*(depth*4) + "Dumping File ID Cluster Table w/ %d entries.." % (cidcl - 1)
    off = 16
    i = 1
    
    while off <= dLen - 8 and cidcl - 1 > 0:
        try:
            dgid, cspidCur = struct.unpack("<LL", data[off:off+8])
        except struct.error:
            print "Warning: Can't unpack next dgid,cspidCur pair\nMaybe CONTINUE record?"
            return

        print(" "*((depth+1)*4) + "%d) dgid %#x (%d), #spids used %#x (%d)" %
                (i, dgid, dgid, cspidCur, cspidCur))
        off += 8
        cidcl -= 1
        i += 1

    if off != dLen:
        print "Warning: off/Dlen mismatch %d/%d" % (off, dLen)

#
msoDrawTypeMap = {
        0xf000:["msofbtDggContainer", "per document data", None],
        0xf001:["msofbtBstoreContainer", "all images in the document", None],
        0xf002:["msofbtDgContainer", "per sheet/page/slide data", None],
        0xf003:["msofbtSpgrContainer", "several SpContainers, the first of which is the group shape itself", None],
        0xf004:["msofbtSpContainer", "a shape", None],
        0xf005:["msofbtSolverContainer", "the rules governing shapes", None],
        0xf006:["msofbtDgg", "an FDGG and several FIDCLs", dggPrinter],
        0xf007:["msofbtBSE", "an FBSE", None],
        0xf008:["msofbtDg", "an FDG", dgPrinter],
        0xf009:["msofbtSpgr", "an FSPGR", ["4%4%4%4%", ["left", "top", "right", "bottom"]]],
        0xf00a:["msofbtSp", "an FSP", spPrinter],
        0xf00b:["msofbtOPT", "a shape property table", optPrinter],
        0xf00c:["msofbtTextbox", "RTF Text", None],
        0xf00d:["msofbtClientTextbox", "the host defined text in textbox", None],
        0xf00e:["msofbtAnchor", "a RECT, in 100000ths of an inch", ["4%4%4%4%", ["left", "top", "right", "bottom"]]],
        0xf00f:["msofbtChildAnchor", "a RECT, in parent relative units", ["4%4%4%4%", ["left", "top", "right", "bottom"]]],
        0xf010:["msofbtClientAnchor", "shape location, host defined format", None],
        0xf011:["msofbtClientData", "host specific data", None],
        0xf012:["msofbtConnectorRule", "an FConnector Rule", ["4%4%4%4%4%4%", ["ruid", "spidA",
            "spidB", "spidC", "cptiA", "cptiB"]]],
        0xf013:["msofbtAlignRule", "an FAlignRule", ["4%4%4%", ["ruid", "align", "cProxies"]]],
        0xf014:["msofbtArcRule", "an FArcRule", ["4%4%", ["ruid", "spid"]]],
        0xf015:["msofbtClientRule", "host defined rule", None],
        0xf015:["msofbtCLSID", "CLSID of app that put data on clipboard", ["4%4%4%4%", ["c1", "c2", "c3", "c4"]]],
        0xf017:["msofbtCalloutRule", "an FCORU", ["4%4%", ["ruid", "spid"]]],
        0xf118:["msofbtRegroupItems", "several FRITs", None],
        0xf11d:["msofbtDeletedPspl", "an FPSPL", None],
        0xf11e:["msofbtSplitMenuColors", "the colors in the top-level split menus", None],
        0xf11f:["msofbtOleObject", "a serialized IStorage for an object", None],
        0xf120:["msofbtColorScheme", "the colors of the source host's color scheme", None],
        0xf121:["msofbtSecondaryOPT", "a shape property table", optPrinter],
        0xf122:["msofbtTertiaryOPT", "a shape property table", optPrinter],
}

#
def msoDrawPrinter(data, dLen, depth=2):
    off = 0
    while off <= dLen - 8:
        try:
            vif, l = struct.unpack("<LL", data[off:off+8])
        except struct.error:
            return

        ver = vif & 0xf
        inst = (vif & 0xfff0) >> 4
        fbt = (vif & 0xffff0000) >> 16

        try:
            desc = msoDrawTypeMap[fbt]
            print(" "*(depth*4) + "Subtype %s [%#x (%d)] ver %#x inst %#x offset %#x, len %#x (%d) (%s)" %
                    (desc[0], fbt, fbt, ver, inst, off, l, l, desc[1]))
            if ver == 0xf:
                msoDrawPrinter(data[off+8:off+8+l], l, depth + 1)
            else:

                #CONTINUE records can make the actual length of the property span across
                #multiple records, which we don't currently support, so we chop it at what
                #we have left in the current record
                lenLeft = min(l, dLen - off - 8)
                if lenLeft != l:
                    print "!!Warning, data chopped short, wanted %d, got %d, CONTINUE rec?" % \
                            (l, lenLeft)
                
                #print out sub-record data with custom printer if available
                if desc[2]:
                    if isinstance(desc[2],  list):
                        printFmt(data[off+8:off+8+lenLeft], lenLeft, desc[2][0], desc[2][1], depth + 1)
                    elif callable(desc[2]):
                        desc[2](data[off+8:off+8+lenLeft], lenLeft, inst, depth + 1)
                else:
                    print hexdump(data[off+8:off+8+lenLeft], indent=(depth + 1)*4),
        except KeyError:
            print " "*(depth*4) + "obj.subtype %#x (%d) ver %#x inst %#x obj.sublen %#x (%d)" % \
                        (fbt, fbt, ver, inst, l, l)
            print hexdump(data[off+8:min(off+8+l, dLen - 8)], indent=(depth + 1)*4),
        off += l + 8
    return -1

#
extraPrinters = {
        "[obj]":objSubPrinter,
        "[msodrawing]":msoDrawPrinter,
}
