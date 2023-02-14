**Приложение («драйвер») для работы с промышленным 4-х канальным источником питания**
*Programmable DC Power Supply
GPP-1326/GPP-2323/GPP-3323/GPP-4323*
## Установка и запуск
1. Склонировать репозиторий с Github:
[`git@github.com:Sviatoslavvvik/GPP_API_driver.git`](README.md)
2. Перейти в директорию проекта
3. Создать виртуальное окружение:
`python -m venv venv`
4. Активировать окружение:
`source\venv\bin\activate`
или для Windows:
`source\venv\scripts\activate`
5. В директории создать .evn файл и заполнить необходимые данные:
`ADRESS=TCPIP0::169.254.129.17::1026::SOCKET - IP адрес прибора`
`PATH=C\Users\79232\ - путь до библиотеки NI-VISA на компьютере`
6. Установка зависимостей:
`pip install -r requirements.txt`
7. Запустить сервер:
`uvicorn main:app --reload`

:::no-loc text="После запуска сервера в случае успешной установки производится непрерывный опрос ТМИ прибора. Данные пишутся в main.log в корневой директории":::