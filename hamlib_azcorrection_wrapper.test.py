#!/usr/bin/env python

import unittest
import hamlib_azcorrection_wrapper as haw

class TestHamlibAzCorrectionTests(unittest.TestCase):

  def testNegativeToPositive_south(self):
    self.assertEqual(haw.negativeToPositive(-180), 180)
    self.assertEqual(haw.negativeToPositive(180), 180)

  
  def testNegativeToPositive_southwest(self):
    self.assertEqual(haw.negativeToPositive(-135), 225)

  def testNegativeToPositive_west(self):
    self.assertEqual(haw.negativeToPositive(-90), 270)

  def testNegativeToPositive_northwest(self):
    self.assertEqual(haw.negativeToPositive(-45), 315)
    
  def testNegativeToPositive_north(self):
    self.assertEqual(haw.negativeToPositive(0), 0)
    self.assertEqual(haw.negativeToPositive(360), 0)
    
  def testNegativeToPositive_northeast(self):
    self.assertEqual(haw.negativeToPositive(45), 45)

  def testNegativeToPositive_east(self):
    self.assertEqual(haw.negativeToPositive(90), 90)

  def testNegativeToPositive_southeast(self):
    self.assertEqual(haw.negativeToPositive(135), 135)


    
if __name__ == '__main__':
    unittest.main()