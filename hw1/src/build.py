from curses.ascii import isalnum
from automata import NFA, SYMBOL_EPSILON, SYMBOL_ANY

# check if the given expression is a single character of the expression/NFA alphabet
def is_unit(exp):
    if len(exp) == 1 and exp.__class__.__name__ == "str" and isalnum(exp):
        return True
    
    return False


# construct and return an NFA matching the given regular expression
# NFA returned by this function may be unoptimized
def construct(regex : str) -> NFA:
    # base case: when the given expression is a single symbol
    if is_unit(regex):
        # 0 is start state, 1 is accept state.
        # args: ([dict with the given symbol mapping to just 1, empty dict], set of just 1(accept state))
        return NFA([{regex:set([1])}, {}], set([1]))
    else:
        # convert regex to a list
        regex = list(regex)
        # construct an NFA for all single letters
        for index, c in enumerate(regex):
            # this means that this is a recursive call and we've gone through this loop already
            if c.__class__.__name__ == "NFA":
                break
            
            if is_unit(c):
                regex[index] = construct(c)

        # recursively evaluate anything that's in brackets
        while True:
            try:
                bracket_index = regex.index('(')
            except:
                break
            
            open_bracket_count = 0
            for i in range(bracket_index + 1, len(regex)):
                if regex[i].__class__.__name__ == "str": 
                    if regex[i] == ')':
                        if open_bracket_count == 0:
                            close_bracket_index = i
                            break
                        else:
                            open_bracket_count -= 1
                    elif regex[i] == '(':
                        open_bracket_count += 1

            in_bracket_ex = regex[bracket_index + 1 : close_bracket_index]
            nfa_for_in_bracket = construct(in_bracket_ex)

            new_regex = regex[:bracket_index]
            new_regex.append(nfa_for_in_bracket)
            new_regex += regex[close_bracket_index + 1:]

            regex = list(new_regex)

        # take care of kleene closure operations
        pos = 0
        while True:
            try:
                pos = regex.index('*', pos)
            except:
                break

            new_regex = regex[:pos - 1]
            new_regex.append(regex[pos - 1].kleene_closure())
            new_regex += regex[pos + 1:]

            regex = new_regex

        # take care of concatenation operations
        pos = 0
        while True:
            try:
                if regex[pos + 1] == '|':
                    pos += 2
                    continue

                new_regex = regex[:pos]
                new_regex.append(regex[pos].concatenation(regex[pos + 1]))
                new_regex += regex[pos + 2:]

                regex = new_regex

            except IndexError:
                break

        # take care of union operations
        for i in range(2, len(regex), 2):
            regex[0] = regex[0].union(regex[i])

        res = regex[0]
        
        return res

def main():
    regex = input()
    nfa = construct(regex).remove_epsilon().remove_unreachable()
    print(nfa.to_string())

if __name__ == "__main__":
    main()
