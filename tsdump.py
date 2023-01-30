import struct

BLOCK_SIZE = 7
PACKET_SIZE = 188
HEADER_SIZE = 4
BLOCK_SIZE_BYTES = BLOCK_SIZE*PACKET_SIZE+4
BLOCK_HEADER_SIZE_BYTES = BLOCK_SIZE*HEADER_SIZE+4
MAX_TS  = 0x7FFFFFF

def ts_diff(ts1, ts2):
    d = ts1 - ts2
    if (d > (MAX_TS+1)/2):
        d -=(MAX_TS+1)
    if (d < -(MAX_TS+1)/2):
        d +=(MAX_TS+1)
    return d

class tsdump:
    def __init__(self, f, header_only=False):
        self.f = f
        self.ts = 0
        self.ts_prev = 0
        self.ts_init = 1
        self.header_only = header_only

    def process_block(self, block):
        if(not self.header_only):
            packets = [block[i: i+PACKET_SIZE] for i in range(0, BLOCK_SIZE*PACKET_SIZE, PACKET_SIZE)]
        else:
            packets = [block[i: i+HEADER_SIZE] for i in range(0, BLOCK_SIZE*HEADER_SIZE, HEADER_SIZE)]
        ts_bytes = block[-4:]
        ts = struct.unpack(">I", ts_bytes)[0]&MAX_TS
        if(self.ts_init):
            self.ts_prev = ts
            self.ts = ts
            self.ts_init = 0
        self.ts += ts_diff(ts, self.ts_prev)
        self.ts_prev = ts
        return packets, self.ts

    def blocks(self):
        while True:
            if(not self.header_only):
                data = self.f.read(BLOCK_SIZE_BYTES)
                if(len(data) != BLOCK_SIZE_BYTES):
                    break
            else:
                data = self.f.read(BLOCK_HEADER_SIZE_BYTES)
                if(len(data) != BLOCK_HEADER_SIZE_BYTES):
                    break
            yield self.process_block(data)
    
def ts_to_us(ts):
    return (ts * 1000000) // 75000000
