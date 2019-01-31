@echo off
set BIN_PATH=%~dp0
set PYLIB_PATH=%BIN_PATH%..\pylib
set PYTHONPATH=%PYLIB_PATH%;%PYTHONPATH%

set FLOW_PATH=%BIN_PATH%flow.py
%BP_VENV%\scripts\python.exe %FLOW_PATH% %*
