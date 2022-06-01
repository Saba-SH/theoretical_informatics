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
        # The states will branch for the read options of the two-tape turing machine
        # How many states we need for a single transition
        STATES_PER_TRANSITION = 32
        # States that every state has regardless its transitions
        NONBRANCH_STATES = 2
        # branch for every state for every pair that can be read from the two tapes
        BRANCH_LENGTH = STATES_PER_TRANSITION - NONBRANCH_STATES
        # one-tape machine states for every two-tape machine state
        STATES_PER_STATE = NONBRANCH_STATES + BRANCH_LENGTH * 9
        for i in range(len(self.state_transitions) - 1):
            ####272 ONE-TAPE-MACHINE STATES FOR EACH TWO-TAPE-MACHINE STATE####
            # but hey, it's O(1)
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
            ## here we branch based on the symbols we read from the tape
            ## and move to the right

            # all pairs that can possibly be read from the two tapes
            all_pairs = [SYMBOL_EMPTY + SYMBOL_EMPTY, SYMBOL_EMPTY + '0', SYMBOL_EMPTY + '1',
                        '0' + SYMBOL_EMPTY, '00', '01',
                        '1' + SYMBOL_EMPTY, '10', '11']
            
            # loop over all the read pairs and add states to perform the transitions
            for pair_index in range(len(all_pairs)):
                curr_pair = all_pairs[pair_index]
                # leave states empty if we have no transition for this uhhhh pair
                if curr_pair not in self.state_transitions[i]:
                    continue
                # the state that we're transitioning to with the current pair
                curr_target = self.state_transitions[i][curr_pair][0]
                # the pair that we should write when reading the current pair
                curr_write_pair = self.state_transitions[i][curr_pair][1]
                # the pair of directions that we should move in on the two tapes
                curr_direction_pair = self.state_transitions[i][curr_pair][2]
                
                ## start of the states for this pair transition
                branch_start = branching_point + 1 + BRANCH_LENGTH * pair_index

                ## update the first read symbol with the first write symbol and move right
                TM.add_transition(branching_point, TuringMachineTransition(DOT_SYMBOLS[NONDOT_SYMBOLS.index(curr_pair[0])], 
                branch_start, DOT_SYMBOLS[NONDOT_SYMBOLS.index(curr_write_pair[0])], 'R'))

                # keep moving right on the tape until we see a BABAMBABAM
                TM.add_transition(branch_start, TuringMachineTransition('0', branch_start, '0', 'R'))
                TM.add_transition(branch_start, TuringMachineTransition('1', branch_start, '1', 'R'))
                TM.add_transition(branch_start, TuringMachineTransition(SYMBOL_EMPTY, branch_start, SYMBOL_EMPTY, 'R'))

                # go past the BABAMBABAM
                TM.add_transition(branch_start, TuringMachineTransition(BABAMBABAM, branch_start + 1, BABAMBABAM, 'R'))

                # loop until we see a dotted symbol
                TM.add_transition(branch_start + 1, TuringMachineTransition('0', branch_start + 1, '0', 'R'))
                TM.add_transition(branch_start + 1, TuringMachineTransition('1', branch_start + 1, '1', 'R'))
                TM.add_transition(branch_start + 1, TuringMachineTransition(SYMBOL_EMPTY, branch_start + 1, SYMBOL_EMPTY, 'R'))

                # go past the dotted symbol and come back
                for dot_symbol in DOT_SYMBOLS:
                    TM.add_transition(branch_start + 1, TuringMachineTransition(dot_symbol, branch_start + 2, dot_symbol, 'R'))
                
                TM.add_transition(branch_start + 2, TuringMachineTransition(BABAMBABAM, branch_start + 3, BABAMBABAM, 'L'))
                TM.add_transition(branch_start + 2, TuringMachineTransition('0', branch_start + 3, '0', 'L'))
                TM.add_transition(branch_start + 2, TuringMachineTransition('1', branch_start + 3, '1', 'L'))
                TM.add_transition(branch_start + 2, TuringMachineTransition(SYMBOL_EMPTY, branch_start + 3, SYMBOL_EMPTY, 'L'))

                ## make the second change that we know we need to make
                TM.add_transition(branch_start + 3, TuringMachineTransition(DOT_SYMBOLS[NONDOT_SYMBOLS.index(curr_pair[1])],
                                branch_start + 4, DOT_SYMBOLS[NONDOT_SYMBOLS.index(curr_write_pair[1])], 'R'))

                # loop until we see a BABAMBABAM
                TM.add_transition(branch_start + 4, TuringMachineTransition('0', branch_start + 4, '0', 'R'))
                TM.add_transition(branch_start + 4, TuringMachineTransition('1', branch_start + 4, '1', 'R'))
                TM.add_transition(branch_start + 4, TuringMachineTransition(SYMBOL_EMPTY, branch_start + 4, SYMBOL_EMPTY, 'R'))
                # move left upon seeing the last BABAMBABAM of the uhhh tape
                TM.add_transition(branch_start + 4, TuringMachineTransition(BABAMBABAM, branch_start + 5, BABAMBABAM, 'L'))

                ## now we be at the end of the second tape
                we_at_end_of_tape = branch_start + 5
                # now uhhh loop to the first dotted symbol
                TM.add_transition(we_at_end_of_tape, TuringMachineTransition('0', we_at_end_of_tape, '0', 'L'))
                TM.add_transition(we_at_end_of_tape, TuringMachineTransition('1', we_at_end_of_tape, '1', 'L'))
                TM.add_transition(we_at_end_of_tape, TuringMachineTransition(SYMBOL_EMPTY, we_at_end_of_tape, SYMBOL_EMPTY, 'L'))
                # pass the dotted symbol and come back
                for dot_symbol in DOT_SYMBOLS:
                    TM.add_transition(we_at_end_of_tape, TuringMachineTransition(dot_symbol, we_at_end_of_tape + 1, dot_symbol, 'R'))
                
                TM.add_transition(we_at_end_of_tape + 1, TuringMachineTransition(BABAMBABAM, we_at_end_of_tape + 2, BABAMBABAM, 'L'))
                TM.add_transition(we_at_end_of_tape + 1, TuringMachineTransition('0', we_at_end_of_tape + 2, '0', 'L'))
                TM.add_transition(we_at_end_of_tape + 1, TuringMachineTransition('1', we_at_end_of_tape + 2, '1', 'L'))
                TM.add_transition(we_at_end_of_tape + 1, TuringMachineTransition(SYMBOL_EMPTY, we_at_end_of_tape + 2, SYMBOL_EMPTY, 'L'))

                ## now we choch the second dot to the left or right, depending on the actual transition that the two-tape machine has
                we_making_moves = we_at_end_of_tape + 2
                # we're doing the second movement first, then the first one. That's because we're passing right to left on the tape
                if curr_direction_pair[1] == 'L':
                    # left movement is easy, just move the dot to the left. the program will reject if there is a BABAMBABAM there
                    for symbol_index in range(len(NONDOT_SYMBOLS)):
                        # remove dot, move left, put dot, move left
                        TM.add_transition(we_making_moves, TuringMachineTransition(DOT_SYMBOLS[symbol_index], we_making_moves + 3,
                                                        NONDOT_SYMBOLS[symbol_index], 'L'))
                        TM.add_transition(we_making_moves + 3, TuringMachineTransition(NONDOT_SYMBOLS[symbol_index], we_making_moves + 4,
                                                        DOT_SYMBOLS[symbol_index], 'L'))
                else:
                    # right movement is easy too, for now. move BABAMBABAM to the right if we see it
                    for symbol_index in range(len(NONDOT_SYMBOLS)):
                        # remove dot, move right
                        TM.add_transition(we_making_moves, TuringMachineTransition(DOT_SYMBOLS[symbol_index], we_making_moves + 1,
                                                        NONDOT_SYMBOLS[symbol_index], 'R'))
                        # just dot the symbol if it's not BABAMBABAM
                        TM.add_transition(we_making_moves + 1, TuringMachineTransition(NONDOT_SYMBOLS[symbol_index], we_making_moves + 4,
                                                        DOT_SYMBOLS[symbol_index], 'L'))
                    # clear BABAMBABAM, move right, put BABAMBABAM, move left
                    TM.add_transition(we_making_moves + 1, TuringMachineTransition(BABAMBABAM, we_making_moves + 2, SYMBOL_EMPTY, 'R'))
                    TM.add_transition(we_making_moves + 2, TuringMachineTransition(SYMBOL_EMPTY, we_making_moves + 3, BABAMBABAM, 'L'))
                    TM.add_transition(we_making_moves + 3, TuringMachineTransition(SYMBOL_EMPTY, we_making_moves + 4, SYMBOL_EMPTY_DOT, 'L'))
                    
                # move left on the tape until we run into a dotted symbol
                we_joining = we_making_moves + 5
                TM.add_transition(we_making_moves + 4, TuringMachineTransition(BABAMBABAM, we_joining, BABAMBABAM, 'L'))
                TM.add_transition(we_making_moves + 4, TuringMachineTransition('0', we_joining, '0', 'L'))
                TM.add_transition(we_making_moves + 4, TuringMachineTransition('1', we_joining, '1', 'L'))
                TM.add_transition(we_making_moves + 4, TuringMachineTransition(SYMBOL_EMPTY, we_joining, SYMBOL_EMPTY, 'L'))

                TM.add_transition(we_joining, TuringMachineTransition(BABAMBABAM, we_joining, BABAMBABAM, 'L'))
                TM.add_transition(we_joining, TuringMachineTransition('0', we_joining, '0', 'L'))
                TM.add_transition(we_joining, TuringMachineTransition('1', we_joining, '1', 'L'))
                TM.add_transition(we_joining, TuringMachineTransition(SYMBOL_EMPTY, we_joining, SYMBOL_EMPTY, 'L'))

                # pass the dot symbol to the right and come back to it as always...
                for dot_symbol in DOT_SYMBOLS:
                    TM.add_transition(we_joining, TuringMachineTransition(dot_symbol, we_joining + 1, dot_symbol, 'R'))
                
                TM.add_transition(we_joining + 1, TuringMachineTransition(BABAMBABAM, we_joining + 2, BABAMBABAM, 'L'))
                TM.add_transition(we_joining + 1, TuringMachineTransition('0', we_joining + 2, '0', 'L'))
                TM.add_transition(we_joining + 1, TuringMachineTransition('1', we_joining + 2, '1', 'L'))
                TM.add_transition(we_joining + 1, TuringMachineTransition(SYMBOL_EMPTY, we_joining + 2, SYMBOL_EMPTY, 'L'))

                ## now we choch the first dot to the left or right
                we_back_at_it_again = we_joining + 2
                if curr_direction_pair[0] == 'L':
                    # left direction is easy again
                    for symbol_index in range(len(NONDOT_SYMBOLS)):
                        TM.add_transition(we_back_at_it_again, TuringMachineTransition(DOT_SYMBOLS[symbol_index], we_back_at_it_again + 11,
                                                            NONDOT_SYMBOLS[symbol_index], 'L'))
                        TM.add_transition(we_back_at_it_again + 11, TuringMachineTransition(NONDOT_SYMBOLS[symbol_index], we_back_at_it_again + 12,
                                                            DOT_SYMBOLS[symbol_index], 'L'))
                else:
                    # right direction. now we have to shift everything to the right if necessary
                    for symbol_index in range(len(NONDOT_SYMBOLS)):
                        # remove dot and move right
                        TM.add_transition(we_back_at_it_again, TuringMachineTransition(DOT_SYMBOLS[symbol_index], we_back_at_it_again + 1,
                                                            NONDOT_SYMBOLS[symbol_index], 'R'))
                        # put dot and move left if there is no BABAMBABAM
                        TM.add_transition(we_back_at_it_again + 1, TuringMachineTransition(NONDOT_SYMBOLS[symbol_index], we_back_at_it_again + 12,
                                                DOT_SYMBOLS[symbol_index], 'L'))
                    # BABAMBABAM? OOOOO, Trobule.
                    # put dotted empty symbol and move right
                    TM.add_transition(we_back_at_it_again + 1, TuringMachineTransition(BABAMBABAM, we_back_at_it_again + 2, SYMBOL_EMPTY_DOT, 'R'))
                    # oof
                    ALL_SYMBOLS_LIST = list(NONDOT_SYMBOLS) + list(DOT_SYMBOLS)     # excluding BABAMBABAM
                    for symbol_index in range(len(ALL_SYMBOLS_LIST)):
                        TM.add_transition(we_back_at_it_again + 2, TuringMachineTransition(ALL_SYMBOLS_LIST[symbol_index],
                                            we_back_at_it_again + 3 + symbol_index, BABAMBABAM, 'R'))

                    # moving things to the right
                    for symbol_index in range(len(ALL_SYMBOLS_LIST)):
                        for symbol_index_u in range(len(ALL_SYMBOLS_LIST)):
                            TM.add_transition(we_back_at_it_again + 3 + symbol_index, TuringMachineTransition(ALL_SYMBOLS_LIST[symbol_index_u],
                                        we_back_at_it_again + 3 + symbol_index_u, ALL_SYMBOLS_LIST[symbol_index], 'R'))

                    # reaching BABAMBABAM
                    for symbol_index in range(len(ALL_SYMBOLS_LIST)):
                        TM.add_transition(we_back_at_it_again + 3 + symbol_index, TuringMachineTransition(BABAMBABAM, we_back_at_it_again + 9,
                                        ALL_SYMBOLS_LIST[symbol_index], 'R'))

                    # put BABAMBABAM at the end 
                    TM.add_transition(we_back_at_it_again + 9, TuringMachineTransition(SYMBOL_EMPTY, we_back_at_it_again + 10, BABAMBABAM, 'L'))
                    # loop left
                    for nondot_symbol in NONDOT_SYMBOLS:
                        TM.add_transition(we_back_at_it_again + 10, TuringMachineTransition(nondot_symbol, we_back_at_it_again + 10,
                                            nondot_symbol, 'L'))
                    # pass dot symbol to the left
                    for dot_symbol in DOT_SYMBOLS:
                        TM.add_transition(we_back_at_it_again + 10, TuringMachineTransition(dot_symbol, we_back_at_it_again + 11,
                                            dot_symbol, 'L'))

                    # loop left
                    TM.add_transition(we_back_at_it_again + 11, TuringMachineTransition(BABAMBABAM, we_back_at_it_again + 11, BABAMBABAM, 'L'))
                    TM.add_transition(we_back_at_it_again + 11, TuringMachineTransition('0', we_back_at_it_again + 11, '0', 'L'))
                    TM.add_transition(we_back_at_it_again + 11, TuringMachineTransition('1', we_back_at_it_again + 11, '1', 'L'))
                    TM.add_transition(we_back_at_it_again + 11, TuringMachineTransition(SYMBOL_EMPTY, we_back_at_it_again + 11, SYMBOL_EMPTY, 'L'))

                    # pass dot symbol to the left
                    TM.add_transition(we_back_at_it_again + 11, TuringMachineTransition(SYMBOL_EMPTY_DOT, we_back_at_it_again + 12,
                                                SYMBOL_EMPTY_DOT, 'L'))

                TM.add_transition(we_back_at_it_again + 12, TuringMachineTransition('0', we_back_at_it_again + 13, '0', 'L'))
                TM.add_transition(we_back_at_it_again + 12, TuringMachineTransition('1', we_back_at_it_again + 13, '1', 'L'))
                TM.add_transition(we_back_at_it_again + 12, TuringMachineTransition(SYMBOL_EMPTY, we_back_at_it_again + 13, SYMBOL_EMPTY, 'L'))

                # loop left...
                TM.add_transition(we_back_at_it_again + 13, TuringMachineTransition('0', we_back_at_it_again + 13, '0', 'L'))
                TM.add_transition(we_back_at_it_again + 13, TuringMachineTransition('1', we_back_at_it_again + 13, '1', 'L'))
                TM.add_transition(we_back_at_it_again + 13, TuringMachineTransition(SYMBOL_EMPTY, we_back_at_it_again + 13, SYMBOL_EMPTY, 'L'))

                TM.add_transition(we_back_at_it_again + 13, TuringMachineTransition(BABAMBABAM, we_back_at_it_again + 14, BABAMBABAM, 'L'))
                # it is over. or is it?
                TM.add_transition(we_back_at_it_again + 14, TuringMachineTransition(BABAMBABAM, STATE_OFFSET + curr_target * STATES_PER_STATE, BABAMBABAM, 'L'))

            TM.add_state()

        ################################################################################
        """Return the constructed single-tape turing machine at the end"""
        return TM
