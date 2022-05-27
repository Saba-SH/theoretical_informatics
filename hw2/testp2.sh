#! /bin/bash

# folder to look for code in
SOURCE_FOLDER="src"
# folder to look for input for program
INPUT_FOLDER="P2"
# folder to look for output to compare to
OUTPUT_FOLDER="P2"
# index of first and last test
TEST_FIRST=0
TEST_LAST=9

# command for executing program
PROG_COMMAND="python3 $SOURCE_FOLDER/simulate.py"

################################################################
for I in $(seq -f "%03g" $TEST_FIRST $TEST_LAST)
do
    INPUT_FILE="$INPUT_FOLDER/in$I.txt"
    OUTPUT_FILE="$OUTPUT_FOLDER/out$I.txt"
    
    PROG_OUTPUT=$(eval " cat $INPUT_FILE | $PROG_COMMAND")
    
    PROG_OUTPUT_STRING=""
    ACTUAL_OUTPUT_STRING=""
    for N in $PROG_OUTPUT
    do
        PROG_OUTPUT_STRING="$PROG_OUTPUT_STRING$N "
    done
    for N in $(cat $OUTPUT_FILE)
    do
        ACTUAL_OUTPUT_STRING="$ACTUAL_OUTPUT_STRING$N "
    done

    if [ "$PROG_OUTPUT_STRING" == "$ACTUAL_OUTPUT_STRING" ]
    then
        echo "TEST $I PASSED"
    else
        echo "#########TEST $I FAILED#######"
    fi

done
