from random import randrange
from src.machine import SYMBOL_EMPTY
PREFIX = "machines/"
reads = [SYMBOL_EMPTY + SYMBOL_EMPTY, SYMBOL_EMPTY + '0', SYMBOL_EMPTY + '1', '0' + SYMBOL_EMPTY, '00', '01',
            '1' + SYMBOL_EMPTY, '10', '11']
directions = ['L', 'R']
chars = [SYMBOL_EMPTY, '0', '1']


def main():
    for i in range(3200):
        f = open(PREFIX + str(i), "w")
        n_states = randrange(1, 64)
        f.write(str(n_states) + "\n")
        
        for j in range(n_states - 1):
            tmp = list(reads)
            n_trans = randrange(0, len(reads))
            if n_trans == 0:
                f.write(str(n_trans) + "\n")
                continue
            chosen = []
            for k in range(n_trans):
                try:
                    ind = randrange(0, len(tmp))
                except Exception:
                    break
                chosen.append(tmp[ind])
                tmp.remove(tmp[ind])
            s = str(n_trans) + " "
            for read in chosen:
                s += read[0] + " " + read[1] + " "
                s += str(randrange(0, n_states)) + " "
                s += chars[randrange(0, len(chars))] + " "
                s += chars[randrange(0, len(chars))] + " "
                s += directions[randrange(0, len(directions))] + " "
                s += directions[randrange(0, len(directions))] + " "
            f.write(s + "\n")
        f.close()
            

if __name__ == "__main__":
    main()
