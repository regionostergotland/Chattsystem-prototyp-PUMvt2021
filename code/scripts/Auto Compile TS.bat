@echo off
for /f "delims=" %%F in ('where tsc.js') do set _path=%%F
IF not "%_path%"=="" (goto FOUND_FILE)
echo tsc.js was not found in PATH
:FOUND_FILE
node "%_path%"
:END
pause