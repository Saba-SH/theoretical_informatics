SYMBOL_EMPTY = '_'
# to separate two tapes of the two-tape turing machine
BABAMBABAM = 'H'
# two-tape turing machines will only have 0 and 1 symbols on their tape. dots will mark the two heads
SYMBOL_ZERO_DOT = 'O'
SYMBOL_ONE_DOT = 'I'
SYMBOL_EMPTY_DOT = 'E'
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

    def run(self, input_string : str) -> str:
        for symbol in input_string:
            self.tape.append(symbol)

        # start at state with index 0
        curr_state_index = 0
        run_result = ""
        while True:
            # increase length of tape if head is past it
            while len(self.tape) <= self.head:
                self.tape.append(SYMBOL_EMPTY)
                # self.tape.append(SYMBOL_EMPTY)
            
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

    # empties the tape and moves head to the beginning of the tape
    def reset(self):
        self.tape = []
        self.head = 0

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
        """Strategy for a transition:
            1. Move left to right on the tape, changing the dotted symbols as we do so.
            2. Move right to left, moving the dots left to right as necessary. Might need to shift things to the right."""
        # The states will branch for the read options of the two-tape turing machine
        # How many states we need for a single transition
        STATES_PER_TRANSITION = 32
        # States that every state has regardless its transitions
        NONBRANCH_STATES = 3
        # branch for second read symbol
        SECOND_BRANCH_LENGTH = STATES_PER_TRANSITION - 7
        # branch for first read symbol
        FIRST_BRANCH_LENGTH = SECOND_BRANCH_LENGTH * 3 + 7 - NONBRANCH_STATES
        # amount of one-tape machine states for every two-tape machine state
        STATES_PER_STATE = NONBRANCH_STATES + FIRST_BRANCH_LENGTH * 3
        for i in range(len(self.state_transitions) - 1):
            ####240 ONE-TAPE-MACHINE STATES FOR EACH TWO-TAPE-MACHINE STATE####
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
            for dot_symbol in DOT_SYMBOLS:
                TM.add_transition(beninging, TuringMachineTransition(dot_symbol, beninging + 1, dot_symbol, 'R'))

            # come back to the dotted symbol
            TM.add_transition(beninging + 1, TuringMachineTransition(BABAMBABAM, beninging + 2, BABAMBABAM, 'L'))
            TM.add_transition(beninging + 1, TuringMachineTransition('0', beninging + 2, '0', 'L'))
            TM.add_transition(beninging + 1, TuringMachineTransition('1', beninging + 2, '1', 'L'))
            TM.add_transition(beninging + 1, TuringMachineTransition(SYMBOL_EMPTY, beninging + 2, SYMBOL_EMPTY, 'L'))

            first_branching_point = beninging + 2

            ## we are at the first head of the two-tape TM
            ## here we branch based on the symbols we read from the tape
            ## and move to the right

            # all pairs that can possibly be read from the two tapes
            all_pairs = [SYMBOL_EMPTY + SYMBOL_EMPTY, SYMBOL_EMPTY + '0', SYMBOL_EMPTY + '1',
                        '0' + SYMBOL_EMPTY, '00', '01',
                        '1' + SYMBOL_EMPTY, '10', '11']
            
            # loop over all the read pairs and add necessary transitions
            for pair_index in range(len(all_pairs)):
                # the pair to be read from the tape
                curr_read_pair = all_pairs[pair_index]
                # skip this pair if we don't have a transition for it
                if curr_read_pair not in self.state_transitions[i]:
                    continue
                
                # the state that we're transitioning to in the two-tape machine
                curr_target_state = self.state_transitions[i][curr_read_pair][0]
                # the pair of symbols that we're writing
                curr_write_pair = self.state_transitions[i][curr_read_pair][1]
                # the directions that the heads are taking
                curr_directions = self.state_transitions[i][curr_read_pair][2]

                # we branch first at the first read symbol
                first_branch_start = first_branching_point + 1 + FIRST_BRANCH_LENGTH * (pair_index // 3)
                ## change the current dotted read symbol with the dotted equivalent of the write symbol
                TM.add_transition(first_branching_point, TuringMachineTransition(DOT_SYMBOLS[NONDOT_SYMBOLS.index(curr_read_pair[0])], 
                                first_branch_start, DOT_SYMBOLS[NONDOT_SYMBOLS.index(curr_write_pair[0])], 'R'))

                # loop right in the same state
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(first_branch_start, TuringMachineTransition(nondot_symbol, first_branch_start, nondot_symbol, 'R'))

                # move to the start of the second tape(right after the BABAMBABAM)
                TM.add_transition(first_branch_start, TuringMachineTransition(BABAMBABAM, first_branch_start + 1, BABAMBABAM, 'R'))
                # loop right again
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(first_branch_start + 1, TuringMachineTransition(nondot_symbol, first_branch_start + 1, nondot_symbol, 'R'))

                # pass the dotted symbol to the right
                for dot_symbol in DOT_SYMBOLS:
                    TM.add_transition(first_branch_start + 1, TuringMachineTransition(dot_symbol, first_branch_start + 2, dot_symbol, 'R'))

                second_branching_point = first_branch_start + 3
                # come back again
                TM.add_transition(first_branch_start + 2, TuringMachineTransition(BABAMBABAM, second_branching_point, BABAMBABAM, 'L'))
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(first_branch_start + 2, TuringMachineTransition(nondot_symbol, second_branching_point, nondot_symbol, 'L'))

                # we branch again at the second read symbol
                second_branch_start = second_branching_point + 1 + SECOND_BRANCH_LENGTH * (pair_index % 3)
                ## change the current dotted read symbol with the dotted equivalent of the write symbol
                TM.add_transition(second_branching_point, TuringMachineTransition(DOT_SYMBOLS[NONDOT_SYMBOLS.index(curr_read_pair[1])], 
                                second_branch_start, DOT_SYMBOLS[NONDOT_SYMBOLS.index(curr_write_pair[1])], 'R'))
                
                # loop right all the way to the end of the second tape
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(second_branch_start, TuringMachineTransition(nondot_symbol, second_branch_start, nondot_symbol, 'R'))
                # come back to the left of the BABAMBABAM(at the end of the second tape)
                TM.add_transition(second_branch_start, TuringMachineTransition(BABAMBABAM, second_branch_start + 1, BABAMBABAM, 'L'))

                ## now we begin moving right to left and moving the heads of the tapes
                # loop left until we encounter a dotted symbol
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(second_branch_start + 1, TuringMachineTransition(nondot_symbol, second_branch_start + 1, nondot_symbol, 'L'))

                # go past the dotted symbol to the right
                for dot_symbol in DOT_SYMBOLS:
                    TM.add_transition(second_branch_start + 1, TuringMachineTransition(dot_symbol, second_branch_start + 2, dot_symbol, 'R'))
                # come back to it...
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(second_branch_start + 2, TuringMachineTransition(nondot_symbol, second_branch_start + 3, nondot_symbol, 'L'))
                TM.add_transition(second_branch_start + 2, TuringMachineTransition(BABAMBABAM, second_branch_start + 3, BABAMBABAM, 'L'))
                
                ## how the next states are configured depends on whether the second head is moving left or right
                second_head_move_point = second_branch_start + 3
                # the movement will be all the same from this point despite the movement direction
                common_point_1 = second_head_move_point + 5
                
                if curr_directions[1] == 'L':
                    # left movement is easy: move the dot to the left. If the dot is at the beginning of the tape, don't move it
                    for dot_symbol in DOT_SYMBOLS:
                        TM.add_transition(second_head_move_point, TuringMachineTransition(dot_symbol, second_head_move_point + 3,
                                    NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)], 'L'))
                        TM.add_transition(second_head_move_point + 3, TuringMachineTransition(NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)],
                                    second_head_move_point + 4, dot_symbol, 'L'))
                    TM.add_transition(second_head_move_point + 3, TuringMachineTransition(BABAMBABAM, second_head_move_point + 3, 
                                    BABAMBABAM, 'R'))
                else:
                    for dot_symbol in DOT_SYMBOLS:
                        # simple case
                        TM.add_transition(second_head_move_point, TuringMachineTransition(dot_symbol, second_head_move_point + 1,
                                    NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)], 'R'))
                        TM.add_transition(second_head_move_point + 1, TuringMachineTransition(NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)],
                                    second_head_move_point + 4, dot_symbol, 'L'))
                    # case when the head is at the right end of the tape: we need to move BABAMBABAM to the right
                    TM.add_transition(second_head_move_point + 1, TuringMachineTransition(BABAMBABAM, second_head_move_point + 2,
                                SYMBOL_EMPTY, 'R'))
                    TM.add_transition(second_head_move_point + 2, TuringMachineTransition(SYMBOL_EMPTY, second_head_move_point + 3,
                                BABAMBABAM, 'L'))
                    TM.add_transition(second_head_move_point + 3, TuringMachineTransition(SYMBOL_EMPTY, second_head_move_point + 4,
                                SYMBOL_EMPTY_DOT, 'L'))
                # skip one unit to the left
                TM.add_transition(second_head_move_point + 4, TuringMachineTransition(BABAMBABAM, common_point_1, BABAMBABAM, 'L'))
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(second_head_move_point + 4, TuringMachineTransition(nondot_symbol, common_point_1, nondot_symbol, 'L'))
                # loop left in the common point
                TM.add_transition(common_point_1, TuringMachineTransition(BABAMBABAM, common_point_1, BABAMBABAM, 'L'))
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(common_point_1, TuringMachineTransition(nondot_symbol, common_point_1, nondot_symbol, 'L'))
                # move to the right of the first dot symbol
                for dot_symbol in DOT_SYMBOLS:
                    TM.add_transition(common_point_1, TuringMachineTransition(dot_symbol, common_point_1 + 1, dot_symbol, 'R'))
                # komm zurück
                TM.add_transition(common_point_1 + 1, TuringMachineTransition(BABAMBABAM, common_point_1 + 2, BABAMBABAM, 'L'))
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(common_point_1 + 1, TuringMachineTransition(nondot_symbol, common_point_1 + 2, nondot_symbol, 'L'))
                
                ## how the next states are configured yet again depends on the movement of the head. this time the first head.
                first_head_move_point = common_point_1 + 2
                common_point_2 = first_head_move_point + 13
                if curr_directions[0] == 'L':
                    # left direction is easy again
                    for dot_symbol in DOT_SYMBOLS:
                        TM.add_transition(first_head_move_point, TuringMachineTransition(dot_symbol, first_head_move_point + 11,
                                    NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)], 'L'))
                        TM.add_transition(first_head_move_point + 11, TuringMachineTransition(NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)],
                                    first_head_move_point + 12, dot_symbol, 'L'))
                    TM.add_transition(first_head_move_point + 11, TuringMachineTransition(BABAMBABAM, first_head_move_point + 11,
                                    BABAMBABAM, 'R'))
                else:
                    for dot_symbol in DOT_SYMBOLS:
                        # simple case
                        TM.add_transition(first_head_move_point, TuringMachineTransition(dot_symbol, first_head_move_point + 1,
                                    NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)], 'R'))
                        TM.add_transition(first_head_move_point + 1, TuringMachineTransition(NONDOT_SYMBOLS[DOT_SYMBOLS.index(dot_symbol)],
                                    first_head_move_point + 12, dot_symbol, 'L'))
                    # this time we have to shift a lot of stuff if we're at the right end of the first tape
                    TM.add_transition(first_head_move_point + 1, TuringMachineTransition(BABAMBABAM, first_head_move_point + 2, 
                                SYMBOL_EMPTY_DOT, 'R'))
                    # challenge: make sense of the next 10 lines without any comments
                    all_symbols = NONDOT_SYMBOLS + DOT_SYMBOLS
                    for symbol_index in range(len(all_symbols)):
                        TM.add_transition(first_head_move_point + 2, TuringMachineTransition(all_symbols[symbol_index],
                                first_head_move_point + 3 + symbol_index, BABAMBABAM, 'R'))
                    for state_index in range(first_head_move_point + 3, first_head_move_point + 9):
                        for symbol_index in range(len(all_symbols)):
                            TM.add_transition(state_index, TuringMachineTransition(all_symbols[symbol_index], 
                                first_head_move_point + 3 + symbol_index, all_symbols[state_index - first_head_move_point - 3], 'R'))
                        TM.add_transition(state_index, TuringMachineTransition(BABAMBABAM, first_head_move_point + 9,
                                all_symbols[state_index - first_head_move_point - 3], 'R'))
                    # move to the end of the first tape
                    TM.add_transition(first_head_move_point + 9, TuringMachineTransition(SYMBOL_EMPTY, first_head_move_point + 10, BABAMBABAM, 'L'))
                    # loop left
                    for nondot_symbol in NONDOT_SYMBOLS:
                        TM.add_transition(first_head_move_point + 10, TuringMachineTransition(nondot_symbol, first_head_move_point + 10,
                                nondot_symbol, 'L'))
                    # go past the second dotted symbol
                    for dot_symbol in DOT_SYMBOLS:
                        TM.add_transition(first_head_move_point + 10, TuringMachineTransition(dot_symbol, first_head_move_point + 11,
                                dot_symbol, 'L'))
                    # loop left
                    TM.add_transition(first_head_move_point + 11, TuringMachineTransition(BABAMBABAM, first_head_move_point + 11, BABAMBABAM, 'L'))
                    for nondot_symbol in NONDOT_SYMBOLS:
                        TM.add_transition(first_head_move_point + 11, TuringMachineTransition(nondot_symbol, first_head_move_point + 11,
                                nondot_symbol, 'L'))
                    # pass the dotted empty symbol to the left
                    TM.add_transition(first_head_move_point + 11, TuringMachineTransition(SYMBOL_EMPTY_DOT, first_head_move_point + 12, 
                                SYMBOL_EMPTY_DOT, 'L'))
                # go left, to the common state
                TM.add_transition(first_head_move_point + 12, TuringMachineTransition(BABAMBABAM, common_point_2, BABAMBABAM, 'L'))
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(first_head_move_point + 12, TuringMachineTransition(nondot_symbol, common_point_2, nondot_symbol, 'L'))
                # loop left
                for nondot_symbol in NONDOT_SYMBOLS:
                    TM.add_transition(common_point_2, TuringMachineTransition(nondot_symbol, common_point_2, nondot_symbol, 'L'))
                # go to the final state of this transition
                TM.add_transition(common_point_2, TuringMachineTransition(BABAMBABAM, common_point_2 + 1, BABAMBABAM, 'L'))
                # make a transition to the state that the two-tape machine wanted to transition to
                TM.add_transition(common_point_2 + 1, TuringMachineTransition(BABAMBABAM, STATE_OFFSET + curr_target_state * STATES_PER_STATE,
                            BABAMBABAM, 'L'))
            
        # this will be the accept state
        TM.add_state()

        ################################################################################
        """Return the constructed single-tape turing machine at the end"""
        return TM
    
    def run(self, input_string : str) -> str:
        for symbol in input_string:
            self.tape1.append(symbol)

        curr_state_index = 0
        run_result = ""
        while True:
            if curr_state_index == len(self.state_transitions) - 1:
                run_result += str(len(self.state_transitions) - 1)
                break

            while len(self.tape1) <= self.head1:
                self.tape1.append(SYMBOL_EMPTY)
            while len(self.tape2) <= self.head2:
                self.tape2.append(SYMBOL_EMPTY)
            
            ss_read = self.tape1[self.head1] + self.tape2[self.head2]

            if ss_read not in self.state_transitions[curr_state_index]:
                run_result += "-1"
                break

            trans = self.state_transitions[curr_state_index][ss_read]

            self.tape1[self.head1] = trans[1][0]
            self.tape2[self.head2] = trans[1][1]

            if trans[2][0].upper() == 'L':
                self.head1 = 0 if self.head1 == 0 else self.head1 - 1
            elif trans[2][0].upper() == 'R':
                self.head1 = self.head1 + 1
            
            if trans[2][1].upper() == 'L':
                self.head2 = 0 if self.head2 == 0 else self.head2 - 1
            elif trans[2][1].upper() == 'R':
                self.head2 = self.head2 + 1

            if trans[0] == len(self.state_transitions) - 1:
                run_result += str(len(self.state_transitions) - 1)
                break

            curr_state_index = trans[0]

            run_result += str(curr_state_index) + "\n"
        
        return run_result

    def reset(self):
        self.tape1 = []
        self.tape2 = []
        self.head1 = 0
        self.head2 = 0

    def to_string(self):
        res = ""
        res += str(len(self.state_transitions)) + "\n"
        for i in range(len(self.state_transitions) - 1):
            res += str(len(self.state_transitions[i]))
            for transition_pair in self.state_transitions[i]:
                res += " " + transition_pair[0] + " " + transition_pair[1] + " " + str(self.state_transitions[i][transition_pair][0]) + " " + self.state_transitions[i][transition_pair][1][0] + " " + self.state_transitions[i][transition_pair][1][1] + " " + self.state_transitions[i][transition_pair][2][0] + " " + self.state_transitions[i][transition_pair][2][1]
            res += "\n"
            
        return res
