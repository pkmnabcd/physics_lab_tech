@echo off
setlocal enabledelayedexpansion

SET INPUT=%1
SET JAVA_PATH=java_code\homebrew origin\src
SET PYTHON_SCRIPT=python_code\data analysis\homebrew origin\main.py
echo Java class files should be found at: %JAVA_PATH%
echo Python script should be found at: %PYTHON_SCRIPT%
echo.

echo Running the cleaning algorithm
java -classpath "%JAVA_PATH%" Main "%INPUT%"

echo.
echo Graphing the original data
python "%PYTHON_SCRIPT%" "%INPUT%"

SET EDITED_INPUT=!INPUT:~0,-5!e.dat
echo.
echo Graphing the edited data
python "%PYTHON_SCRIPT%" "%EDITED_INPUT%"
