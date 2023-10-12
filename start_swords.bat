

:: Эта команда отключает вывод выполненных команд в окне командной строки. 
:: Символ @ перед командой означает, что сама команда echo off не будет выведена 
:: на экран.
::@echo off

:: Эта команда создаёт копию текущих переменных окружения и 
:: устанавливает новые локальные переменные для этого батника. 
:: Изменения, сделанные в этом батнике, не будут влиять на 
:: глобальные переменные окружения.
setlocal

:: Чтение переменных окружения
@REM set TOKEN=%TOKEN%
@REM set TELEGRAM_GROUP_SWORDS_BOT='-XXX'
@REM set TELEGRAM_TOKEN_SWORDS='XXX:YYY' 
@REM python start_swords.py --token %TOKEN% --arg1 value1 --arg2 value2


:: Передача переменных окружения и аргументов командной строки в Python-скрипт
cd D:\linux\bots\bot_swords 
python start_swords.py 
:: Пауза для просмотра вывода
pause

endlocal
