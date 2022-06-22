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

def extract_pat_ts(fname, header_only):
    ret = []
    with tsdump.tsdump(fname, header_only) as d:
        for packets, ts in d.blocks():
            for packet in packets:
                pid, cc = parse_packet(packet)
                if(pid==PAT_PID and cc==0):
                    ret.append(ts)
    return ret

def main():
    parser = OptionParser()
    parser.add_option("-s", action="store_true", dest="small", default=False,
                  help="header only dump")
    (options, args) = parser.parse_args()

    PAT_TS_1 = extract_pat_ts(FILE_1, options.small)
    PAT_TS_2 = extract_pat_ts(FILE_2, options.small)
    
    pat_count = min(len(PAT_TS_1), len(PAT_TS_2))

    print("PAT timing difference (us):")
    for i in range(pat_count):
        print(tsdump.ts_to_us(PAT_TS_1[i] - PAT_TS_2[i]))

if __name__ == "__main__":
    sys.exit(main())
