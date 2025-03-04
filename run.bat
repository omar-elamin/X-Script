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

echo Checking conda environment: %ENV_NAME%

:: Try to find conda
where conda >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    :: Conda is in PATH
    
    :: Check if environment exists
    conda env list | findstr /B /C:"%ENV_NAME% " >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Environment %ENV_NAME% does not exist. Creating it...
        call conda create -y -n %ENV_NAME% python=3.9
        if %ERRORLEVEL% NEQ 0 (
            echo Failed to create environment %ENV_NAME%
            exit /b 1
        )
    )
    
    :: Activate the environment
    call conda activate %ENV_NAME%
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to activate environment %ENV_NAME%
        exit /b 1
    )
    
    :: Install Python dependencies if requirements.txt exists
    if exist requirements.txt (
        echo Installing Python dependencies...
        pip install -r requirements.txt
        if %ERRORLEVEL% NEQ 0 (
            echo Failed to install Python dependencies
            exit /b 1
        )
    )
) else (
    :: Try common Conda installation paths
    set CONDA_FOUND=0
    
    if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
        set CONDA_PATH=%USERPROFILE%\miniconda3
        set CONDA_FOUND=1
    ) else if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
        set CONDA_PATH=%USERPROFILE%\anaconda3
        set CONDA_FOUND=1
    ) else if exist "%PROGRAMFILES%\miniconda3\Scripts\activate.bat" (
        set CONDA_PATH=%PROGRAMFILES%\miniconda3
        set CONDA_FOUND=1
    ) else if exist "%PROGRAMFILES%\anaconda3\Scripts\activate.bat" (
        set CONDA_PATH=%PROGRAMFILES%\anaconda3
        set CONDA_FOUND=1
    )
    
    if !CONDA_FOUND! EQU 1 (
        :: Check if environment exists
        call "!CONDA_PATH!\Scripts\conda.exe" env list | findstr /B /C:"%ENV_NAME% " >nul 2>&1
        if %ERRORLEVEL% NEQ 0 (
            echo Environment %ENV_NAME% does not exist. Creating it...
            call "!CONDA_PATH!\Scripts\conda.exe" create -y -n %ENV_NAME% python=3.9
            if %ERRORLEVEL% NEQ 0 (
                echo Failed to create environment %ENV_NAME%
                exit /b 1
            )
        )
        
        :: Activate the environment
        call "!CONDA_PATH!\Scripts\activate.bat" %ENV_NAME%
        
        :: Install Python dependencies if requirements.txt exists
        if exist requirements.txt (
            echo Installing Python dependencies...
            pip install -r requirements.txt
            if %ERRORLEVEL% NEQ 0 (
                echo Failed to install Python dependencies
                exit /b 1
            )
        )
    ) else (
        echo Could not find conda. Please make sure conda is installed and properly configured.
        exit /b 1
    )
)

:: Check for package.json and install npm dependencies if needed
if exist package.json (
    echo Checking npm dependencies...
    
    :: Check if node_modules directory exists
    if not exist node_modules (
        echo Installing npm dependencies...
        call npm install
        if %ERRORLEVEL% NEQ 0 (
            echo Failed to install npm dependencies
            exit /b 1
        )
    )
)

echo Starting the application...
npm start 