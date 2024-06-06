#!/bin/bash

INPUT=$1
JAVA_PATH="java_code/homebrew origin/src/"
PYTHON_SCRIPT="python_code/data analysis/homebrew origin/main.py"
echo "Java class files should be found at: $JAVA_PATH"
echo "Python script should be found at: $PYTHON_SCRIPT"

echo
echo "Running the cleaning algorithm"
java -cp "$JAVA_PATH" Main "$INPUT"
echo
echo "Graphing the original data"
python "$PYTHON_SCRIPT" "$INPUT"
EDITED_INPUT="${INPUT%.dat}e.dat"
echo
echo "Graphing the edited data"
python "$PYTHON_SCRIPT" "$EDITED_INPUT"
