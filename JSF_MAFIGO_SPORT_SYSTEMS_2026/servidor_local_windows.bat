@echo off
title JSF & MAFIGO SPORT SYSTEMS - Servidor Local
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (py -m http.server 8080 --bind 0.0.0.0 & goto fin)
where python >nul 2>nul
if %errorlevel%==0 (python -m http.server 8080 --bind 0.0.0.0 & goto fin)
echo No se encontro Python.
echo Instala Python 3 de 64 bits con "Add python.exe to PATH" activado.
pause
:fin
