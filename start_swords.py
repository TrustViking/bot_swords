#!/usr/bin/env python3
#
import os, sys, psutil, pynvml, logging, asyncio, time
from typing import Coroutine
from bot_env.mod_log import Logger
from argparse import ArgumentParser

class Start:
    """Module for START"""
    countInstance=0
    #
    def __init__(self, 
                 folder_swords='swords',
                 pattern_name_swords='swords_',
                 log_file='log.md', 
                 log_level=logging.DEBUG,
                 ):
        Start.countInstance += 1
        self.countInstance = Start.countInstance
        #
        self.log_file=log_file
        self.log_level=log_level
        self.folder_swords = folder_swords
        self.pattern_name_swords = pattern_name_swords
        # Разбор аргументов командной строки
        self._arg_parser()
        # Logger
        self.Logger = Logger(self.log_file, self.log_level)
        self._print()

        #     
    # выводим № объекта
    def _print(self):
        print(f'\n[Start] countInstance: [{self.countInstance}]')
        self.Logger.log_info(f'\n[Start] countInstance: [{self.countInstance}]\n')
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
    # добавление аргументов командной строки
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
        # (CRITICAL, ERROR, WARNING,INFO, DEBUG)
        if args.log_level: self.log_level=logging.getLevelName(args.log_level.upper())
        if args.folder_swords: self.folder_swords=args.folder_swords
        if args.pattern_name_swords: self.pattern_name_swords=args.pattern_name_swords

    # Функция для логирования информации о памяти
    def log_memory(self):
        self.Logger.log_info(f'****************************************************************')
        self.Logger.log_info(f'*Data RAM {os.path.basename(sys.argv[0])}: [{psutil.virtual_memory()[2]}%]')
        # Инициализируем NVML для сбора информации о GPU
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        self.Logger.log_info(f'\ndeviceCount [{deviceCount}]')
        for i in range(deviceCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            self.Logger.log_info(f"#GPU [{i}]: used memory [{int(meminfo.used / meminfo.total * 100)}%]")
            self.Logger.log_info(f'****************************************************************\n')
        # Освобождаем ресурсы NVML
        pynvml.nvmlShutdown()

    # обертка для безопасного выполнения методов
    # async def safe_execute(self, coroutine: Callable[..., Coroutine[Any, Any, T]]) -> T:
    async def safe_await_execute(self, coroutine: Coroutine, name_func: str = None):
        if not coroutine:
            print(f'\n[Start safe_await_execute] coroutine is {coroutine}')
            return None
        try:
            return await coroutine
        except Exception as eR:
            print(f'\nERROR[Start {name_func}] ERROR: {eR}') 
            self.Logger.log_info(f'\nERROR[Start {name_func}] ERROR: {eR}') 
            return None

    # Асинхронная функция для запуска скрипта
    async def making_subprocess_script(self, script):
        self.Logger.log_info(f'[Start making_subprocess_script] start script: {script}')
        print(f'\n[Start making_subprocess_script] start script: {script}')
        # Example:
        # await asyncio.create_subprocess_shell("ls -l > output.txt")
        # await asyncio.create_subprocess_exec("ls", "-l")
        try:
            # Используем asyncio для асинхронного запуска скрипта
            process = await self.safe_await_execute(asyncio.create_subprocess_shell(script), 'run_script')
            if not process:
                print(f'\n[Start making_subprocess_script] нет процесса!!! process: {process}')
                return None 
        except Exception as eR:
            print(f'\nERROR[Start making_subprocess_script] ERROR: {eR}') 
            self.Logger.log_info(f'\nERROR[Start making_subprocess_script] ERROR: {eR}') 
            return None
        await process.wait()


# MAIN **************************
# Главная асинхронная функция
async def main():
    print(f'\nСтарт приложения...\n') 
    # print(f'\n==============================================================================\n')
    file_start = os.path.basename(sys.argv[0])
    path_start = sys.path[0]
    print(f'File: [{file_start}]')
    print(f'Path: [{path_start}]') 
    # print(f'Data memory: [{psutil.virtual_memory()}]')
    # Вывод значений с названиями
    print(f'Data memory:')
    memory = psutil.virtual_memory()
    for field in memory._fields:
        print(f"{field}: {getattr(memory, field)}")    
    
    # Создаем экземпляр класса Start
    start = Start()
    start.log_memory()
    #
    # Список скриптов для запуска
    args_bot_telega=' '
    
    if start.folder_swords: 
        args_bot_telega+=f'--folder_swords {start.folder_swords} '

    if start.pattern_name_swords: 
        args_bot_telega+=f'--pattern_name_swords {start.pattern_name_swords} '
    
    if start.log_file:
        log_file_arg=f'--log_file {start.log_file} '
        args_bot_telega+=log_file_arg

    if start.log_level:
        log_level_arg=f'--log_level {start.log_level} '
        args_bot_telega+=log_level_arg

    full_path_telega = os.path.join(sys.path[0], 'bot_telega.py')
    if not os.path.isfile(full_path_telega):
        print(f'\nERROR [Start main] Нет файла: {full_path_telega}')
        return None
    
    script_telega_args = 'python ' + full_path_telega + args_bot_telega
    print(f'\n[Start main] script_telega: {script_telega_args}')
    
    scripts = [
        script_telega_args,
                ]
    print(f'\n[Start main] scripts: {scripts}')
    #
    # Запускаем скрипты асинхронно
    
    tasks = [start.making_subprocess_script(script) for script in scripts]
    await start.safe_await_execute(asyncio.gather(*tasks), 'gather')

# Запускаем главную асинхронную функцию
if __name__ == "__main__":
    asyncio.run(main())



