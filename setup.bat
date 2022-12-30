@echo off

set BAT_SCRIPT_DIR=%~dp0
set PY_CMD=
set ERRORLEVEL=

::This says to pipe the standard-output and error stream to null.
py -3.7 --version 2>nul  >nul
IF %ERRORLEVEL% == 0 (
    set PY_CMD=py -3.7
    goto execute
)

py -3.9 --version 2>nul  >nul
IF %ERRORLEVEL% == 0 (
    set PY_CMD=py -3.9
    goto execute
)

IF NOT DEFINED PY_CMD (
  echo Python not found! Need to install python 3.7 or 3.9
  goto error
)

:execute
cd %BAT_SCRIPT_DIR%
echo Using Python:
::Executes second command only if first command's errorlevel is NOT 0
%PY_CMD% --version || goto error

echo Create Virtual Environment
%PY_CMD% -m venv venv || goto error

echo Activate Virtual Environment
call %BAT_SCRIPT_DIR%\venv\Scripts\activate.bat || goto error

echo Updating PIP
%PY_CMD% -m pip install --upgrade pip || goto error
echo Installing Python Packages
%PY_CMD% -m pip install -r requirements.txt || goto error

echo Setup pre-commit hooks
%PY_CMD% -m pip install pre-commit || goto error
pre-commit.exe install || goto error
pre-commit.exe autoupdate || goto error
echo Setup finished!
pause 
goto :eof

:error
echo Error during setup.
pause
