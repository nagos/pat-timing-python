import unittest
import pat_timing

class TestPatTiming(unittest.TestCase):
    data = b"\x47\x00\x12\x14\x47\x15\x37\x16"
    def test_parse_packet(self):
        pid, cc = pat_timing.parse_packet(self.data)
        self.assertEqual(pid, 18)
        self.assertEqual(cc, 4)

if __name__ == '__main__':
    unittest.main()
