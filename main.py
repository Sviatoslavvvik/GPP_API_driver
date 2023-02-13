import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from gpp import GppUnit
from models import ChanelNumber, SwitchedOn
from telemetry_logging import get_permanent_telemetry

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

ADRESS: str = 'TCPIP0::169.254.129.17::1026::SOCKET'  # IP прибора добавить из env
PATH: str = ''  # путь до NI-VISA на компьютере # добавить из env
DELAY: float = 0.3  # задержка между командами

logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event('startup')
async def app_startup():
    """Устанавливаем соединение с прибором
    Начинаем опрашивать ТМИ"""
    global gpp_unit
    gpp_unit = GppUnit(ADRESS, PATH)
    asyncio.create_task(get_permanent_telemetry(gpp_unit))


@app.post('/switched_on/')
async def switched_on(params: SwitchedOn):
    """Включение канала"""
    logger.info(f'Включение канала {params.ch}')
    try:
        gpp_unit.set_current(params.ch, params.current)        
        await asyncio.sleep(DELAY)
        logger.info(f'Установка значения тока {params.current}')
    except Exception as error:
        logger.error(error, exc_info=True)
        return JSONResponse(content={'message': 'Ошибка установки тока'},
                            status_code=503)
    try:
        gpp_unit.set_voltage(params.ch, params.voltage)
        await asyncio.sleep(DELAY)
    except Exception as error:
        logger.error(error, exc_info=True)
        return JSONResponse(content={'message': 'Ошибка утсановки напряжения'},
                            status_code=503)
    try:
        gpp_unit.switch_on(params.ch)
        await asyncio.sleep(DELAY)
    except Exception as error:
        logger.error(error, exc_info=True)
        return JSONResponse(content={'message': 'Ошибка включения'},
                            status_code=503)
    return JSONResponse(content={'message': 'Канал успешно включен',
                                 'params': params})


@app.post('/switched_off/')
async def switched_off(chanel: ChanelNumber):
    """Выключение канала"""
    logger.info(f'Выключение канала {chanel.ch}')
    try:
        gpp_unit.switch_off(chanel.ch)
        await asyncio.sleep(DELAY)
    except Exception as error:
        logger.error(error, exc_info=True)
        return JSONResponse(content={'message': 'Ошибка выключения'},
                            status_code=503)
    return {f'Канал {chanel.ch} выключен '}


@app.post('/get_channel_state/')
async def get_chennel_state(chanel: ChanelNumber):
    """Запрос статуса канала"""
    logger.info(f'Запрос статуса канала {chanel.ch}')
    try:
        response = gpp_unit.measure_all(chanel.ch)
        await asyncio.sleep(DELAY)
    except Exception as error:
        logger.error(error, exc_info=True)
        return JSONResponse(content={'message': 'Ошибка запроса параметров'},
                            status_code=503)
    return JSONResponse(content=response)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000) # удалить перед отправкой 