import unittest
import tsdump
import io

class TetsTsdump(unittest.TestCase):
    data = (
        b"\x47\x00\x12\x14"
        b"\x47\x15\x37\x16"
        b"\x47\x15\x41\x12"
        b"\x47\x15\x2d\x1f"
        b"\x47\x00\xc9\x1f"
        b"\x47\x0f\xe8\x1c"
        b"\x47\x00\x65\x10"
        b"\x06\xde\x6b\xb8"
    )
    def test_tsdiff(self):
        d1 = tsdump.ts_diff(0, 0x7FFFFFF)
        self.assertEqual(d1, 1)
        d2 = tsdump.ts_diff(0x7FFFFFF, 0)
        self.assertEqual(d2, -1)
        d3 = tsdump.ts_diff(0, 5)
        self.assertEqual(d3, -5)
        d3 = tsdump.ts_diff(5, 0)
        self.assertEqual(d3, 5)
    
    def test_blocks(self):
        f = io.BytesIO(self.data)
        dump = tsdump.tsdump(f, True)
        it = dump.blocks()
        packets, ts = it.__next__()
        self.assertEqual(ts, 115239864)
        self.assertEqual(packets[0], b"\x47\x00\x12\x14")
        self.assertEqual(packets[1], b"\x47\x15\x37\x16")

if __name__ == '__main__':
    unittest.main()
