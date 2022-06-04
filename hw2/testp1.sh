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
    printf "\n~~~~~~~~~~~TEST $I STARTED~~~~~~~~~~~~\n\n"

    INPUT_FILE="$INPUT_FOLDER/in$I.txt"
    TEST_FILE="$TEST_FOLDER/t$I.txt"
    ANSWER_FILE="$ANSWER_FOLDER/a$I.txt"

    CONVERTED_MACHINE="$(eval cat $INPUT_FILE | $CONV_PROG_COMMAND)"
    
    TEST_STRINGS=( )
    while IFS= read -r line
    do
        TEST_STRINGS+=( "$line" )
    done <<< "$(cat $TEST_FILE)"
    TEST_STRINGS_COUNT=${#TEST_STRINGS[@]}

    readarray -t ANSWERS < $ANSWER_FILE
    
    for (( J = 0; J < $TEST_STRINGS_COUNT; J++ ))
    do
        PROG_INPUT="$(printf "$CONVERTED_MACHINE\n${TEST_STRINGS[$J]}")"
        
        TMPFILENAME="tmp${RANDOM}${RANDOM}${RANDOM}${RANDOM}_${I}_${J}"
        echo "$PROG_INPUT" >$TMPFILENAME
        SIMULATION_OUTPUT=$(eval "cat $TMPFILENAME | $SIM_PROG_COMMAND")
        rm $TMPFILENAME
        
        TRIMMED_SIMULATION_OUTPUT="$(echo $SIMULATION_OUTPUT | xargs)"

        if [ "${TRIMMED_SIMULATION_OUTPUT: -2: 2}" == "-1" ]
        then
            if [ "${ANSWERS[$J]}" == "T" ]
            then
                echo "#######TEST $I FAILED####### ON STRING $(($J + 1))"
                # break
            fi
        else
            if [ "${ANSWERS[$J]}" == "F" ]
            then
                echo "#######TEST $I FAILED####### ON STRING $(($J + 1))"
                # break
            fi
        fi
    done
    printf "\n~~~~~~~~~~~TEST $I FINISHED~~~~~~~~~~~\n"
    
done
