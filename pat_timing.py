#!/usr/bin/env python3

import sys
import tsdump
import struct
from optparse import OptionParser

FILE_1 = "record_1.ts"
FILE_2 = "record_2.ts"
PAT_PID = 0

def parse_packet(packet):
    pid = struct.unpack(">H", packet[1:3])[0] & 0x1fff
    cc = struct.unpack(">B", packet[3:4])[0] & 0x0f
    return pid, cc

def extract_ts_packets(block):
    for packets, ts in block:
        for packet in packets:
            pid, cc = parse_packet(packet)
            if(pid==PAT_PID and cc==0):
                yield(ts)

def process(f1, f2, small):
    TS_1 = tsdump.tsdump(f1, small)
    TS_2 = tsdump.tsdump(f2, True)
    it = zip(extract_ts_packets(TS_1.blocks()), extract_ts_packets(TS_2.blocks()))
    for x in it:
        yield(tsdump.ts_to_us(x[0] - x[1]))

def main():
    parser = OptionParser()
    parser.add_option("-s", action="store_true", dest="small", default=False,
                  help="header only dump")
    (options, args) = parser.parse_args()

    with open(FILE_1, "rb") as f1, open(FILE_2, "rb") as f2:
        for i in process(f1, f2, options.small):
            print(i)

if __name__ == "__main__":
    sys.exit(main())
