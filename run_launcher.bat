@echo off
setlocal

REM Get directory of the script
set "SCRIPT_DIR=%~dp0"
cd "%SCRIPT_DIR%"

REM Activate virtual environment if it exists
if exist venv (
    call venv\Scripts\activate.bat
) else (
    REM Create virtual environment if it doesn't exist
    python -m venv venv
    call venv\Scripts\activate.bat
    
    REM Install requirements
    if exist requirements.txt (
        pip install -r requirements.txt
    )
    
    REM Install launcher requirements if they exist separately
    if exist launcher_requirements.txt (
        pip install -r launcher_requirements.txt
    )
)

REM Run the launcher
python launcher.py

endlocal 