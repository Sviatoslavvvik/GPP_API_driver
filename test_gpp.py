import inspect
import unittest
from unittest.mock import Mock, patch

from pyvisa import ResourceManager

import gpp
from gpp import GppUnit
from main import ADRESS, PATH


class TestGPPMethods(unittest.TestCase):
   
    @patch('gpp.GppUnit', autospec=True)
    def test_measure_all(self, MockGpp):
        test_unit = MockGpp(ADRESS, PATH)
        request = test_unit.measure_all(1)
        request.assert_called_with(':MEASure1:ALL?')

if __name__ == '__main__':
    unittest.main()