@echo off
setlocal

set MAIN_SCRIPT=interfaz.py  REM Cambia esto al nombre de tu archivo principal
pyinstaller --onefile --windowed %MAIN_SCRIPT%

echo Ejecutable creado para %MAIN_SCRIPT% en la carpeta "dist".
pause
