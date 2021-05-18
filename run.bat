@echo off
title run
python --version 2>NUL
if errorlevel 1 goto errorNoPython
pip install --user -U nltk
pip install --user scipy
pip install -r requirements.txt
python code/server.py
pause
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed
