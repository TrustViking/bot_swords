
:: This command disables the display of executed commands in the command-line window.
:: The @ symbol before the command means that the 'echo off' command itself will not be displayed.
:: @echo off

:: This command creates a copy of the current environment variables and
:: sets new local variables for this batch file.
:: Changes made in this batch file will not affect
:: global environment variables.
setlocal

:: Reading environment variables
@REM set TELEGRAM_TOKEN_SWORDS=1234567890:ABCDEFabcdef

:: Passing environment variables and command-line arguments to the Python script
cd D:\linux\bots\bot_swords
python start_swords.py

:: Pause to view the output
pause

endlocal
