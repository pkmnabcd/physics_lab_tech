#!/bin/bash

INPUT=$1
JAVA_PATH="java_code/homebrew origin/src/"
PYTHON_SCRIPT="python_code/data analysis/homebrew origin/main.py"
echo "Java class files should be found at: $JAVA_PATH"
echo "Python script should be found at: $PYTHON_PATH"

java -cp $JAVA_PATH Main $INPUT
echo
python $PYTHON_SCRIPT $INPUT
