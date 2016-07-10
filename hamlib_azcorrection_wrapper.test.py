#!/usr/bin/env python

import unittest
import hamlib_azcorrection_wrapper as haw

class TestHamlibAzCorrectionTests(unittest.TestCase):
  
  def testNegativeToPositive_southwest(self):
    #-135 degrees is the negative azimuth of southwest; the positive equivalent is 225 
    self.assertEqual(haw.negativeToPositive(-135),225)
    
    
if __name__ == '__main__':
    unittest.main()