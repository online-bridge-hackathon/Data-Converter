import os
import unittest
from collections import namedtuple
import pbn


DIR = os.path.dirname(__file__)

class PBNTest(unittest.TestCase):
    def test_parse_pbn_string(self):
        """
        This tests various pbn methods and reads from
        storage
        """
        with open(os.path.join(DIR, 'test.pbn')) as f:
            pbn_string = f.read()

        boards = pbn.parse_pbn_string(pbn_string)

        self.assertEqual(len(boards), 2)
        self.assertEqual(boards[0]['board'], "1")
        self.assertEqual(boards[1]['event'], "Men's Pairs - SPRING NABC 1970")
        self.assertEqual(
            boards[1]['deal']['S'],
            ['SK', 'SQ', 'ST', 'S7', 'S4', 'HK', 'HJ', 'H7', 'H5', 'DA', 'DQ', 'D2', 'C7']
        )
        self.assertEqual(
            boards[0]['deal']['W'],
            ['SA', 'ST', 'S2', 'H7', 'H5', 'H2', 'DA', 'D6', 'D3', 'D2', 'CQ', 'CT', 'C2']
        )
        self.assertEqual(boards[1]['declarer'], "S")
        self.assertEqual(boards[1]['contract'], {'level': 4, 'denomination': 'H', 'risk': None})
        self.assertEqual(
            boards[0]['auction'],
            [('1NT', ''), ('Pass', ''), ('3NT', ''), ('Pass', ''), ('Pass', ''), ('Pass', '')]
        )
        self.assertEqual(boards[0]['play'], [])
        self.assertEqual(len(boards[1]['play']), 13)
