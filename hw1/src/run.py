from automata import NFA

def nfa_result(nfa : "NFA", string : str):
    res = ""

    # set of all possible states at a given time
    possible_states = set([0])
    
    for s in string:
        # set of all possible states after reading the current symbol
        new_possible_states = set()
        # update the new possible states with moves from each currently possible state
        for current_possible_state in possible_states:
            new_possible_states.update(nfa.next_states(current_possible_state, s))

        # update the currently possible states
        possible_states = new_possible_states

        # answer to whether one of the currently possible states is an accept state
        curr_ans = 'N'
        # iterate over the set of possible states
        for possible_state in possible_states:
            # if there's at least one accept state possible, make current answer positive and break loop
            if possible_state in nfa.accept_states:
                curr_ans = 'Y'
                break

        res += curr_ans

    return res

def main():
    string = input()
    
    # read and process the first line
    desc = input().split(' ')
    n_states = int(desc[0])
    n_acc_states = int(desc[1])
    n_total_transitions = int(desc[2])

    # start constructing the NFA 
    states = []
    for i in range(n_states):
        states.append(dict())
    nfa = NFA(states, set())

    # read the accept states
    accept_states = input().split(' ')
    for i in range(len(accept_states)):
        accept_states[i] = int(accept_states[i])
    
    # set the accept states
    nfa.accept_states = set(accept_states)

    # take the transitions of each state
    for i in range(n_states):
        # info about the transitions of a single state
        info = input().split(' ')
        # number of transitions from the current state
        n_transitions = int(info[0])
        # position in the list of descriptions of transitions
        pos = 1

        for j in range(n_transitions):
            # read the symbol and state of the transition, moving pos forward
            symbol = info[pos]
            pos += 1
            state = int(info[pos])
            pos += 1
            # add the transition: ith state, current symbol -> current state
            if symbol not in nfa.states[i]:
                nfa.states[i][symbol] = set()
            
            nfa.states[i][symbol].add(state)

    print(nfa_result(nfa, string))

if __name__ == "__main__":
    main()
