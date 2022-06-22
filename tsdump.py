import struct

BLOCK_SIZE = 7
PACKET_SIZE = 188
BLOCK_SIZE_BYTES = BLOCK_SIZE*PACKET_SIZE+4
MAX_TS  = 0x7FFFFFF

class tsdump:
    def __init__(self, fname):
        self.fname = fname
        self.ts = 0
        self.ts_prev = 0
        self.ts_init = 1

    def __enter__(self):
        self.f = open(self.fname, "rb")
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()
    
    def ts_diff(self, ts1, ts2):
        d = ts1 - ts2
        if (d > (MAX_TS+1)/2):
            d -=(MAX_TS+1)
        if (d < -(MAX_TS+1)/2):
            d +=(MAX_TS+1)
        return d

    def process_block(self, block):
        packets = [block[i: i+PACKET_SIZE] for i in range(0, BLOCK_SIZE*PACKET_SIZE, PACKET_SIZE)]
        ts_bytes = block[-4:]
        ts = struct.unpack(">I", ts_bytes)[0]&MAX_TS
        if(self.ts_init):
            self.ts_prev = ts
            self.ts = ts
            self.ts_init = 0
        self.ts += self.ts_diff(ts, self.ts_prev)
        self.ts_prev = ts
        return packets, self.ts

    def blocks(self):
        while True:
            data = self.f.read(BLOCK_SIZE_BYTES)
            if(len(data) != BLOCK_SIZE_BYTES):
                break
            yield self.process_block(data)
    
def ts_to_us(ts):
    return (ts * 1000000) // 75000000
