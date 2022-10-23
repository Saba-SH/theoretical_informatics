#! /bin/bash

# amount of machines to generate
GENERATED_MACHINES=256
# maximum amount of states in a single machine
MAX_STATE_AMOUNT=16
# all strings up to this length will be generated
MAX_TEST_STRING_LENGTH=7
# longest time that one test is allowed to run for(necessary for avoiding infinite cycles)
TIMEOUT_DURATION=0.5

# command for clearing old generated machines
CLEAR_COMMAND="rm machines/*"
# command for generating new machines
GENERATION_COMMAND="python3 generate_machines.py $GENERATED_MACHINES $MAX_STATE_AMOUNT"
# command for listing filenames of machines
LISTING_COMMAND="ls machines/*"
# command for running a test on a single machine
TEST_COMMAND="python3 test.py $MAX_TEST_STRING_LENGTH"

################################################################
echo "clearing old machines"
$CLEAR_COMMAND
echo "generating new machines"
$GENERATION_COMMAND
echo "starting tests"
TEST_NUMBER=1
for machine in $($LISTING_COMMAND)
do
    cat "$machine" | timeout $TIMEOUT_DURATION $TEST_COMMAND;
    echo -ne "test $TEST_NUMBER/$GENERATED_MACHINES"\\r
    ((TEST_NUMBER++))
done
echo && echo "testing finished"
