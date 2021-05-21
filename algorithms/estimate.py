from dist import ftp, approx
import networkx as nx
import argparse
import matplotlib.pyplot as plt


def to_array(t):
    tt = list()
    td = nx.DiGraph([(u,v) for (u,v) in t.edges if u<v])
    nx.draw(td)
    plt.show()
    # for n in t.nodes:
    #     print(n)
    #     for k in t.predecessors(n):
    #         print(k, t.predecessors(n)[k])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='estimate approx factor.')
    parser.add_argument('-n', type=int, required=True,
                        help='number of mode/labels')
    parser.add_argument('-d', type=int, required=True,
                        help='simulation distance')
    parser.add_argument('-k', type=int, required=True,
                        help='ftp\'s kmax')
    args = parser.parse_args()


    randtree = nx.random_tree(args.n)
    s = nx.topological_sort(randtree)
    print(s[0])
    tree = nx.bfs_tree(randtree, 0)
    nx.draw(tree)
    plt.show()
    print(randtree.edges)
    to_array(randtree)