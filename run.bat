@echo off
REM Run script for CMD: crea entorno, instala dependencias y arranca la app
IF NOT EXIST .venv (
    python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

python main.py
pause