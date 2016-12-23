
import numpy as np
from ctypes import cdll, POINTER, c_int, c_double, c_void_p

import networkit
import networkx as nx

class GraphStructureException(Exception):
    """When SCOTCH_graphBuild() returns 1 if the graph structure has not been successfully set with all of the input data."""

def load_graph(path):
    print("Loading graph data...")
    nkG = networkit.graphio.METISGraphReader().read(path)

    # convert to networkx Graph
    G = networkit.nxadapter.nk2nx(nkG)

    # add node weights from METIS file
    with open(path, "r") as metis:

        # read meta data from first line
        first_line = next(metis).split()
        m_nodes = int(first_line[0])
        m_edges = int(first_line[1])

        for i, line in enumerate(metis):
            if line.strip():
                weight = line.split()[0]
                G.add_nodes_from([i], weight=str(weight))
            else:
                # blank line indicates no node weight
                G.add_nodes_from([i], weight=0.0)

    return G


class libScotch(object):
    def __init__(self):
        self.graph = None

        lib = cdll.LoadLibrary('/usr/local/lib/libscotch.so')

        self.SCOTCH_Arch = c_double*128
        self.SCOTCH_Graph = c_double*128
        self.SCOTCH_Strat = c_double*128

        # SCOTCH_version
        self.SCOTCH_version = lib.SCOTCH_version
        self.SCOTCH_version.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]

        # SCOTCH_archInit
        self.SCOTCH_archInit = lib.SCOTCH_archInit
        self.SCOTCH_archInit.argtypes = [POINTER(self.SCOTCH_Arch)]

        # SCOTCH_archExit
        self.SCOTCH_archExit = lib.SCOTCH_archExit
        self.SCOTCH_archExit.argtypes = [POINTER(self.SCOTCH_Arch)]

        # SCOTCH_graphInit
        self.SCOTCH_graphInit = lib.SCOTCH_graphInit
        self.SCOTCH_graphInit.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphExit
        self.SCOTCH_graphExit = lib.SCOTCH_graphExit
        self.SCOTCH_graphExit.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphBuild
        self.SCOTCH_graphBuild = lib.SCOTCH_graphBuild
        self.SCOTCH_graphBuild.argtypes = [
            POINTER(self.SCOTCH_Graph), c_int, c_int,
            c_void_p, c_void_p, c_void_p, c_void_p,
            c_int, c_void_p, c_void_p
        ]

    def _create_adjacency_list(self, nxG):
        adjacency_start = [0]
        adjacency_list = []
        for n,nbrdict in G.adjacency_iter():
            edges = list(nbrdict.keys())
            adjacency_start += [adjacency_start[-1] + len(edges)]
            adjacency_list += edges

        # Since edges are represented by both of their ends,
        # the number of edge data in the graph is twice the
        # number of graph edges.
        assert (len(adjacency_list) == G.number_of_edges()*2)

        return (adjacency_start, adjacency_list)

    def _cleanup(self):
        #if any(v != 0.0 for v in self.arch):
        #    self.SCOTCH_archExit(arch)

        if any(v != 0.0 for v in self.graph):
            self.SCOTCH_graphExit(self.graph)

        #if any(v != 0.0 for v in self.strat):
        #    self.SCOTCH_stratExit(strat)


    def version(self):
        versptr = c_int(0)
        relaptr = c_int(0)
        patcptr = c_int(0)
        ret = self.SCOTCH_version(versptr, relaptr, patcptr)
        return "{}.{}.{}".format(versptr.value, relaptr.value, patcptr.value)

    def networkx_to_scotch_graph(self, nxG):

        if self.graph:
            self._cleanup()

        # Initialise
        self.graph = self.SCOTCH_Graph()
        self.SCOTCH_graphInit(self.graph)

        adjacency_start, adjacency_list = self._create_adjacency_list(nxG)

        baseval = 0
        vertnbr = nxG.number_of_nodes()
        verttab = np.asanyarray(adjacency_start, dtype=np.int32)
        velotab = None # array of node weights
        edgenbr = len(adjacency_list)
        edgetab = np.asanyarray(adjacency_list, dtype=np.int32)
        edlotab = None # array of edge weights

        #     SCOTCH_graphBuild(grafh, baseval, vertnbr, verttab, vendtab, velotab, vlbltab, edgenbr, edgetab, edlotab)
        rt = self.SCOTCH_graphBuild(self.graph, baseval, vertnbr, verttab.ctypes, None, velotab, None, edgenbr, edgetab.ctypes, edlotab)
        if rt != 0:
            raise GraphStructureException("Failed to set graph structure")

        return self.graph




f = libScotch()
print(f.version())

G = load_graph("/home/sami/py-graph/data/oneshot_fennel_weights.txt")
scotch_graph = f.networkx_to_scotch_graph(G)

print(scotch_graph)
