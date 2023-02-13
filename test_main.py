import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


class TestRouting(unittest.TestCase):
    @patch('gpp.GppUnit')
    def test_switched_on(self, gpp_mock):
        """Тест на вызов правильных методов при включении"""
        with TestClient(app) as client:
            with patch('main.app_startup'):
                client.post(
                    '/switched_on/',
                    json={'ch': 1, 'current': 0.1, 'voltage': 0.1})
                gpp_mock.set_current.assert_called_once()
                gpp_mock.set_voltage.assert_called_once()
                gpp_mock.switch_on.assert_called_once()

    @patch('gpp.GppUnit')
    def test_switched_off(self, gpp_mock):
        """Тест на вызов правильных методов при выключении"""
        with TestClient(app) as client:
            with patch('main.app_startup'):
                client.post(
                    '/switched_off/',
                    json={'ch': 1})
                gpp_mock.switch_off.assert_called_once()

    @patch('gpp.GppUnit')
    def test_chennel_state(self, gpp_mock):
        """Тест на вызов правильных методов при запросе статуса"""
        with TestClient(app) as client:
            with patch('main.app_startup'):
                client.post(
                    '/get_channel_state/',
                    json={'ch': 1})
                gpp_mock.measure_all.assert_called_once()


if __name__ == '__main__':
    unittest.main()
