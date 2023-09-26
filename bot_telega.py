#!/usr/bin/env python3 
#
import logging, asyncio, time, sys
from typing import Coroutine
from argparse import ArgumentParser
from sqlalchemy.engine.result import Row
#
from bot_env.create_obj4bot import dp, bot
from bot_env.mod_log import Logger
from handlers.client import  Handlers4bot

#
#
class Telega:
    """Modul for TELEGRAM"""
    countInstance=0
    #
    def __init__(self, 
                 folder_swords='swords',
                 pattern_name_swords='swords_',
                 log_file='telega_log.md',  
                 log_level=logging.DEBUG,
                 ):
        Telega.countInstance += 1
        self.countInstance = Telega.countInstance
        self.bot=bot
        self.dp=dp
        self.log_file=log_file
        self.log_level=log_level
        self.folder_swords = folder_swords
        self.pattern_name_swords = pattern_name_swords
        # Разбор аргументов
        self._arg_parser()
        # Logger
        self.Logger = Logger(log_file=self.log_file, 
                             log_level=self.log_level)
        # Client
        self.client = Handlers4bot(logger=self.Logger, 
                                   folder_swords = self.folder_swords,
                                   pattern_name_swords = self.pattern_name_swords,
                                   )
        self._print()
    #
    # выводим № объекта
    def _print(self):
        print(f'\n[Telega] countInstance: [{self.countInstance}]')
        self.Logger.log_info(f'\n[Telega] countInstance: [{self.countInstance}]\n')
        msg = (f"Started at {time.strftime('%X')}\n"
              f'platform: [{sys.platform}]\n'
              f'\nАргументы:\n'
              f'log_file: {self.log_file}\n'
              f'log_level: {self.log_level}\n'
              f'folder_swords: {self.folder_swords}\n'
              f'pattern_name_swords: {self.pattern_name_swords}\n'
              )
        print(msg)
        self.Logger.log_info(msg)
#
    # добавление аргументов строки
    def _arg_added(self, parser: ArgumentParser):
        # Добавление аргументов
        parser.add_argument('-fs', '--folder_swords', type=str, help='Папка для файлов стоп-слов')
        parser.add_argument('-ns', '--pattern_name_swords', type=str, help='Шаблон имени файла стоп-слов')
        parser.add_argument('-lf', '--log_file', type=str, help='Имя журнала логгирования')
        parser.add_argument('-ll', '--log_level', type=str, help='Уровень логгирования')

    # Разбор аргументов строки
    def _arg_parser(self):
        # Инициализация парсера аргументов
        parser = ArgumentParser()
        # добавление аргументов строки
        self._arg_added(parser)
        args = parser.parse_args()

        if args.log_file: self.log_file=args.log_file
        if args.log_level: self.log_level=int(args.log_level) # (CRITICAL, ERROR, WARNING,INFO, DEBUG)
        if args.folder_swords: self.folder_swords=args.folder_swords
        if args.pattern_name_swords: self.pattern_name_swords=args.pattern_name_swords
#
    # обертка для безопасного выполнения методов
    # async def safe_execute(self, coroutine: Callable[..., Coroutine[Any, Any, T]]) -> T:
    async def safe_await_execute(self, coroutine: Coroutine, name_func: str = None):
        if not coroutine:
            print(f'\n[Telega safe_await_execute] coroutine is {coroutine}')
            return None
        try:
            return await coroutine
        except Exception as eR:
            print(f'\nERROR[Telega {name_func}] ERROR: {eR}') 
            self.Logger.log_info(f'\nERROR[Telega {name_func}] ERROR: {eR}') 
            return None

    ### запускаем клиент бот-телеграм
    async def client_work(self):
        await self.safe_await_execute(self.client.register_handlers_client(), 'client_work')            

    # отправляем сообщение
    async def send_msg(self, row: Row, msg: str):
        chat_id = str(row.chat_id)
        username=str(row.username)
        message = await self.safe_await_execute(self.bot.send_message(chat_id=chat_id, text=msg), 'send_msg')       
        if not message:
                print(f'\n[Telega send_msg] не удалось отправить пользователю [{username}] сообщение')
                return None
        return message  

# MAIN **************************
async def main():
    print(f'\n**************************************************************************')
    print(f'\nБот вышел в онлайн')
    # создаем объект и в нем регистрируем хэндлеры Клиента
    telega=Telega()  
    telega.Logger.log_info(f'\n[main] Создали объект {telega}')
    print(f'\n[main] Создали объект {telega}')
    # регистрируем обработчики
    await telega.client_work()
    drop_pending_updates = await telega.bot.delete_webhook(drop_pending_updates=True)
    print(f'\n[telega main] сбросили ожидающие обновления: [{drop_pending_updates}]')
    # обработчики
    await telega.dp.start_polling(telega.bot)
    print(f'\n[telega main] закончили start_polling...')
    #
#
if __name__ == "__main__":
    asyncio.run(main())
    # executor.start_polling(dp, skip_updates=True, on_startup=main)


