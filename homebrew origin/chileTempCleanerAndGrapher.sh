#!/bin/bash

source ./scriptPathsSetter.sh

INPUT=$1
echo "Java class files should be found at: $JAVA_PATH"
echo "Python script should be found at: $PYTHON_SCRIPT"
echo "The following was inputted: $INPUT"
echo

echo "Running the cleaning algorithm"
java -cp "$JAVA_PATH" Main "$INPUT"
echo

echo "Graphing the original data"
python3 "$PYTHON_SCRIPT" "$INPUT"
echo
echo

EDITED_INPUT="${INPUT%.dat}e.dat"
echo "Graphing the edited data"
echo "Edited input file: $EDITED_INPUT"
python3 "$PYTHON_SCRIPT" "$EDITED_INPUT"

echo
echo
