SYMBOL_EMPTY = '_'
# to separate two tapes of the two-tape turing machine
BABAMBABAM = ':'
# two-tape turing machines will only have 0 and 1 symbols on their tape. dots will mark the two heads
SYMBOL_ZERO_DOT = 'O'
SYMBOL_ONE_DOT = 'I'
SYMBOL_EMPTY_DOT = '^'
# keep lists of possible symbols for the sake of convenience
NONDOT_SYMBOLS = ['0', '1', SYMBOL_EMPTY]
DOT_SYMBOLS = [SYMBOL_ZERO_DOT, SYMBOL_ONE_DOT, SYMBOL_EMPTY_DOT]

class TuringMachineTransition:
    # returns a one-element dict:
    # key: tape symbol
    # value: three-element list _ target state, symbol to write on tape and direction(L/R)
    def dictized(self) -> dict:
        return {self.readSymbol : [self.target, self.writeSymbol, self.direction]}
    
    def __init__(self, readSymbol : str, target : int, writeSymbol : str, direction : str) -> None:
        self.readSymbol = readSymbol
        self.writeSymbol = writeSymbol
        self.direction = direction
        self.target = target


class TuringMachine:
    def __init__(self) -> None:
        self.state_transitions = []
        self.tape = []
        self.head = 0

    def add_state(self):
        # dict mapping tape symbols
        # to three-element lists(index of target state, symbol to write on tape, direction of head movement)
        self.state_transitions.append(dict())

    def add_transition(self, from_index : int, transition : TuringMachineTransition):
        self.state_transitions[from_index].update(transition.dictized())

    def run(self, input : str) -> str:
        for symbol in input:
            self.tape.append(symbol)

        # start at state with index 0
        curr_state_index = 0
        run_result = ""
        while True:
            # increase length of tape if head is past it
            while len(self.tape) <= self.head:
                self.tape.append(SYMBOL_EMPTY)
                self.tape.append(SYMBOL_EMPTY)
            
            # symbol read from tape
            c_read = self.tape[self.head]

            # reject if no transition from current state for current input
            if c_read not in self.state_transitions[curr_state_index]:
                # reject
                run_result += "-1"
                break
            
            # transition from the current state with the current input
            trans = self.state_transitions[curr_state_index][c_read]
            
            # write to tape
            self.tape[self.head] = trans[1]
            
            # move head
            if trans[2].upper() == 'L':
                self.head = 0 if self.head == 0 else self.head - 1
            elif trans[2].upper() == 'R':
                self.head = self.head + 1

            # accept the string and terminate work if we're transitioning to the last(accept) state
            if trans[0] == len(self.state_transitions) - 1:
                # accept
                run_result += str(len(self.state_transitions) - 1)
                break

            curr_state_index = trans[0]

            # record index of current state
            run_result += str(curr_state_index) + "\n"

        return run_result

    # returns a string representation of the machine in the form:
    # {total count of states}
    # for each state except the last one:
    #   {amount of transitions for the state} for each transition: {read symbol} {target state} {write symbol} {head movement direction(L/R)}
    def to_string(self) -> str:
        res = ""
        res += str(len(self.state_transitions)) + "\n"
        for i in range(len(self.state_transitions) - 1):
            res += str(len(self.state_transitions[i]))
            for transition_symbol in self.state_transitions[i]:
                res += " " + transition_symbol + " " + str(self.state_transitions[i][transition_symbol][0]) + " " + self.state_transitions[i][transition_symbol][1] + " " + self.state_transitions[i][transition_symbol][2]
            res += "\n"

        return res

class TwoTapeTuringMachineTransition:
    # returns a one-element dict:
    # key: two-element string _ symbols to read from the two tapes
    # value: three-element list _ target state, symbols to write on tape and directions
    def dictized(self) -> dict:
        return {self.readSymbol1 + self.readSymbol2 : [self.target, self.writeSymbol1 + self.writeSymbol2, self.direction1 + self.direction2]}

    def __init__(self, readSymbol1 : str, readSymbol2 : str, target : int, writeSymbol1 : str, writeSymbol2 : str, direction1 : str, direction2 : str) -> None:
        self.readSymbol1 = readSymbol1
        self.readSymbol2 = readSymbol2
        self.target = target
        self.writeSymbol1 = writeSymbol1
        self.writeSymbol2 = writeSymbol2
        self.direction1 = direction1
        self.direction2 = direction2

class TwoTapeTuringMachine:
    def __init__(self):
        self.state_transitions = []
        self.tape1 = []
        self.tape2 = []
        self.head1 = 0
        self.head2 = 0

    def add_state(self):
        # dict mapping two-symbol strings of tape symbols
        # to three-element lists(index of target state, symbols to write on tape, directions of head movement)
        self.state_transitions.append(dict())

    def add_transition(self, from_index : int, transition : TwoTapeTuringMachineTransition):
        self.state_transitions[from_index].update(transition.dictized())

    def to_single_tape(self) -> TuringMachine:
        ################################################################################
        TM = TuringMachine()
        ################################################################################
        """Setup:
            Add a separator at the beginning, shift input to the right(add one empty cell if no input),
            add separator at the end of input,
            add empty cell after second separator, add another separator after it,
            mark both heads(first symbol of input and the newly added empty cell) with dots.
            At the end, the actual head is standing at the first separator(first symbol on the actual tape)."""
        STATE_OFFSET = 11
        for i in range(STATE_OFFSET):
            TM.add_state()

        #####
        TM.add_transition(0, TuringMachineTransition('0', 1, BABAMBABAM, 'R'))
        TM.add_transition(0, TuringMachineTransition('1', 2, BABAMBABAM, 'R'))
        TM.add_transition(0, TuringMachineTransition(SYMBOL_EMPTY, 3, BABAMBABAM, 'R'))
        #####
        TM.add_transition(1, TuringMachineTransition('0', 1, '0', 'R'))
        TM.add_transition(1, TuringMachineTransition('1', 2, '0', 'R'))
        TM.add_transition(1, TuringMachineTransition(SYMBOL_EMPTY, 5, '0', 'R'))
        #####
        TM.add_transition(2, TuringMachineTransition('0', 1, '1', 'R'))
        TM.add_transition(2, TuringMachineTransition('1', 2, '1', 'R'))
        TM.add_transition(2, TuringMachineTransition(SYMBOL_EMPTY, 5, '1', 'R'))
        #####
        TM.add_transition(3, TuringMachineTransition(SYMBOL_EMPTY, 4, SYMBOL_EMPTY, 'R'))
        ######
        TM.add_transition(4, TuringMachineTransition(SYMBOL_EMPTY, 6, BABAMBABAM, 'R'))
        ######
        TM.add_transition(5, TuringMachineTransition(SYMBOL_EMPTY, 6, BABAMBABAM, 'R'))
        ######
        TM.add_transition(6, TuringMachineTransition(SYMBOL_EMPTY, 7, SYMBOL_EMPTY_DOT, 'R'))
        ######
        TM.add_transition(7, TuringMachineTransition(SYMBOL_EMPTY, 8, BABAMBABAM, 'L'))
        ######
        TM.add_transition(8, TuringMachineTransition(SYMBOL_EMPTY_DOT, 8, SYMBOL_EMPTY_DOT, 'L'))
        TM.add_transition(8, TuringMachineTransition(BABAMBABAM, 8, BABAMBABAM, 'L'))
        
        TM.add_transition(8, TuringMachineTransition(SYMBOL_EMPTY, 9, SYMBOL_EMPTY, 'L'))
        TM.add_transition(8, TuringMachineTransition('1', 9, '1', 'L'))
        TM.add_transition(8, TuringMachineTransition('0', 9, '0', 'L'))
        #####
        TM.add_transition(9, TuringMachineTransition('0', 9, '0', 'L'))
        TM.add_transition(9, TuringMachineTransition('1', 9, '1', 'L'))

        TM.add_transition(9, TuringMachineTransition(BABAMBABAM, 10, BABAMBABAM, 'R'))
        #####
        TM.add_transition(10, TuringMachineTransition(SYMBOL_EMPTY, 11, SYMBOL_EMPTY_DOT, 'L'))
        TM.add_transition(10, TuringMachineTransition('1', 11, SYMBOL_ONE_DOT, 'L'))
        TM.add_transition(10, TuringMachineTransition('0', 11, SYMBOL_ZERO_DOT, 'L'))
        #####
        """Setup is now complete. We are at state 11 
        with actual head of the single tape TM pointing at the beginning of the tape."""
        """States with index less than 11 shouldn't be touched any longer."""
        ################################################################################
        """Now we begin making states that actually correspond to
         the states of the two-tape turing machine."""
        # The states will branch at the read options of the two-tape turing machine
        SECOND_BRANCH_LENGTH = 32-7
        FIRST_BRANCH_LENGTH = SECOND_BRANCH_LENGTH * 3 + 4
        STATES_PER_STATE = FIRST_BRANCH_LENGTH * 3 + 3
        for i in range(len(self.state_transitions)):
            ####240 ONE-TAPE-MACHINE STATES FOR EACH TWO-TAPE-MACHINE STATE####
            for j in range(STATES_PER_STATE):
                TM.add_state()

            beninging = STATE_OFFSET + i * STATES_PER_STATE
            # loop in the same state until we reach a dotted symbol(two-tape machine head)
            TM.add_transition(beninging, TuringMachineTransition(BABAMBABAM, beninging, BABAMBABAM, 'R'))
            TM.add_transition(beninging, TuringMachineTransition('0', beninging, '0', 'R'))
            TM.add_transition(beninging, TuringMachineTransition('1', beninging, '1', 'R'))
            TM.add_transition(beninging, TuringMachineTransition(SYMBOL_EMPTY, beninging, SYMBOL_EMPTY, 'R'))

            # go one unit past the dotted symbol
            for DOT_SYMBOL in DOT_SYMBOLS:
                TM.add_transition(beninging, TuringMachineTransition(DOT_SYMBOL, beninging + 1, DOT_SYMBOL, 'R'))

            # come back to the dotted symbol
            TM.add_transition(beninging + 1, TuringMachineTransition(BABAMBABAM, beninging + 2, BABAMBABAM, 'L'))
            TM.add_transition(beninging + 1, TuringMachineTransition('0', beninging + 2, '0', 'L'))
            TM.add_transition(beninging + 1, TuringMachineTransition('1', beninging + 2, '1', 'L'))
            TM.add_transition(beninging + 1, TuringMachineTransition(SYMBOL_EMPTY, beninging + 2, SYMBOL_EMPTY, 'L'))

            branching_point = beninging + 2

            ## we are at the first head of the two-tape TM
            ## here we branch based on the symbol we read from the tape
            ## and move one unit to the right
            has_zero_1 = has_one_1 = has_empty_1 = '#'
            for transition_balls in self.state_transitions[i]:
                if transition_balls[0] == '0':
                    # save the symbol to which we're transitioning
                    has_zero_1 = self.state_transitions[i][transition_balls][1][0]
                    break

            for transition_balls in self.state_transitions[i]:
                if transition_balls[0] == '1':
                    has_one_1 = self.state_transitions[i][transition_balls][1][0]
                    break

            for transition_balls in self.state_transitions[i]:
                if transition_balls[0] == SYMBOL_EMPTY:
                    has_empty_1 = self.state_transitions[i][transition_balls][1][0]
                    break

            if has_zero_1 != '#':
                # update the dotted symbol and move one unit to the right
                TM.add_transition(branching_point, TuringMachineTransition(SYMBOL_ZERO_DOT, 
                branching_point + 1 + FIRST_BRANCH_LENGTH * 0,
                DOT_SYMBOLS[NONDOT_SYMBOLS.index[has_zero_1]], 'R'))
                
                # loop over all nondot symbols
                TM.add_transition(branching_point + 1, TuringMachineTransition('0', branching_point + 1, '0', 'R'))
                TM.add_transition(branching_point + 1, TuringMachineTransition('1', branching_point + 1, '1', 'R'))
                TM.add_transition(branching_point + 1, TuringMachineTransition(SYMBOL_EMPTY, branching_point + 1, SYMBOL_EMPTY, 'R'))
                # move over to the beginning of the "second tape"
                TM.add_transition(branching_point + 1, 
                TuringMachineTransition(BABAMBABAM, branching_point + 2, BABAMBABAM, 'R'))

                # loop over all nondot symbols
                TM.add_transition(branching_point + 2, TuringMachineTransition('0', branching_point + 2, '0', 'R'))
                TM.add_transition(branching_point + 2, TuringMachineTransition('1', branching_point + 2, '1', 'R'))
                TM.add_transition(branching_point + 2, TuringMachineTransition(SYMBOL_EMPTY, branching_point + 2, SYMBOL_EMPTY, 'R'))

                # go one unit past the dotted symbol
                for DOT_SYMBOL in DOT_SYMBOLS:
                    TM.add_transition(branching_point + 2, TuringMachineTransition(DOT_SYMBOL, branching_point + 3, DOT_SYMBOL, 'R'))

                # come back to the dotted symbol
                TM.add_transition(branching_point + 3, TuringMachineTransition(BABAMBABAM, branching_point + 4, BABAMBABAM, 'L'))
                TM.add_transition(branching_point + 3, TuringMachineTransition('0', branching_point + 4, '0', 'L'))
                TM.add_transition(branching_point + 3, TuringMachineTransition('1', branching_point + 4, '1', 'L'))
                TM.add_transition(branching_point + 3, TuringMachineTransition(SYMBOL_EMPTY, branching_point + 4, SYMBOL_EMPTY, 'L'))

                ## we are at the second head of the two-tape TM
                ## here we branch again based on the symbol we read from the tape
                ## and move one unit to the right
                has_zero_2 = has_one_2 = has_empty_2 = '#'
                for transition_balls in self.state_transitions[i]:
                    if transition_balls[1] == '0':
                    # save the symbol to which we're transitioning
                        has_zero_2 = self.state_transitions[i][transition_balls][1][1]
                        break

                for transition_balls in self.state_transitions[i]:
                    if transition_balls[1] == '1':
                        has_one_2 = self.state_transitions[i][transition_balls][1][1]
                        break

                for transition_balls in self.state_transitions[i]:
                    if transition_balls[1] == SYMBOL_EMPTY:
                        has_empty_2 = self.state_transitions[i][transition_balls][1][1]
                        break
                
                another_branching_point = branching_point + FIRST_BRANCH_LENGTH * 0 + 4
                if has_zero_2 != '#':
                    # update the dotted symbol and move one unit to the right
                    TM.add_transition(another_branching_point, TuringMachineTransition(SYMBOL_ZERO_DOT, 
                    another_branching_point + 1 + SECOND_BRANCH_LENGTH * 0,
                    DOT_SYMBOLS[NONDOT_SYMBOLS.index[has_zero_2]], 'R'))

                    # loop over all nondot symbols
                    TM.add_transition(another_branching_point + 1, TuringMachineTransition('0', another_branching_point + 1, '0', 'R'))
                    TM.add_transition(another_branching_point + 1, TuringMachineTransition('1', another_branching_point + 1, '1', 'R'))
                    TM.add_transition(another_branching_point + 1, TuringMachineTransition(SYMBOL_EMPTY, another_branching_point + 1, SYMBOL_EMPTY, 'R'))

                    # move to the end of the "second tape"
                    TM.add_transition(another_branching_point + 1, TuringMachineTransition(BABAMBABAM, another_branching_point + 2, BABAMBABAM, 'L'))

                    
                    a_new_start = another_branching_point + 2
                    # loop over all nondot symbols
                    TM.add_transition(a_new_start, TuringMachineTransition('0', a_new_start, '0', 'L'))
                    TM.add_transition(a_new_start, TuringMachineTransition('1', a_new_start, '1', 'L'))
                    TM.add_transition(a_new_start, TuringMachineTransition(SYMBOL_EMPTY, a_new_start, SYMBOL_EMPTY, 'L'))                    
                    # go past the dotted symbol
                    TM.add_transition(a_new_start, TuringMachineTransition(SYMBOL_ZERO_DOT, a_new_start + 1, SYMBOL_ZERO_DOT, 'R'))
                    TM.add_transition(a_new_start, TuringMachineTransition(SYMBOL_ONE_DOT, a_new_start + 1, SYMBOL_ONE_DOT, 'R'))
                    TM.add_transition(a_new_start, TuringMachineTransition(SYMBOL_EMPTY_DOT, a_new_start + 1, SYMBOL_EMPTY_DOT, 'R'))                    
                    # come back to the dotted symbol
                    TM.add_transition(a_new_start + 1, TuringMachineTransition(BABAMBABAM, a_new_start + 2, BABAMBABAM, 'L'))
                    TM.add_transition(a_new_start + 1, TuringMachineTransition('0', a_new_start + 2, '0', 'L'))
                    TM.add_transition(a_new_start + 1, TuringMachineTransition('1', a_new_start + 2, '1', 'L'))
                    TM.add_transition(a_new_start + 1, TuringMachineTransition(SYMBOL_EMPTY, a_new_start + 2, SYMBOL_EMPTY, 'L'))

                    ## next movement depends on whether the two-tape machine moves second head to the left or right
                    different_kinda_branching_point = a_new_start + 2
                    if self.state_transitions[i]['00'][2][1] == 'L':
                        # move the dot over to the left
                        for dot_symbol in DOT_SYMBOLS:
                            TM.add_transition(different_kinda_branching_point, TuringMachineTransition(dot_symbol, different_kinda_branching_point + 3, NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)], 'L'))
                        for nondot_symbol in NONDOT_SYMBOLS:
                            TM.add_transition(different_kinda_branching_point + 3, TuringMachineTransition(nondot_symbol, different_kinda_branching_point + 4, DOT_SYMBOLS[NONDOT_SYMBOLS.index(nondot_symbol)], 'L'))
                    else:
                        # move the dot over to the right
                        for dot_symbol in DOT_SYMBOLS:
                            TM.add_transition(different_kinda_branching_point, TuringMachineTransition(dot_symbol, different_kinda_branching_point + 1, NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)], 'R'))
                        # move BABAMBABAM one unit to the right if necessary
                        TM.add_transition(different_kinda_branching_point + 1, TuringMachineTransition(BABAMBABAM, different_kinda_branching_point + 2, SYMBOL_EMPTY, 'R'))
                        TM.add_transition(different_kinda_branching_point + 2, TuringMachineTransition(SYMBOL_EMPTY, different_kinda_branching_point + 3, BABAMBABAM, 'L'))
                        TM.add_transition(different_kinda_branching_point + 3, TuringMachineTransition(SYMBOL_EMPTY, different_kinda_branching_point + 4, SYMBOL_EMPTY_DOT, 'L'))
                        # just place dot if BABAMBABAM is ok
                        for nondot_symbol in NONDOT_SYMBOLS:
                            TM.add_transition(different_kinda_branching_point + 1, TuringMachineTransition(nondot_symbol, different_kinda_branching_point + 4, DOT_SYMBOLS[NONDOT_SYMBOLS.index(nondot_symbol)], 'L'))

                    connection_point = different_kinda_branching_point + 5
                    TM.add_transition(different_kinda_branching_point + 4, TuringMachineTransition(BABAMBABAM, connection_point, BABAMBABAM, 'L'))
                    TM.add_transition(different_kinda_branching_point + 4, TuringMachineTransition('0', connection_point, '0', 'L'))
                    TM.add_transition(different_kinda_branching_point + 4, TuringMachineTransition('1', connection_point, '1', 'L'))
                    TM.add_transition(different_kinda_branching_point + 4, TuringMachineTransition(SYMBOL_EMPTY, connection_point, SYMBOL_EMPTY, 'L'))

                    # loop over all nondot symbols
                    TM.add_transition(connection_point, TuringMachineTransition(BABAMBABAM, connection_point, BABAMBABAM, 'L'))
                    TM.add_transition(connection_point, TuringMachineTransition('0', connection_point, '0', 'L'))
                    TM.add_transition(connection_point, TuringMachineTransition('1', connection_point, '1', 'L'))
                    TM.add_transition(connection_point, TuringMachineTransition(SYMBOL_EMPTY, connection_point, SYMBOL_EMPTY, 'L'))

                    # skip to the right of the dot symbol
                    for dot_symbol in DOT_SYMBOLS:
                        TM.add_transition(connection_point, TuringMachineTransition(dot_symbol, connection_point + 1, dot_symbol, 'R'))
                    # go back to the dot symbol
                    TM.add_transition(connection_point + 1, TuringMachineTransition(BABAMBABAM, connection_point + 2, BABAMBABAM, 'L'))
                    TM.add_transition(connection_point + 1, TuringMachineTransition('0', connection_point + 2, '0', 'L'))
                    TM.add_transition(connection_point + 1, TuringMachineTransition('1', connection_point + 2, '1', 'L'))
                    TM.add_transition(connection_point + 1, TuringMachineTransition(SYMBOL_EMPTY, connection_point + 2, SYMBOL_EMPTY, 'L'))

                    ## next movement depends on whether the two-tape machine moves second head to the left or right
                    another_different_kinda_branching_point = connection_point + 2
                    if self.state_transitions[i]['00'][2][0] == 'L':
                        # move the dot over to the left
                        for dot_symbol in DOT_SYMBOLS:
                            TM.add_transition(another_different_kinda_branching_point, TuringMachineTransition(dot_symbol, another_different_kinda_branching_point + 11, NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)], 'L'))
                        for nondot_symbol in NONDOT_SYMBOLS:
                            TM.add_transition(another_different_kinda_branching_point + 11, TuringMachineTransition(nondot_symbol, another_different_kinda_branching_point + 12, DOT_SYMBOLS[NONDOT_SYMBOLS.index(nondot_symbol)], 'L'))
                    else:
                        # move the dot over to the right
                        for dot_symbol in DOT_SYMBOLS:
                            TM.add_transition(another_different_kinda_branching_point, TuringMachineTransition(dot_symbol, another_different_kinda_branching_point + 1, NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)], 'R'))
                        # shift everything over to the right if necessary
                        TM.add_transition(another_different_kinda_branching_point + 1, TuringMachineTransition(BABAMBABAM, another_different_kinda_branching_point + 2, SYMBOL_EMPTY_DOT, 'R'))

                        TM.add_transition(another_different_kinda_branching_point + 2, TuringMachineTransition('0', another_different_kinda_branching_point + 3, BABAMBABAM, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 2, TuringMachineTransition('1', another_different_kinda_branching_point + 4, BABAMBABAM, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 2, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 5, BABAMBABAM, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 2, TuringMachineTransition(SYMBOL_ZERO_DOT, another_different_kinda_branching_point + 6, BABAMBABAM, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 2, TuringMachineTransition(SYMBOL_ONE_DOT, another_different_kinda_branching_point + 7, BABAMBABAM, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 2, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 8, BABAMBABAM, 'R'))


                        TM.add_transition(another_different_kinda_branching_point + 3, TuringMachineTransition('0', another_different_kinda_branching_point + 3, '0', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 3, TuringMachineTransition('1', another_different_kinda_branching_point + 4, '0', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 3, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 5, '0', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 3, TuringMachineTransition(SYMBOL_ZERO_DOT, another_different_kinda_branching_point + 6, '0', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 3, TuringMachineTransition(SYMBOL_ONE_DOT, another_different_kinda_branching_point + 7, '0', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 3, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 8, '0', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 3, TuringMachineTransition(BABAMBABAM, another_different_kinda_branching_point + 9, '0', 'R'))

                        TM.add_transition(another_different_kinda_branching_point + 4, TuringMachineTransition('0', another_different_kinda_branching_point + 3, '1', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 4, TuringMachineTransition('1', another_different_kinda_branching_point + 4, '1', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 4, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 5, '1', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 4, TuringMachineTransition(SYMBOL_ZERO_DOT, another_different_kinda_branching_point + 6, '1', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 4, TuringMachineTransition(SYMBOL_ONE_DOT, another_different_kinda_branching_point + 7, '1', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 4, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 8, '1', 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 4, TuringMachineTransition(BABAMBABAM, another_different_kinda_branching_point + 9, '1', 'R'))
                        
                        TM.add_transition(another_different_kinda_branching_point + 5, TuringMachineTransition('0', another_different_kinda_branching_point + 3, SYMBOL_EMPTY, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 5, TuringMachineTransition('1', another_different_kinda_branching_point + 4, SYMBOL_EMPTY, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 5, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 5, SYMBOL_EMPTY, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 5, TuringMachineTransition(SYMBOL_ZERO_DOT, another_different_kinda_branching_point + 6, SYMBOL_EMPTY, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 5, TuringMachineTransition(SYMBOL_ONE_DOT, another_different_kinda_branching_point + 7, SYMBOL_EMPTY, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 5, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 8, SYMBOL_EMPTY, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 5, TuringMachineTransition(BABAMBABAM, another_different_kinda_branching_point + 9, SYMBOL_EMPTY, 'R'))

                        TM.add_transition(another_different_kinda_branching_point + 6, TuringMachineTransition('0', another_different_kinda_branching_point + 3, SYMBOL_ZERO_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 6, TuringMachineTransition('1', another_different_kinda_branching_point + 4, SYMBOL_ZERO_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 6, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 5, SYMBOL_ZERO_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 6, TuringMachineTransition(SYMBOL_ZERO_DOT, another_different_kinda_branching_point + 6, SYMBOL_ZERO_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 6, TuringMachineTransition(SYMBOL_ONE_DOT, another_different_kinda_branching_point + 7, SYMBOL_ZERO_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 6, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 8, SYMBOL_ZERO_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 6, TuringMachineTransition(BABAMBABAM, another_different_kinda_branching_point + 9, SYMBOL_ZERO_DOT, 'R'))

                        TM.add_transition(another_different_kinda_branching_point + 7, TuringMachineTransition('0', another_different_kinda_branching_point + 3, SYMBOL_ONE_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 7, TuringMachineTransition('1', another_different_kinda_branching_point + 4, SYMBOL_ONE_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 7, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 5, SYMBOL_ONE_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 7, TuringMachineTransition(SYMBOL_ZERO_DOT, another_different_kinda_branching_point + 6, SYMBOL_ONE_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 7, TuringMachineTransition(SYMBOL_ONE_DOT, another_different_kinda_branching_point + 7, SYMBOL_ONE_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 7, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 8, SYMBOL_ONE_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 7, TuringMachineTransition(BABAMBABAM, another_different_kinda_branching_point + 9, SYMBOL_ONE_DOT, 'R'))

                        TM.add_transition(another_different_kinda_branching_point + 8, TuringMachineTransition('0', another_different_kinda_branching_point + 3, SYMBOL_EMPTY_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 8, TuringMachineTransition('1', another_different_kinda_branching_point + 4, SYMBOL_EMPTY_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 8, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 5, SYMBOL_EMPTY_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 8, TuringMachineTransition(SYMBOL_ZERO_DOT, another_different_kinda_branching_point + 6, SYMBOL_EMPTY_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 8, TuringMachineTransition(SYMBOL_ONE_DOT, another_different_kinda_branching_point + 7, SYMBOL_EMPTY_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 8, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 8, SYMBOL_EMPTY_DOT, 'R'))
                        TM.add_transition(another_different_kinda_branching_point + 8, TuringMachineTransition(BABAMBABAM, another_different_kinda_branching_point + 9, SYMBOL_EMPTY_DOT, 'R'))
                        
                        # place a BABAMBABAM at the end of the "second tape" and start moving left
                        TM.add_transition(another_different_kinda_branching_point + 9, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 10, BABAMBABAM, 'L'))
                        # loop left until a dotted symbol
                        TM.add_transition(another_different_kinda_branching_point + 10, TuringMachineTransition('0', another_different_kinda_branching_point + 10, '0', 'L'))
                        TM.add_transition(another_different_kinda_branching_point + 10, TuringMachineTransition('1', another_different_kinda_branching_point + 10, '1', 'L'))
                        TM.add_transition(another_different_kinda_branching_point + 10, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 10, SYMBOL_EMPTY, 'L'))
                        # go past the dotted symbol to the left
                        TM.add_transition(another_different_kinda_branching_point + 10, TuringMachineTransition(SYMBOL_ZERO_DOT, another_different_kinda_branching_point + 11, SYMBOL_ZERO_DOT, 'L'))
                        TM.add_transition(another_different_kinda_branching_point + 10, TuringMachineTransition(SYMBOL_ONE_DOT, another_different_kinda_branching_point + 11, SYMBOL_ONE_DOT, 'L'))
                        TM.add_transition(another_different_kinda_branching_point + 10, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 11, SYMBOL_EMPTY_DOT, 'L'))
                        # loop left until the second dotted symbol
                        TM.add_transition(another_different_kinda_branching_point + 11, TuringMachineTransition(BABAMBABAM, another_different_kinda_branching_point + 11, BABAMBABAM, 'L'))
                        TM.add_transition(another_different_kinda_branching_point + 11, TuringMachineTransition('0', another_different_kinda_branching_point + 11, '0', 'L'))
                        TM.add_transition(another_different_kinda_branching_point + 11, TuringMachineTransition('1', another_different_kinda_branching_point + 11, '1', 'L'))
                        TM.add_transition(another_different_kinda_branching_point + 11, TuringMachineTransition(SYMBOL_EMPTY, another_different_kinda_branching_point + 11, SYMBOL_EMPTY, 'L'))
                        # pass the second dotted symbol to the left
                        TM.add_transition(another_different_kinda_branching_point + 11, TuringMachineTransition(SYMBOL_EMPTY_DOT, another_different_kinda_branching_point + 12, SYMBOL_EMPTY_DOT, 'L'))
                        # just place dot if no shifting is needed
                        for nondot_symbol in NONDOT_SYMBOLS:
                            TM.add_transition(another_different_kinda_branching_point + 1, TuringMachineTransition(nondot_symbol, another_different_kinda_branching_point + 12, DOT_SYMBOLS[NONDOT_SYMBOLS.index(nondot_symbol)], 'L'))
                            
                    another_connection_point = another_different_kinda_branching_point + 13
                    TM.add_transition(another_different_kinda_branching_point + 12, TuringMachineTransition('0', another_connection_point, '0', 'L'))
                    TM.add_transition(another_different_kinda_branching_point + 12, TuringMachineTransition('1', another_connection_point, '1', 'L'))
                    TM.add_transition(another_different_kinda_branching_point + 12, TuringMachineTransition(SYMBOL_EMPTY, another_connection_point, SYMBOL_EMPTY, 'L'))
                    # loop all the way to the left of the actual tape
                    TM.add_transition(another_connection_point, TuringMachineTransition('0', another_connection_point, '0', 'L'))
                    TM.add_transition(another_connection_point, TuringMachineTransition('1', another_connection_point, '1', 'L'))
                    TM.add_transition(another_connection_point, TuringMachineTransition(SYMBOL_EMPTY, another_connection_point, SYMBOL_EMPTY, 'L'))

                    final_point = another_connection_point + 1
                    TM.add_transition(another_connection_point, TuringMachineTransition(BABAMBABAM, final_point, BABAMBABAM, 'L'))
                    # add actual transition to a state that the two-tape machine actually wanted to transition to
                    TM.add_transition(final_point, TuringMachineTransition(BABAMBABAM, STATE_OFFSET + self.state_transitions[i]['00'][0] * STATES_PER_STATE, BABAMBABAM, 'L'))
                    
                    ####################################################################################################################

                    

        ################################################################################
        """Return the constructed single-tape turing machine at the end"""
        return TM
