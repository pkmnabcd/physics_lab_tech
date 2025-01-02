@echo off

CALL scriptPathsSetter.bat

SET INPUT=%1
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
echo.
if "!INPUT:~-4!" == ".dat" (
  REM INPUT ends with .dat
  SET EDITED_INPUT=!INPUT:~0,-4!e.dat
) else (
  REM Assuming INPUT ends with .dat"
  SET EDITED_INPUT=!INPUT:~0,-5!e.dat"
)

setlocal disabledelayedexpansion
echo.
echo Graphing the edited data
echo Edited input file: %EDITED_INPUT%
python "%PYTHON_SCRIPT%" %EDITED_INPUT%
echo.
echo.
