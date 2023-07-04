import json
import os.path

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
import asyncio


"""
1. Перейти в папку с проектом и создать виртуальное окружение: python3 -m venv 
2. Активировать виртуальное окружение: source venv/bin/activate
3. Установить зависимости: pip install -r requirements.txt
4. В файле CreateTgSession/venv/lib/python3.10(возможно другая версия)/site-packages/opentele/td/account.py 
   закомментировать строки: 213, 214, 215, 216
5. Исправить значения переменных ниже.
6. В активированном виртуальном окружении запустить скрипт: python main.py 
"""

""" Тип вашей системы """
system = 'Linux'  # 'Windows'

""" Имя пользователя системы """
sys_username = 'ms'


async def main():
    if system == 'Linux':
        tdataFolder = f"/home/{sys_username}/.local/share/TelegramDesktop/tdata"
    else:
        tdataFolder = fr"C:\Users\{sys_username}\AppData\Roaming\Telegram Desktop\tdata"

    tdesk = TDesktop(tdataFolder)
    assert tdesk.isLoaded()

    for account in tdesk._TDesktop__accounts:
        data_api = account._Account__api.__dict__

        client = await tdesk.ToTelethon(session="telethon.session", flag=UseCurrentSession)
        await client.connect()
        data_account = (await client.get_me()).__dict__
        data_account.pop('status')
        result_data = data_api | data_account
        with open(f'{result_data.get("phone")}.json', "w", encoding='utf-8') as file:
            json.dump(result_data, file, ensure_ascii=False, indent=4)
        client.disconnect()
        os.rename('telethon.session', f'{result_data.get("phone")}.session')
asyncio.run(main())
