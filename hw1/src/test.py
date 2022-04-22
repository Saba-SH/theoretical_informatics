from automata import NFA, SYMBOL_ANY, SYMBOL_EPSILON

nfaA = NFA([{"a":set([1])}, []], set([1]))
nfaB = NFA([{"b":set([1])}, []], set([1]))

nfaC = nfaA.union(nfaB).kleene_closure().remove_epsilon()

nfaA = NFA([{"a":set([1])}, []], set([1]))
nfaB = NFA([{"b":set([1])}, []], set([1]))
nfaD = nfaA.union(nfaB).kleene_closure()

print(nfaD.to_string() + "\n")
print(nfaC.to_string() + "\n")

nfaE = nfaC.remove_unreachable()
print(nfaE.to_string() + "\n")
