@echo off
title JSF & MAFIGO SPORT SYSTEMS - Servidor Central
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 goto runpy
where python >nul 2>nul
if %errorlevel%==0 goto runpython
echo.
echo NO SE ENCONTRO PYTHON.
echo Instala Python 3 de 64 bits y marca "Add python.exe to PATH".
pause
exit /b
:runpy
py servidor_central.py
goto fin
:runpython
python servidor_central.py
:fin
pause
