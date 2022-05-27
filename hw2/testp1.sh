#! /bin/bash

# folder to look for input for program
INPUT_FOLDER="P1"
# folder to look for tests to run the converted machine on
TEST_FOLDER="P1"
# folder to look for desired answers of the run
ANSWER_FOLDER="P1"
# index of first and last test
TEST_FIRST=0
TEST_LAST=3

# command for executing conversion program
CONV_PROG_COMMAND="python3 src/convert.py"
# command for executing simulation program
SIM_PROG_COMMAND="python3 src/simulate.py"

################################################################
for I in $(seq -f "%03g" $TEST_FIRST $TEST_LAST)
do
    INPUT_FILE="$INPUT_FOLDER/in$I.txt"
    TEST_FILE="$TEST_FOLDER/t$I.txt"
    ANSWER_FILE="$ANSWER_FOLDER/a$I.txt"

    CONVERTED_MACHINE="$(eval cat $INPUT_FILE | $CONV_PROG_COMMAND)"

    INPUT_STRINGS=$(cat $INPUT_FILE)
    ANSWERS=$(cat $ANSWER_FILE)
    for J in 1..${#INPUT_STRINGS[@]}
    do
        SIMULATION_OUTPUT=$(eval "echo "$'$CONVERTED_MACHINE\n${INPUT_STRINGS[J]}'" | $SIM_PROG_COMMAND")
        TRIMMED_SIMULATION_OUTPUT=$(echo $SIMULATION_OUTPUT | xargs)
        if [ "${TRIMMED_SIMULATION_OUTPUT:-2:2}" == "-1" ]
        then
            if [ "${ANSWERS[J]}" == "T" ]
            then
                echo "#########TEST $I FAILED####### ON STRING $J"
                break
            fi
        else
            if [ "${ANSWERS[J]}" == "F" ]
            then
                echo "#########TEST $I FAILED####### ON STRING $J"
                break
            fi
        fi
    done
    echo "TEST $I COMPLETED"
    
done
