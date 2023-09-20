
import os, sys
from io import BytesIO
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from aiogram import types
from aiogram.types.message import ContentType
from aiogram.types import InputFile
from aiogram.dispatcher.filters import Command
from bot_env.mod_log import Logger
from bot_env.create_obj4bot import bot, dp, token

class Handlers4bot:
    """
    Создаем для telegram-bot хэндлеры клиента:

    Аргументы:
    - logger: Logger
    """
    countInstance=0
    #
    def __init__(self, 
                 logger: Logger,
                 folder_swords,
                 pattern_name_swords,
                    ): 

        Handlers4bot.countInstance+=1
        self.countInstance=Handlers4bot.countInstance
        self.countHandlers=0
        self.folder_swords=folder_swords
        self.pattern_name_swords=pattern_name_swords
        self.bot=bot
        self.dp=dp
        self.token=token
        # ℃ ∈ ☪
        self.replace_dict={'a': '@', 'e':'€', 'i':'!', 'o':'0', 's':'$', 'u':'*',
                           'а': '@', 'е':'€', 'и':'N', 'й':'N', 'о':'0', 'р':'₽', 'с':'©', 'я':'Ⓡ', 'т':'✝'}
        self.path_swords = os.path.join(sys.path[0], folder_swords, pattern_name_swords)
        self.Logger = logger
        self._new_client()
        #
        #
    # New Client
    def _new_client(self):
        print(f'[_new_client] Client# {self.countInstance}')
        self.Logger.log_info(f'[_new_client] Client# {self.countInstance}')

    # New handlers
    def _new_handlers(self, name_handler=None):
        self.countHandlers+=1
        print(f'\n\n[_new_handlers] Handler {name_handler} # {self.countHandlers}')
        self.Logger.log_info(f'[_new_handlers] Handler# {self.countHandlers}')

    # асинхронная обертка для безопасного выполнения методов
    async def safe_await_execute(self, coroutine, name_func: str = None):
        try:
            return await coroutine
        except Exception as eR:
            print(f'\nERROR[Handlers4bot {name_func}] ERROR: {eR}') 
            self.Logger.log_info(f'\nERROR[Handlers4bot {name_func}] ERROR: {eR}') 
            return None

    # синхронная обертка для безопасного выполнения методов
    def safe_execute(self, func, name_func: str = None):
        try:
            return func
        except Exception as eR:
            print(f'\nERROR[VidCompar {name_func}] ERROR: {eR}') 
            self.Logger.log_info(f'\nERROR[VidCompar {name_func}] ERROR: {eR}') 
            return None

    def filtering_swords(self, file_path: str):
        """
        Загружает файл стоп-слов, убирает повторы и сортирует его
        с последующей записью на диск

        :param file_path: полный путь к файлу
        :return: полный путь к перезаписанному файлу
        """
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            print(f'\nERROR [filtering_swords] Проверьте полный путь к файлу стоп-слов: {file_path}')
            return None
        
        try:
            # Чтение файла в память
            with open(file_path, 'r') as f:
                stop_words = f.read().splitlines()

            # Добавление вариантов слов с большой и маленькой буквы
            case_sensitive_words = set()
            for word in set(filter(lambda x: x.strip(), stop_words)):
                case_sensitive_words.add(word.lower())
                case_sensitive_words.add(word.capitalize())            

            # Сортировка
            swords = sorted(case_sensitive_words)

            # запись файла в память
            with open(file_path, 'w') as f:
                for word in swords:
                    f.write(f"{word}\n")
        except Exception as eR:
            print(f'\nERROR[Handlers4bot filtering_swords] ERROR: {eR}') 
            self.Logger.log_info(f'\nERROR[Handlers4bot filtering_swords] ERROR: {eR}') 
            return None
        return file_path

    # определяем язык текста
    # возвращаем строку 'en', 'ru' or None
    def detection_lang(self, buf: BytesIO):
        text = [line.decode('utf-8') for line in buf.readlines()]
        try:
            return detect(' '.join(text))
        except LangDetectException as eR:
            print(f'\nERROR[Handlers4bot detection_lang] LangDetectException: {eR}')
            self.Logger.log_info (f'\nERROR[Handlers4bot detection_lang] LangDetectException: {eR}')
            return None
        except UnicodeDecodeError as eU:
            error_message = f'\nERROR[Handlers4bot detection_lang] UnicodeDecodeError: {eU}'
            print(error_message)  # или self.Logger.log_info(error_message)
            return None

    def diction_swords(self, file_path: str, replace_dict: dict):
        """
        Загружает слова из файла и создает словарь стоп-слов и их замен.

        :param file_path: полный путь к файлу
        :param replace_dict: словарь для замены символов
        :return: словарь, где ключ - исходное слово, значение - измененное слово
        """
        
        word_dict = {}

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            print(f'\nERROR [load_words_from_file] Проверьте полный путь к файлу стоп-слов')
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Убираем пробелы и переносы строк с обоих концов строки
                word = line.strip()
                
                # Производим замену символов
                replaced_word = "".join([replace_dict.get(char, char) for char in word])
                
                # Сохраняем в словаре
                word_dict[word] = replaced_word
                
        return word_dict

    # обрабатывает команду пользователя - /start
    async def command_start(self, message: types.Message): 
        # await Form.first_video.set()
        msg = (f'Пришлите сюда файл с титрами на:\n'
               f'\n- английском языке или русском языке. \n'
               f'\nДругие языки пока не поддерживаются \n')
        await self.bot.send_message(message.from_user.id, msg)  
    
    # обработчик любого сообщения, кроме  - /start
    async def any2start(self, message: types.Message):
        await self.bot.send_message(message.from_user.id, text=f'Прислали: {message.content_type}\n')
        msg = (f'Наберите команду [/start] для начала')
        await self.bot.send_message(message.from_user.id, msg)

    # замена слов из словаря
    def replace_swords (self, buf: BytesIO, diction: dict):
        # Создаем новый буфер для записи обработанного текста
        new_buf = BytesIO()
        new_buf.seek(0)
        buf.seek(0)
        # Обрабатываем исходный буфер построчно
        for line in buf.readlines():
            # Декодируем строку из байтов в строку Unicode
            decoded_line = line.decode('utf-8')
            
            # Разбиваем строку на слова и обрабатываем каждое слово
            words = decoded_line.split()
            new_words = [diction.get(word, word) for word in words]
            
            # Собираем строку обратно и кодируем ее в байты
            new_line = ' '.join(new_words).encode('utf-8')

            # Записываем обработанную строку в новый буфер
            new_buf.write(new_line + b'\n')
        return new_buf

    # отправляем буфер-документ
    async def send_srt_file(self, chat_id: str, buffer: BytesIO):
        # Переход к началу буфера
        buffer.seek(0)
        message_file = await self.safe_await_execute(
                        self.bot.send_document(chat_id, InputFile(buffer, filename='title.srt'), caption='Файл титров без стоп-слов'),'send_srt_file')
        return message_file

    # отправляем сообщение
    async def send_msg(self, chat_id: str, msg: str):
        message = await self.safe_await_execute(
                        self.bot.send_message(chat_id=chat_id, 
                                              text=msg), 'send_msg')
        return message       

    ## обработчик файла титров
    async def process_title(self, message: types.Message):
        self._new_handlers('process_title')
        #
        doc = message.document if message else None
        if not doc:
            msg = (f'\n[Handlers4bot process_title] Документ не получил. \n'
                   f'Отправьте документ еще раз.')
            print(msg)
            await self.bot.send_message(message.from_user.id, msg)            
            return None
        file_doc = await self.bot.get_file(doc.file_id)
        #
        doc_file_id=str(message.document.file_id)
        doc_file_size=str(message.document.file_size)
        number = int(doc_file_size)
        file_size_format = f"{number:,}".replace(",", " ")
        mime = str(message.document.mime_type).split('/')[1]
        print(f'\n[Handlers4bot process_title] \nfile_id: {doc_file_id} \nmime: {mime}')
        #
        msg = (f'Файл с титрами:\n'
               f'file_size: {file_size_format} bytes\n'
               f'mime_type: {mime}\n'
               f'Начинаю обрабатывать файл...'
               )
        await self.bot.send_message(message.from_user.id, msg)
        
        # Загрузить документ в буфер
        buf = await self.safe_await_execute(file_doc.download(destination_file=BytesIO(), timeout=120), 'process_title file_doc.download')   
        if not buf:
            print(f"\n[Handlers4bot process_title] document don't saved in buf. BUF: {buf}")
            self.Logger.log_info(f"\n[Handlers4bot process_title] document don't saved in buf. BUF: {buf}")
            return None 
        # 
        # начало буфера
        buf.seek(0)
        language = self.detection_lang(buf)
        print(f'language: {language}')
        if not language:
            msg = f'\n[Handlers4bot process_title] Не определили язык титров language: {language}'
            print(msg)
            await self.send_msg(message.from_user.id, msg)
            return None
        
        # создаем словарь стоп_слов и их замены
        swords = self.safe_execute(self.diction_swords(self.filtering_swords(self.path_swords+language.upper()+'.txt'), self.replace_dict), 'process_title load_words_from_file')
        print(f'swords: {swords}')
        if not swords:
            msg = (f'\n[Handlers4bot process_title] Не создали словарь стоп-слов {swords} \n'
                  f'на языке {language}') 
            print(msg)
            await self.send_msg(message.from_user.id, msg)
            return None
        
        # новый файл титров
        new_buf = self.safe_execute(self.replace_swords(buf, swords), 'process_title replace_swords')
        size_in_bytes = new_buf.getbuffer().nbytes
        print(f'new_buf size_in_bytes: {size_in_bytes}')
        if not new_buf:
            msg = (f'\n[Handlers4bot process_title] Не создали новый файл титров {new_buf} \n'
                  f'на языке {language}')
            print(msg)
            await self.send_msg(message.from_user.id, msg)
            return None
        
        # отправляем буфер-документ
        msg = await self.safe_await_execute(self.send_srt_file(message.from_user.id, new_buf), 'process_title send_srt_file')
        if msg: 
            print(f'\n[Handlers4bot process_title] Новый файл с титрами отправлен')
        else: 
            msg = f'\n[Handlers4bot process_title] Новый файл с титрами не отправлен'
            print(msg)
            await self.send_msg(message.from_user.id, msg)
            return None

    ### регистрация хэндлеров
    async def register_handlers_client(self):
        # обрабатываем нажатие кнопки СТАРТ 
        self.dp.register_message_handler(self.command_start, Command('start'))

        # обрабатываем первое видео 
        self.dp.register_message_handler(self.process_title, content_types=ContentType.DOCUMENT)
        
        # любые сообщения и на старт
        self.dp.register_message_handler(self.any2start, content_types=ContentType.ANY, state='*')




