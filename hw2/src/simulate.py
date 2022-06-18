from machine import TuringMachine, TuringMachineTransition


def main():
    n_states = int(input())

    TM = TuringMachine()
    for i in range(n_states):
        TM.add_state()

    for i in range(n_states - 1):
        info = input().split(" ")
        n_transitions = int(info[0])
        for j in range(n_transitions):
            TM.add_transition(i, TuringMachineTransition(info[1 + j * 4], int(info[2 + j * 4]), info[3 + j * 4], info[4 + j * 4]))

    input_string = input()

    print(TM.run(input_string).strip())


if __name__ == "__main__":
    main()
