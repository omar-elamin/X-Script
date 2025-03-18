@echo off
setlocal

echo ==========================================================
echo REMINDER: Make sure you've activated your conda environment
echo           by running 'conda activate xscript' first!
echo ==========================================================
echo.

echo Checking Node.js installation...
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Node.js not found. Please install Node.js.
    exit /b 1
)

echo Checking npm installation...
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo npm not found. Please install npm.
    exit /b 1
)

:: Check for package.json and install npm dependencies if needed
if exist package.json (
    echo Checking npm dependencies...
    if not exist node_modules (
        echo Installing npm dependencies...
        call npm install
        if %ERRORLEVEL% NEQ 0 (
            echo Failed to install npm dependencies
            exit /b 1
        )
    )
)

:: Start the app with specified port
echo Starting the application on port 8008...

:: Using the correct format for passing port to Next.js
call npm start -- -p 8008

exit /b 0