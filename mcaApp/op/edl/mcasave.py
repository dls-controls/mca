#!/bin/env dls-python

# import module
from pkg_resources import require
require("cothread==2.10")
import cothread
from cothread.catools import *

import sys,os, tempfile, time
import argparse

def main():
    usage = """Stores data and settings from an EPICS MCA application"""

    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument(
            "mca_pv",
            help="The PV base name for the MCA application " + \
            "($(P) in the EDM gui). A colon ':' " + \
            "will be added if ommited")
    parser.add_argument("adc",
                        help="The ADC extension to the MCA PV " + \
                        "($(M) in the EDM gui)")
    args = parser.parse_args()
    
    # get the MCA PV
    P = args.mca_pv
    M = args.adc

    if not P.endswith(":"):
        P = P + ":"
    # first try to get the filename to store the data in
    filename = ""
    filepv = "%s%s:FILE"%(P,M)
    print "FILE PV: ", filepv
    try:
        result = caget(filepv, datatype = DBR_CHAR_STR)
        filename = str(result).replace(":","_")
    except:
        print "### ERROR: Unable to get a valid filename from PV (%s)"%(filepv)
        filename = None
        
        
    # create the first line of our file with a timestamp
    fileStr = "Logged on %s\n"%time.strftime("%a %d.%m.%Y at %H:%M")        
        
    # get the livetime, realtime and N-channels 
    # settings from the experiment
    pvs = [P+M+field for field in [".ELTM", ".PLTM", ".ERTM", ".PRTM",]]
    results = caget(pvs)
    fileStr += "\n# Livetime and realtime\n"
    for result in results:
        fileStr += "%s\t%f\n"%(result.name, result)

    # get number of elements
    fileStr += "\n# Number of elements\n"
    result = caget(P+M+".NUSE")
    fileStr += "%s\t%i\n"%(result.name, result)

    # get the amplifier setup
    fileStr += "\n# amplifier setup\n"
    results = caget([P+field for field in ["adc1GAIN", "adc1OFFSET", "adc1LLD"]], datatype = DBR_STRING)
    for result in results:
        fileStr += "%s\t%s\n"%(result.name, result)

    # get the regions of interst
    fileStr += "\n# Regions of interest\n"
    roilows = caget(["%s%s.R%iLO"%(P,M,i) for i in range(5)])
    roihighs = caget(["%s%s.R%iHI"%(P,M,i) for i in range(5)])
    rois = zip(*[roilows, roihighs])
    fileStr += "ROI\tlow\thigh\n"
    for i,roi in enumerate(rois):
        fileStr += "ROI%i\t%i\t%i\n"%(i, roi[0], roi[1])
        
    # get the data
    result = caget("%s%s.VAL"%(P,M))
    fileStr += "\n# MCA data\n"
    fileStr += "Channel\tCount\n"
    for channel, count in enumerate(result):
        fileStr += "%i\t%i\n"%(channel, count)

    print "Creating datafile: %s"%filename
    try:
        fptr = file(filename, "w")
    except:
        print "### ERROR: could not open file %s for writing."%filename
        fptr = None
        filename = None
                
    if not fptr:
        filename = tempfile.mktemp(prefix="mca_%s_"%P)
        print "Creating tmp datafile: %s"%filename
        try:
            fptr = file(filename, "w")
        except:
            print "### ERROR: could not open file %s for writing."%filename
            print "###        printing data to stdout instead\n"
            print fileStr
            fptr = None
        
    if fptr:                
        fptr.write(fileStr)
        fptr.close()
        
if __name__ == "__main__":
    main()

