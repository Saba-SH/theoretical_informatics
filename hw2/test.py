import sys
from src.machine import TuringMachine, TuringMachineTransition, TwoTapeTuringMachine, TwoTapeTuringMachineTransition

def main():
    # take two-tape machine as input
    n_states = int(input())

    TTTM = TwoTapeTuringMachine()
    for i in range(n_states):
        TTTM.add_state()

    for i in range(n_states - 1):
        info = input().split(" ")
        n_transitions = int(info[0])
        for j in range(n_transitions):
            TTTM.add_transition(i, TwoTapeTuringMachineTransition(info[1 + j * 7], info[2 + j * 7], int(info[3 + j * 7]), info[4 + j * 7], info[5 + j * 7], info[6 + j * 7], info[7 + j * 7]))
    #
    # convert the machine to single tape
    TM = TTTM.to_single_tape()
    #
    # generate all strings of length at most first command-line argument
    strings = ['']
    lists = []
    
    for i in range(int(sys.argv[1])):
        lists.append([])

    lists[0].append('')

    for i in range(1, len(lists)):
        for s in lists[i - 1]:
            lists[i].append(s + '0')
            lists[i].append(s + '1')
        strings += lists[i]
    #
    # run both the single-tape and two-tape machine and compare their outputs
    for s in strings:
        # if len(TTTM.state_transitions) > 2 or len(TTTM.state_transitions[0]) > 6:
        #     continue
        tm_run = TM.run(s)
        tttm_run = TTTM.run(s)
        TM.reset()
        TTTM.reset()
        if tm_run[-2:] == '-1' and tttm_run[-2:] == '-1':
            # print("\""  + s + "\" REJECTED BY BOTH")
            continue
        if tm_run[-2:] != '-1' and tttm_run[-2:] != '-1':
            # print("\"" + s + "\" ACCEPTED BY BOTH")
            continue
        print(TTTM.to_string() + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" + tttm_run)
        print(TM.to_string() + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" + tm_run)
        print("COMPARISON FAILED ON STRING \"" + s + "\"")
        print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        break
    # 

if __name__ == "__main__":
    main()
