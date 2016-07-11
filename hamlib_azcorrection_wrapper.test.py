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

    def testNegativeToPositive_floating(self):
        self.assertEqual(haw.negativeToPositive(-134.75), 225.25)



    def testPositiveToNegative_south(self):
        self.assertEqual(180, haw.positiveToNegative(-180))
        self.assertEqual(180, haw.positiveToNegative(180))

    def testPositiveToNegative_southwest(self):
        self.assertEqual(225, haw.positiveToNegative(-135))

    def testPositiveToNegative_west(self):
        self.assertEqual(270, haw.positiveToNegative(-90))

    def testPositiveToNegative_northwest(self):
        self.assertEqual(315, haw.positiveToNegative(-45))
        
    def testPositiveToNegative_north(self):
        self.assertEqual(0, haw.positiveToNegative(0))
        #self.assertEqual(0, haw.positiveToNegative(360))
        
    def testPositiveToNegative_northeast(self):
        self.assertEqual(45, haw.positiveToNegative(45))

    def testPositiveToNegative_east(self):
        self.assertEqual(90, haw.positiveToNegative(90))

    def testPositiveToNegative_southeast(self):
        self.assertEqual(135, haw.positiveToNegative(135))

    def testPositiveToNegative_floating(self):
        self.assertEqual(225.25, haw.negativeToPositive(-134.75))




    def testExtractAzEl_NoInput(self):
        self.assertRaises(ValueError, haw.extractAzEl)

    def testExtractAzEl_BadInput_SingleString(self):
        self.assertRaises(ValueError, haw.extractAzEl, "junk that won't actually parse")

    def testExtractAzEl_SingleLineString_Integer(self):
        self.assertEqual(haw.extractAzEl("P 100 200"), {'az':100.0, 'el':200.0})

    def testExtractAzEl_SingleLineString_Float(self):
        self.assertEqual(haw.extractAzEl("P 102.5 203.7"), {'az':102.5, 'el':203.7})

    def testExtractAzEl_MultiLineString_Integer(self):
        inputString = """P
                        100
                        200
                        """
            
        self.assertEqual(haw.extractAzEl(inputString), {'az':100.0, 'el':200.0})

    def testExtractAzEl_MultiLineString_Float(self):
        inputString = """P
                        102.5
                        203.7
                        """
        self.assertEqual(haw.extractAzEl(inputString), {'az':102.5, 'el':203.7})


    def testExtractAzEl_SingleLineString_Integer_NegativeAz(self):
        self.assertEqual(haw.extractAzEl("P -100 200"), {'az':-100.0, 'el':200.0})

    def testExtractAzEl_SingleLineString_Float_NegativeAz(self):
        self.assertEqual(haw.extractAzEl("P -102.5 203.7"), {'az':-102.5, 'el':203.7})

    def testExtractAzEl_MultiLineString_Integer_NegativeAz(self):
        inputString = """P
                        -100
                        200
                        """
                            
        self.assertEqual(haw.extractAzEl(inputString), {'az':-100.0, 'el':200.0})

    def testExtractAzEl_MultiLineString_Float_NegativeAz(self):
        inputString = """P
                        -102.5
                        203.7
                        """
        self.assertEqual(haw.extractAzEl(inputString), {'az':-102.5, 'el':203.7})


    





    def testExtractAzEl_MultiString_Float(self):
        inputString = ["P ",
                        "102.5",
                        "203.7"]
        self.assertEqual(haw.extractAzEl(inputString), {'az':102.5, 'el':203.7})

    def testExtractAzEl_MultiString_Integer_NegativeAz(self):
        inputString = ["P ",
                        "-100",
                        "200"]
                            
        self.assertEqual(haw.extractAzEl(inputString), {'az':-100.0, 'el':200.0})

    def testExtractAzEl_MultiString_Float_NegativeAz(self):
        inputString = ["P ",
                        "-102.5",
                        "203.7"]
        self.assertEqual(haw.extractAzEl(inputString), {'az':-102.5, 'el':203.7})




    
if __name__ == '__main__':
    unittest.main()