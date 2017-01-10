import os
import networkx as nx

def read_metis(DATA_FILENAME):

    G = nx.Graph()

    # add node weights from METIS file
    with open(DATA_FILENAME, "r") as metis:

        n = 0
        first_line = None
        has_edge_weights = False
        has_node_weights = False
        for i, line in enumerate(metis):
            if line[0] == '%':
                # ignore comments
                continue

            if not first_line:
                # read meta data from first line
                first_line = line.split()
                m_nodes = int(first_line[0])
                m_edges = int(first_line[1])
                if len(first_line) > 2:
                    # FMT has the following meanings:
                    #  0  the graph has no weights (in this case, you can omit FMT)
                    #  1  the graph has edge weights
                    # 10  the graph has node weights
                    # 11  the graph has both edge and node weights
                    file_format = first_line[2]
                    if int(file_format) == 0:
                        pass
                    elif int(file_format) == 1:
                        has_edge_weights = True
                    elif int(file_format) == 10:
                        has_node_weights = True
                    elif int(file_format) == 11:
                        has_edge_weights = True
                        has_node_weights = True
                    else:
                        assert False, "File format not supported"
                continue

            # METIS starts node count from 1, here we start from 0 by
            # subtracting 1 in the edge list and incrementing 'n' after
            # processing the line.
            if line.strip():
                e = line.split()
                if len(e) > 2:
                    # create weighted edge list:
                    #  [(1, 2, {'weight':'2'}), (1, 3, {'weight':'8'})]
                    edges_split = list(zip(*[iter(e[1:])] * 2))
                    edge_list = [(n, int(v[0]) - 1, {'weight': int(v[1])}) for v in edges_split]

                    G.add_edges_from(edge_list)
                    G.node[n]['weight'] = int(e[0])
                else:
                    # no edges
                    G.add_nodes_from([n], weight=int(e[0]))
            else:
                # blank line indicates no node weight
                G.add_nodes_from([n], weight=int(0))
            n += 1

    # sanity check
    assert (m_nodes == G.number_of_nodes())
    assert (m_edges == G.number_of_edges())

    return G


