SYMBOL_EMPTY = '_'
# put at the start of the converted machine tape
SYMBOL_BEGIN = ';'
# to separate two tapes of the two-tape turing machine
SYMBOL_SEPARATOR = ':'
# two-tape turing machines will only have 0 and 1 symbols on their tape. dots will mark the two heads
SYMBOL_ZERO_DOT = 'O'
SYMBOL_ONE_DOT = 'I'
SYMBOL_EMPTY_DOT = '^'
# keep a list of possible symbols for convenience
NONDOT_SYMBOLS = ['0', '1', '_']
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
        TM = TuringMachine()
        # add a lot of states
        for i in range(len(self.state_transitions)):
            for j in range(50):
                TM.add_state()

        curr_state_index = 0
        
