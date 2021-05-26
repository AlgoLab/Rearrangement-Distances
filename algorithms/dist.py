from statistics import mode
from itertools import permutations, combinations, chain
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

def apply_permutations_seq(t, p):
    tt = t.copy()
    for ix, _ in enumerate(p):
        jx = (ix + 1) % len(p)
        i = p[ix]
        j = p[jx]
        # tt[i] = t[j]
        # tt[j] = t[i]
        # print(i,j)
        # for c in direct_children(t, i):
        #     tt[c] = j
        # for c in direct_children(t, j):
        #     tt[c] = i
        swap(tt, i, j)
        if jx == len(p) - 1:
            break
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

def fpt(t1, t2, kmax=4, max_iter=0):
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
    return -1

def calc_pseq_w(p):
    s = set(chain(*p))
    return len(s)

def fpt2(t1, t2, kmax, quick_return=False):
    t1 = t1.copy()

    min_dist = kmax**2
    
    for k in range(2, kmax + 1):
        for k1 in range(0, k + 1):
            if k1 >= min_dist:
                return min_dist
            # permutations
            k1_search = range(len(t1))
            for p in permutations(combinations(k1_search, 2), k1):
                tstar = apply_permutations(t1, p)
                if tstar == t2:
                    return k1

                opt_seq = len(active_set(tstar, t2))
                if opt_seq <= k - k1 and opt_seq + k1 < min_dist:
                    min_dist = opt_seq + k1
                    # print('up', p, opt_seq)
                    if quick_return:
                        return min_dist
                    

                if k1 == k:
                    continue

    return min_dist

def fpt2w(t1, t2, kmax, quick_return=False):
    t1 = t1.copy()
    min_dist = kmax**2
    
    for k in range(2, kmax + 1):
        for k1 in range(0, k + 1):
            if k1 >= min_dist:
                return min_dist
            # permutations
            k1_search = range(len(t1))
            for p in permutations(combinations(k1_search, 2), k1):
                tstar = apply_permutations(t1, p)
                pw = calc_pseq_w(p)
                if tstar == t2:
                    return pw

                opt_seq = len(active_set(tstar, t2))
                if opt_seq <= k - pw and opt_seq + pw < min_dist:
                    min_dist = opt_seq + pw
                    # print('up', p, opt_seq)
                    if quick_return:
                        return min_dist
                    

                if k1 == k:
                    continue

    return min_dist

# Change approach to permutations
def fptP(t1, t2, kmax, quick_return=False):
    t1 = t1.copy()
    min_dist = kmax**2
    
    for k in range(2, kmax + 1):
        # check for k1=0 -> lac only
        opt_seq = len(active_set(t1, t2))
        if opt_seq <= k and opt_seq < min_dist:
            min_dist = opt_seq

        # p starts from 2 and do it in permutations sense
        for k1 in range(2, k + 1):
            if k1 >= min_dist:
                return min_dist
            # permutations
            k1_search = range(len(t1))
            for p in permutations(k1_search, k1):
                tstar = apply_permutations_seq(t1, p)
                if tstar == t2:
                    return k1

                opt_seq = len(active_set(tstar, t2))
                if opt_seq <= k - k1 and opt_seq + k1 < min_dist:
                    # print('up', k1, opt_seq, p)
                    min_dist = opt_seq + k1
                    if quick_return:
                        return min_dist

                if k1 == k:
                    continue
    return min_dist

def to_nx(t):
    g = nx.DiGraph()
    for i in range(len(t)):
        if t[i] != None:
            g.add_edge(t[i], i)

    return g

def is_isomorphic(t1, t2):
    tt1 = to_nx(t1)
    tt2 = to_nx(t2)

    return nx.is_isomorphic(tt1, tt2)


def fpt_iso(t1, t2, kmax, max_iter=0):
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

    t1 = [8, 7, 6, 9, 2, 4, 9, None, 2, 1]
    t2 = [5, 7, 0, 5, 2, 1, 8, None, 2, 8]

    import sys

    # from matplotlib import pyplot as plt
    # pos=nx.nx_agraph.graphviz_layout(to_nx(tuple(t1)),prog='dot')
    # nx.draw(to_nx(tuple(t1)), pos=pos, with_labels=True)
    # plt.show()
    # pos=nx.nx_agraph.graphviz_layout(to_nx(tuple(t2)),prog='dot')
    # nx.draw(to_nx(tuple(t2)), pos=pos, with_labels=True)
    # plt.show()


    # print(active_set(T1, T3))
    # print(approx(T1, T2))
    # print(ftp_iso(T1, T2, kmax=int(sys.argv[1]), max_iter=0))
    # print(approx(t1,t2))
    # print(fpt2w(t1,t2, int(sys.argv[1])))
    # print(fptP(t1,t2, int(sys.argv[1])))

    # print(apply_permutations(t1, ((8,9),)))
    print(t1)
    tt = apply_permutations_seq(t1, (8,4,3,5))
    # tt = apply_permutations_seq(tt, (4,3))
    # tt = apply_permutations_seq(tt, (3,5))
    # tt = apply_permutations(t1, ((8,4),(4,3),(3,5)))
    # print(tt)
    # pos=nx.nx_agraph.graphviz_layout(to_nx(tt),prog='dot')
    # nx.draw(to_nx(tt), pos=pos, with_labels=True)
    # plt.show()