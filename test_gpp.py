import unittest
from unittest.mock import Mock, patch

from gpp import GppUnit
from main import ADRESS, PATH


class TestGPPMethods(unittest.TestCase):
    def test_measure_all_right(self):
        """Проверка отправки корректного запроса"""
        with patch('gpp.GppUnit'):
            gpp_unit = GppUnit(ADRESS, PATH)
            gpp_unit.unit = Mock()
            gpp_unit.measure_all(2)
            gpp_unit.unit.query.assert_called_with(':MEASure2:ALL?')

    def test_measure_all_bad(self):
        """Проверка отправки некорректного запроса"""
        with patch('gpp.GppUnit'):
            gpp_unit = GppUnit(ADRESS, PATH)
            gpp_unit.unit = Mock()
            with self.assertRaises(ValueError):
                gpp_unit.measure_all(5)

    def test_set_current_right(self):
        """Проверка  корректной установки тока"""
        with patch('gpp.GppUnit'):
            gpp_unit = GppUnit(ADRESS, PATH)
            gpp_unit.unit = Mock()
            gpp_unit.set_current(1, 1.500)
            gpp_unit.unit.write.assert_called_with(':SOURce1:CURRent 1.5')

    def test_set_current_bad(self):
        """Проверка некорректной установки тока"""
        with patch('gpp.GppUnit'):
            gpp_unit = GppUnit(ADRESS, PATH)
            gpp_unit.unit = Mock()
            with self.assertRaises(ValueError):
                gpp_unit.set_current(1, 5)

    def test_set_voltage_right(self):
        """Проверка  корректной установки ныпряжения"""
        with patch('gpp.GppUnit'):
            gpp_unit = GppUnit(ADRESS, PATH)
            gpp_unit.unit = Mock()
            gpp_unit.set_voltage(2, 31.500)
            gpp_unit.unit.write.assert_called_with(':SOURce2:VOLTage 31.5')

    def test_set_voltage_bad(self):
        """Проверка некорректной установки тока"""
        with patch('gpp.GppUnit'):
            gpp_unit = GppUnit(ADRESS, PATH)
            gpp_unit.unit = Mock()
            with self.assertRaises(ValueError):
                gpp_unit.set_voltage(5, 45)

    def test_switch_on_right(self):
        """Проверка  корректного включения"""
        with patch('gpp.GppUnit'):
            gpp_unit = GppUnit(ADRESS, PATH)
            gpp_unit.unit = Mock()
            gpp_unit.switch_on(2)
            gpp_unit.unit.write.assert_called_with(':OUTPut2:STATe ON')

    # некорректное включение канала считаем проверенным ранее, т.к
    # проверка ведётся одним методом
    def test_switch_off_right(self):
        """Проверка  корректного включения"""
        with patch('gpp.GppUnit'):
            gpp_unit = GppUnit(ADRESS, PATH)
            gpp_unit.unit = Mock()
            gpp_unit.switch_off(2)
            gpp_unit.unit.write.assert_called_with(':OUTPut2:STATe OFF')
