@echo off
setlocal

set VENV_DIR=.venv

set PROJECT_DIR=%cd%


echo Setting up your project environment...

IF NOT EXIST %VENV_DIR% (
    echo Virtual environment not found. Creating a new one...
    python -m venv %VENV_DIR%
)

call %VENV_DIR%\Scripts\activate.bat

echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements-gpu.txt
pip install -r requirements.txt


echo Setup complete. You can now run your project!
pause
