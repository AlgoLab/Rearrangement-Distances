from statistics import mode
from itertools import permutations, combinations
import networkx as nx
from functools import lru_cache

def direct_children(t, i):
    c = list()
    for ix, j in enumerate(t):
        if j == i:
            c.append(ix)
    return c

def _rec_descends(t, i, d):
    ci = direct_children(t, i)
    if len(ci) == 0:
        return
    else:
        d += ci
        for j in ci:
            _rec_descends(t, j, d)

def descendands(t, i):
    d = list()
    _rec_descends(t, i, d)
    return d
    

def active_set(t1, t2):
    s = list()
    for i, _ in enumerate(t1):
        if t1[i] != t2[i]:
            s.append(i)
    return s

def approx(t1, t2):
    d = 0

    t1 = t1.copy()
    t2 = t2.copy()

    # Step 1
    for ix, _ in enumerate(t1):
        if t1[ix] and t2[ix] and t1[ix] != t2[ix]:
            if t1[t1[ix]]:
                t1[t1[ix]] = None
                d += 1
            if t1[t2[ix]]:
                t1[t2[ix]] = None
                d += 1
                
    # Step 2
    for i, _ in enumerate(t1):
        PP = list()
        for j in direct_children(t2, i):
            if t2[j]:
                PP.append(t2[j])

        if len(PP) != 0:
            x = mode(PP)
            
            for j in direct_children(t1, i):
                if t2[j] != x:
                    t1[j] = None
                    d += 1

    # Step 3
    for i, _ in enumerate(t1):
        PP = list()
        for j in direct_children(t2, i):
            if t1[j]:
                PP.append(t1[j])
        
        if len(PP) != 0:
            x = mode(PP)

            for j in direct_children(t2, i):
                if t1[j] != x:
                    t1[j] = None
                    d += 1

    # Step 4
    for i, _ in enumerate(t1):
        if t1[i] and t2[i] and t1[i] != t2[i]:
            t1[i] = t2[i]
            d += 1

    return d

def swap(tt, i, j):
    if i == j:
        return

    ci = direct_children(tt, i)
    cj = direct_children(tt, j)

    # if p(j) = i => p(i) = j; p(j) = p(i)
    if tt[j] == i:
        tt[j] = tt[i]
        tt[i] = j
    # if p(i) = j => p(i) = p(j); p(j) = i
    elif tt[i] == j:
        tt[i] = tt[j]
        tt[j] = i
    else:
        tt[j], tt[i] = tt[i], tt[j]

    for c in ci:
        if c == j:
            continue
        tt[c] = j
    for c in cj:
        if c == i:
            continue
        tt[c] = i

def apply_permutations(t, p):
    tt = t.copy()
    for op in p:
        swap(tt, op[0], op[1])
    return tt

def linkandcut(tt, i, j):
    if i!= j and not j in descendands(tt, i):
        tt[i] = j

def apply_linkandcut(t, op):
    tt = t.copy()
    for o in op:
        linkandcut(tt, *o)
        # tt[o[0]] = tt[o[1]]
    return tt

def ftp(t1, t2, kmax=4, max_iter=0):
    t1 = t1.copy()

    tot_iter = 0
    
    for k in range(2, kmax + 1):
        for k1 in range(0, k + 1):
            # permutations
            k1_search = range(len(t1))
            for p in permutations(combinations(k1_search, 2), k1):
                # print(p)
                tstar = apply_permutations(t1, p)
                if tstar == t2:
                    return k1

                tot_iter+=1
                if max_iter > 0 and tot_iter >= max_iter:
                    return -k1

                if k1 == k:
                    continue

                for k2 in range(1, (k - k1) + 1):
                    k2_search = range(len(tstar))
                    for seq in permutations(permutations(k2_search, 2), k2):
                        tstar2 = apply_linkandcut(tstar, seq)
                        if tstar2 == t2:
                            return k1 + k2
                        tot_iter+=1

                        if max_iter > 0 and tot_iter >= max_iter:
                            return -(k1 + k2)

    print(f'tot {tot_iter}')

@lru_cache()
def to_nx(t):
    g = nx.DiGraph()
    for i in range(len(t)):
        if t[i] != None:
            g.add_edge(t[i], i)

    return g

@lru_cache()
def is_isomorphic(t1, t2):
    tt1 = to_nx(t1)
    tt2 = to_nx(t2)

    return nx.is_isomorphic(tt1, tt2)


def ftp_iso(t1, t2, kmax, max_iter=0):
    t1 = t1.copy()
    tt2 = tuple(t2)

    tot_iter = 0
    
    for k in range(2, kmax + 1):
        for k1 in range(1, k + 1):
            # permutations
            k1_search = range(len(t1))
            for p in permutations(permutations(k1_search, 2), k1):
                # print(p)
                tstar = apply_linkandcut(t1, p)
                if tstar == t2:
                    return k1

                tot_iter+=1
                if max_iter > 0 and tot_iter >= max_iter:
                    return -k1

                if k1 == k:
                    continue

                if not is_isomorphic(tt2, tuple(tstar)):
                    continue

                for k2 in range(1, (k - k1) + 1):
                    k2_search = range(len(tstar))
                    for seq in permutations(combinations(k2_search, 2), k2):
                        tstar2 = apply_permutations(tstar, seq)
                        if tstar2 == t2:
                            return k1 + k2
                        tot_iter+=1

                        if max_iter > 0 and tot_iter >= max_iter:
                            return -(k1 + k2)

    print(f'tot {tot_iter}')


# tt = T1.copy()
# print(tt)
# print(swap(tt, 3,4))
# print(tt)
# print(swap(tt, 3,5))
# print(tt)

# print(tt, T3==tt)
# tstar = apply_linkandcut(tt,((5,1),))
# print(tstar, T4==tstar)

# tg1 = to_nx(T1)
# tg2=to_nx(T3)

# print(nx.is_isomorphic(tg1,tg2))

if __name__ == "__main__":
    T1 = [None,0,0,2,2,1,3,3,3,4]
    T2 = [6,0,None,2,2,0,4,4,3,7]

    T3 = [None,0,0,1,2,2,4,4,4,5]
    T4 = [None,0,0,1,2,1,4,4,4,5]

    t1 = [8, 5, 7, None, 0, 3, 4, 4, 1, 1]
    t2 = [8, 5, 7, None, 0, 3, 2, 4, 1, 1]

    import sys


    # print(active_set(T1, T3))
    # print(approx(T1, T2))
    # print(ftp_iso(T1, T2, kmax=int(sys.argv[1]), max_iter=0))
    print(approx(t1,t2))
    print(ftp(t1,t2, int(sys.argv[1])))