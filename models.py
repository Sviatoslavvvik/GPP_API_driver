from typing import Dict

from pydantic import BaseModel, Field, root_validator


class ChanelNumber(BaseModel):
    """Модель номера канала"""
    ch: int = Field(
        title='Номер канала',
        ge=1,
        le=4
    )


class SwitchedOn(BaseModel):
    """Параметры для включения"""
    ch: int = Field(
        title='Номер канала',
        ge=1,
        le=4
    )
    current: float = Field(
        title='Значение тока',
        ge=0.000,
        le=3.000
    )
    voltage: float = Field(
        title='Значение напряжения',
        ge=0.000,
        le=32.000
    )

    @root_validator()
    def switch_on_validation(cls, values):
        """Валидация значение тока"""
        current_limits: Dict[str, float] = {
            1: 3.000,
            2: 3.000,
            3: 1.000,
            4: 1.000}
        voltage_limits: Dict[str, float] = {
            1: 32.000,
            2: 32.000,
            3: 5.000,
            4: 15.000}
        current, volt = values.get('current'), values.get('voltage')
        ch = values.get('ch')
        if current <= current_limits.get(ch) and current >= 0:
            values['current'] = round(current, 3)
        else:
            raise ValueError('Значение тока вне допустимых пределов')
        if volt <= voltage_limits.get(ch) and volt >= 0:
            values['voltage'] = round(volt, 3)
        else:
            raise ValueError('Значение Напряжения вне допустимых пределов')
        return values
