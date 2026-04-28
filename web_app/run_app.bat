@echo off
title PaxeraHealth AI Segmentation App

cd /d "%~dp0backend"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting PaxeraHealth AI App on http://127.0.0.1:8000
echo.

timeout /t 2 /nobreak
start http://127.0.0.1:8000

python app.py

pause
