@echo off

SET INPUT=%1
SET JAVA_PATH=java_src
SET PYTHON_SCRIPT=python_src\main.py
echo Java class files should be found at: %JAVA_PATH%
echo Python script should be found at: %PYTHON_SCRIPT%
echo The following was inputted: %INPUT%
echo.

echo Running the cleaning algorithm
java -classpath "%JAVA_PATH%" Main %INPUT%

echo.
echo Graphing the original data
python "%PYTHON_SCRIPT%" %INPUT%

setlocal enabledelayedexpansion
SET EDITED_INPUT=!INPUT:~0,-5!e.dat
setlocal disabledelayedexpansion
echo.
echo Graphing the edited data
python "%PYTHON_SCRIPT%" %EDITED_INPUT%
