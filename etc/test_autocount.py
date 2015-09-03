#!/bin/env dls-python2.6
from pkg_resources import require
require("cothread")
import cothread
import time
from random import random
from cothread.catools import *

P="BL11I-EA-COUNT-01"

silence_range = [0,0]
last_update = 0

def ct2_changed(val):
    global last_update
    last_update = time.time()
    if last_update > silence_range[0] and last_update < silence_range[1]:
        print "Error %f in range %s" %(last_update, silence_range)

mon = camonitor(P+".S2", ct2_changed, format=FORMAT_TIME)


while True:
    now = time.time()
    caput(P+".CNT", 1)
    silence_range = [now + 1.1, now + 10.9]
    cothread.Sleep(13)
    while last_update < now + 10.9:
        print "Error no autocount started at %f" %time.time()
        cothread.Sleep(0.1)
    cothread.Sleep(random()*5)

