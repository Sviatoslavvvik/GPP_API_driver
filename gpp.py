import logging
from logging.handlers import RotatingFileHandler
from typing import Dict

from pyvisa import ResourceManager
from pyvisa.errors import VisaIOError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('main.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s, %(name)s')
handler.setFormatter(formatter)


class GppUnit:
    """Класс для реализации подключения к устройству"""
    def __init__(self, address: str,
                 path_to_NI: str) -> None:
        self.path_to_NI = path_to_NI
        resource_manager: ResourceManager = ResourceManager(path_to_NI)
        self.address = address
        try:
            self.unit = resource_manager.open_resource(self.address)
        except VisaIOError:
            logger.critical('Ошибка подключения к прибору')
        else:
            logger.info('Соеденинение установлено')

    def _check_chanel_number(self, ch: int) -> None:
        """Проверяем номер канала"""
        if ch not in range(1, 5):
            logging.error('Задан некорректный номер канала')
            raise ValueError(f'Номер канала на выключение не в 1 <= {ch} < 4')

    def _check_quantiti_value(
            self,
            limits: Dict[int, float],
            val: float,
            ch: int) -> None:
        """Проверяем лимиты"""
        if val > limits.get(ch):
            logging.error('Установлено значение с превышением')
            raise ValueError(f'Превышение лимита по каналу {ch}',
                             f'Задаваемое значение {val},'
                             f' максимальное {limits.get(ch)}')
        if val < 0:
            logging.error('Значение не может быть меньше нуля')
            raise ValueError(f'Значение  по каналу {ch}',
                             f'{val} < 0,')

    def measure_all(self, ch: int) -> str:
        """Запрос всех параметров канала ch"""
        self._check_chanel_number(ch)
        return self.unit.query(f':MEASure{ch}:ALL?')

    def set_current(self, ch: int, curr: int) -> None:
        """Задать ток канала ch"""
        current_limits: Dict[str, float] = {
            1: 3.000,
            2: 3.000,
            3: 1.000,
            4: 1.000}
        self._check_chanel_number(ch)
        self._check_quantiti_value(current_limits, curr, ch)
        self.unit.write(f':SOURce{ch}:CURRent {curr}')

    def set_voltage(self, ch: int, volt: float) -> None:
        """Задать напряжение канала ch"""
        voltage_limits: Dict[str, float] = {
            1: 32.000,
            2: 32.000,
            3: 5.000,
            4: 15.000}
        self._check_chanel_number(ch)
        self._check_quantiti_value(voltage_limits, volt, ch)
        self.unit.write(f':SOURce{ch}:VOLTage {volt}')

    def switch_on(self, ch: int) -> None:
        """Включить выход ch канала питания"""
        self._check_chanel_number(ch)
        self.unit.write(f':OUTPut{ch}:STATe ON')

    def switch_off(self, ch: int) -> None:
        """Выключить выход ch канала питания"""
        self._check_chanel_number(ch)
        self.unit.write(f':OUTPut{ch}:STATe OFF')
