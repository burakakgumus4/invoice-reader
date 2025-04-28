@echo off
setlocal

set VENV_DIR=.venv

set PROJECT_DIR=%cd%

set ASSETS_LIB_DIR=%PROJECT_DIR%\assets\libs

set PYTHON_SITE_PACKAGES=%PROJECT_DIR%\.venv\Lib\site-packages\paddle\libs

echo [✔] Setting up your project environment...

IF NOT EXIST %VENV_DIR% (
    echo [•] Virtual environment not found. Creating a new one...
    python -m venv %VENV_DIR%
)

call %VENV_DIR%\Scripts\activate.bat

echo [•] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo [•] Copying required Paddle DLL files...
IF NOT EXIST %PYTHON_SITE_PACKAGES% (
    mkdir %PYTHON_SITE_PACKAGES%
)
xcopy /Y /S "%ASSETS_LIB_DIR%\*" "%PYTHON_SITE_PACKAGES%"

echo [✔] Setup complete. You can now run your project!
pause
