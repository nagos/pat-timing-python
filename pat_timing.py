#!/usr/bin/env python3

import sys
import tsdump
import struct

FILE_1 = "record_1.ts"
FILE_2 = "record_2.ts"
PAT_PID = 0

def parse_packet(packet):
    pid = struct.unpack(">H", packet[1:3])[0] & 0x1fff
    cc = struct.unpack(">B", packet[3:4])[0] & 0x0f
    return pid, cc

def extract_pat_ts(fname):
    ret = []
    with tsdump.tsdump(fname) as d:
        for packets, ts in d.blocks():
            for packet in packets:
                pid, cc = parse_packet(packet)
                if(pid==PAT_PID and cc==0):
                    ret.append(ts)
    return ret

def main():
    PAT_TS_1 = extract_pat_ts(FILE_1)
    PAT_TS_2 = extract_pat_ts(FILE_2)
    
    pat_count = min(len(PAT_TS_1), len(PAT_TS_2))

    print("PAT timing difference (us):")
    for i in range(pat_count):
        print(tsdump.ts_to_us(PAT_TS_1[i] - PAT_TS_2[i]))

if __name__ == "__main__":
    sys.exit(main())
