from machine import TwoTapeTuringMachine, TwoTapeTuringMachineTransition


def main():
    n_states = int(input())

    TTTM = TwoTapeTuringMachine()
    for i in range(n_states):
        TTTM.add_state()

    for i in range(n_states - 1):
        info = input().split(" ")
        n_transitions = int(info[0])
        for j in range(n_transitions):
            TTTM.add_transition(i, TwoTapeTuringMachineTransition(info[1 + j * 7], info[2 + j * 7], int(info[3 + j * 7]), info[4 + j * 7], info[5 + j * 7], info[6 + j * 7], info[7 + j * 7]))

    TM = TTTM.to_single_tape()

    print(TM.to_string().strip())


if __name__ == "__main__":
    main()
