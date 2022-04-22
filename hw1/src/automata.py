from bisect import bisect


SYMBOL_ANY = 'A'
SYMBOL_EPSILON = 'E'

class NFA:
    """Constructor"""

    # initializes an NFA with the given states. STATES MUST BE A LIST OF DICT(SYMBOL, SET(INT)) OF TRANSITIONS 
    def __init__(self, states : list, accept_states : set) -> None:
        self.states = states
        self.accept_states = accept_states

    
    """Regular expression operations on NFA. Thompson's algorithm is being used."""
    
    # does a union operation with the other NFA and returns the result. BOTH NFA-S MUST HAVE SINGLE START AND ACCEPT STATES
    def union(self, other : "NFA"):
        new_start = {SYMBOL_EPSILON : {1, len(self.states) + 1}}
        new_accept = {}
        # iterating over the list of states
        for state in self.states:
            # iterating over the symbols for state
            for key_symbol in state:
                new_transitions = set()
                # iterating over the corresponding states for symbol
                for other_state in state[key_symbol]:
                    # incrementing 
                    new_transitions.add(other_state + 1)
                state[key_symbol] = new_transitions
        
        self.states.insert(0, new_start)

        for accept_state in self.accept_states:
            # remove the accept state 
            self.accept_states.remove(accept_state)
            # add an epsilon transition from the former accept state to the new accept state
            self.states[accept_state + 1] = {SYMBOL_EPSILON : {len(self.states) + len(other.states)}}
            break

        # update the list of states for the other NFA
        tmp_incrementer = len(self.states)
        for state in other.states:
            for key_symbol in state:
                new_transitions = set()
                for other_state in state[key_symbol]:
                    new_transitions.add(other_state + tmp_incrementer)
                state[key_symbol] = new_transitions

        # append the list of other NFA states to the current NFA states
        self.states += other.states
        # add a new accept state
        self.states.append(new_accept)
        
        # add epsilon transition from the former accept state of the other NFA to the new accept state
        for other_accept_state in other.accept_states:
            self.states[other_accept_state + tmp_incrementer] = {SYMBOL_EPSILON : {len(self.states) - 1}}

        # add the new accept state
        self.accept_states = set([len(self.states) - 1])

        # return self as the end result
        return self

    # does a Kleene closure and returns the result. NFA MUST HAVE SINGLE START AND ACCEPT STATE
    def kleene_closure(self):
        new_start = {SYMBOL_EPSILON : {1, len(self.states) + 1}}
        new_accept = {}
        # iterating over the list of states
        for state in self.states:
            new_transitions = set()
            # iterating over the symbols for state
            for key_symbol in state:
                # iterating over the corresponding states for symbol
                for other_state in state[key_symbol]:
                    # incrementing 
                    new_transitions.add(other_state + 1)
                state[key_symbol] = new_transitions

        # add the new start state
        self.states.insert(0, new_start)

        # add an epsilon transition from the former accept state to the new accept state
        for accept_state in self.accept_states:
            self.accept_states.remove(accept_state)
            self.states[accept_state + 1] = {SYMBOL_EPSILON : set([1, len(self.states)])}
            break

        # add the new accept state
        self.states.append(new_accept)
        self.accept_states = set([len(self.states) - 1])

        # return self as the end result
        return self

    # does a concatenation operation with the other NFA and returns the result. SINGLE START/ACCEPT
    def concatenation(self, other : "NFA"):
        if len(self.states) == 0:
            return other
        
        if len(other.states) == 0:
            return self

        tmp_incrementer = len(self.states) - 1

        # iterating over the list of states of other NFA
        for other_state in other.states:
            # iterating over the symbols for state
            for key_symbol in other_state:
                new_transitions = set()
                # iterating over the corresponding states for symbol
                for other_other_state in other_state[key_symbol]:
                    # updating the numeration of the states
                    new_transitions.add(other_other_state + tmp_incrementer)
                
                other_state[key_symbol] = new_transitions
        
        # the new accept state will be the accept state of the other NFA
        self.accept_states = set([other.accept_states.pop() + tmp_incrementer])
        
        self.states.pop(len(self.states) - 1)
        self.states += other.states

        # return self as the end result
        return self


    """Operations for optimizing NFA"""
    
    # replaces all epsilon transitions from self and returns the result
    def remove_epsilon(self):
        # strategy can probably be optimized
        # can also be broken down into two methods: 
        # one for determining new accept states and another for getting rid of epsilon transitions
        
        # First part
        # all states that have an epsilon transition to an accept state become accept states themselves
        while True:
            # save the amount of accept states initially
            former_accept_count = len(self.accept_states)

            # iterate over all the states
            for state_index, state in enumerate(self.states):
                # don't waste time iterating if the current state is already an accept one
                if state_index in self.accept_states:
                    continue

                try:
                    # check epsilon transitions
                    for other_state in state[SYMBOL_EPSILON]:
                        # make the current state an accept state if it has an epsilon transition to one
                        if other_state in self.accept_states:
                            self.accept_states.add(state_index)
                            break
                # the state might have no epsilon transitions
                except KeyError:
                    pass

            # if no new accept states were added, break out of the loop
            if len(self.accept_states) == former_accept_count:
                break
        

        # Second part
        # all states having epsilon transitions additionally get the same transitions 
        # as the ones that they have epsilon transitions to
        been = []
        for i in range(len(self.states)):
            been.append(set())

        while True:
            # loop until there is at least one epsilon transition left
            total_epsilon_count = 0
            for state in self.states:
                try:
                    total_epsilon_count += len(state[SYMBOL_EPSILON])
                except:
                    pass
            if total_epsilon_count == 0:
                break

            for state_index, state in enumerate(self.states):
                try:
                    # discard epsilon transition into itself
                    state[SYMBOL_EPSILON].discard(state_index)
                    # copy the initial set of states to which we have epsilon transitions
                    former_epsilon_transitions = set(state[SYMBOL_EPSILON])
                    
                    # note that we've been to these states with epsilon transitions
                    been[state_index].update(former_epsilon_transitions)

                    for other_state in former_epsilon_transitions:
                        # add to the current one all the transitions of the states to which we have epsilons
                        for symbol in self.states[other_state]:
                            try:
                                # only add new epsilon transitions if we haven't had them yet 
                                # otherwise we can have infinite loops
                                if symbol == SYMBOL_EPSILON:
                                    for ep_tr in self.states[other_state][SYMBOL_EPSILON]:
                                        if ep_tr not in been[state_index]:
                                            state[SYMBOL_EPSILON].add(ep_tr)
                                else:
                                    state[symbol].update(self.states[other_state][symbol])

                            except KeyError:
                                state[symbol] = set(self.states[other_state][symbol])

                    # get rid of initial epsilon transitions
                    state[SYMBOL_EPSILON] -= former_epsilon_transitions
                
                # ignore states with no epsilon transitions
                except KeyError:
                    pass

        for state in self.states:
            try:
                # these sets are all empty at this point
                state.pop(SYMBOL_EPSILON)
            except:
                pass

        return self
    
    # removes all the states that are unreachable and returns the result
    def remove_unreachable(self):
        # an iteration might create new unreachable states, so keep looping
        while True:
            # save the initial total amount of states
            n_states = len(self.states)
            # do a single iteration of removing unreachable states
            self = self.__remove_unreachable_helper()
            # break the loop if no states were removed in this iteration
            if len(self.states) == n_states:
                break
            
        return self
    
    # does one iteration removing unreachable states
    def __remove_unreachable_helper(self):
        reachable = set()
        # iterate over all the states to see which ones have at least one state transitioning to them
        for state in self.states:
            for symbol in state:
                for other_state in state[symbol]:
                    reachable.add(other_state)

        unreachable = []
        # iterate over the indices of the states to see which one of them is unreachable
        # skip the start(index 0) state
        for i in range(1, len(self.states)):
            if i not in reachable:
                unreachable.append(i)

        # remove unreachable states from the states of the NFA
        unreachable_set = set(unreachable)
        new_states = []
        for state_index, state in enumerate(self.states):
            if state_index not in unreachable_set:
                new_states.append(state)
        self.states = new_states

        # same thing for accept states
        for unreachable_state in unreachable:
            self.accept_states.discard(unreachable_state)

        # adjust the indices of the states that are left 
        for state in self.states:
            for symbol in state:
                former_transitions = set(state[symbol])
                state[symbol] = set()
                for other_state in former_transitions:
                    state[symbol].add(other_state - bisect(unreachable, other_state))
        
        former_accept_states = set(self.accept_states)
        self.accept_states = set()
        # same thing for accept states
        for accept_state in former_accept_states:
            self.accept_states.add(accept_state - bisect(unreachable, accept_state))

        return self


    """Used for navigating through NFA"""
    
    # returns the set of states reachable from the current state with the given symbol
    def next_states(self, current_state, symbol):
        try:
            return self.states[current_state][symbol]
        except:
            return set()

    """Used for representing NFA"""
    
    # returns a string representation of NFA in the following form:
    # {state count} {accept state count} {total transition count}
    # [accept state indices]
    # for every state:
    #     {count of transitions from this state} [transitions in the form [{symbol} {state}]]
    def to_string(self):
        res = ""
        
        n_states = len(self.states)
        n_accept_states = len(self.accept_states)
        n_transitions = 0
        for state in self.states:
            for symbol in state:
                n_transitions += len(state[symbol])

        res += str(n_states) + " " + str(n_accept_states) + " " + str(n_transitions) + "\n"

        for accept_state in self.accept_states:
            res += str(accept_state) + " "
        
        res += "\n"

        for state in self.states:
            n_curr_transitions = 0
            
            for symbol in state:
                n_curr_transitions += len(state[symbol])

            res += str(n_curr_transitions) + " "

            for symbol in state:
                for other_state in state[symbol]:
                    res += symbol + " " + str(other_state) + " "

            res += "\n"

        return res
