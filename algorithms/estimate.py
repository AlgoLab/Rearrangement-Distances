from itertools import permutations
from dist import fpt, approx, swap, linkandcut, descendands, fpt2
import networkx as nx
import argparse
from random import choice, random

import timeit


def to_array(t):
    assert nx.is_tree(t)
    tt = [None for _ in range(len(t.nodes))]
        
    for n in t.nodes:
        for k in t.predecessors(n):
            assert type(k) == int
            tt[n] = k
    return tt

def random_tree(n):
    randprufer = nx.random_tree(n)
    randtree = nx.bfs_tree(randprufer, choice(range(n)))
    return to_array(randtree)

def is_valid_linkandcut(t, i, j):
    if i != j and not j in descendands(t, i):
        return True
    return False

def perturbe(t, d):
    tt = t.copy()
    n = len(t)

    for _ in range(d):
        opt = random()
        if opt < 0.5:
            # permutation
            i = choice(range(n))
            j = choice(range(n))
            while i == j:
                i = choice(range(n))
                j = choice(range(n))
            swap(tt, i, j)

        else:
            # link and cut
            i = choice(range(n))
            j = choice(range(n))
            while not is_valid_linkandcut(tt, i, j):
                i = choice(range(n))
                j = choice(range(n))
            linkandcut(tt, i, j)
    return tt

def report(t1, t2, d, k, d_approx, d_fpt, t_approx, t_fpt):
    't1,t2,d,k,approximation,fpt,approximation_time,fpt_time'
    print(f'"{t1}","{t2}",{d},{k},{d_approx},{d_fpt},{t_approx},{t_fpt}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='estimate approx factor.')
    parser.add_argument('-n', type=int, required=True,
                        help='number of mode/labels')
    parser.add_argument('-d', type=int, required=True,
                        help='simulation distance')
    parser.add_argument('-k', type=int, required=True,
                        help='ftp\'s kmax')
    args = parser.parse_args()

    t1 = random_tree(args.n)
    t2 = perturbe(t1, args.d)


    start = timeit.default_timer()
    d_approx = approx(t1, t2)
    stop = timeit.default_timer()
    t_approx = stop - start

    start = timeit.default_timer()
    d_fpt = fpt2(t1, t2, args.k)
    stop = timeit.default_timer()
    t_fpt = stop - start

    # start = timeit.default_timer()
    # d_fpt2 = fpt2(t1, t2, args.k)
    # stop = timeit.default_timer()
    # t_fpt2 = stop - start

    report(t1, t2, args.d, args.k, d_approx, d_fpt, t_approx, t_fpt)
    # print(d_fpt, d_fpt2, t_fpt2)