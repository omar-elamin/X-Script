@echo off
setlocal enabledelayedexpansion

:: Default environment name
set DEFAULT_ENV=xscript

:: Use the provided environment name or the default
if "%~1"=="" (
    set ENV_NAME=%DEFAULT_ENV%
) else (
    set ENV_NAME=%~1
)

echo Activating conda environment: %ENV_NAME%

:: Try to find conda
where conda >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    :: Conda is in PATH
    call conda activate %ENV_NAME%
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to activate environment %ENV_NAME%
        exit /b 1
    )
) else (
    :: Try common Conda installation paths
    if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
        call "%USERPROFILE%\miniconda3\Scripts\activate.bat" %ENV_NAME%
    ) else if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
        call "%USERPROFILE%\anaconda3\Scripts\activate.bat" %ENV_NAME%
    ) else if exist "%PROGRAMFILES%\miniconda3\Scripts\activate.bat" (
        call "%PROGRAMFILES%\miniconda3\Scripts\activate.bat" %ENV_NAME%
    ) else if exist "%PROGRAMFILES%\anaconda3\Scripts\activate.bat" (
        call "%PROGRAMFILES%\anaconda3\Scripts\activate.bat" %ENV_NAME%
    ) else (
        echo Could not find conda. Please make sure conda is installed and properly configured.
        exit /b 1
    )
)

echo Starting the application...
npm start 