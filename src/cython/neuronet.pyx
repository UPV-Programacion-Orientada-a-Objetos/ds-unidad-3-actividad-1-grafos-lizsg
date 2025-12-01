# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string

# Declaración de la clase C++
cdef extern from "../cpp/GraphBase.h":
    cdef cppclass GraphBase:
        pass

cdef extern from "../cpp/SparseGraph.h":
    cdef cppclass SparseGraph(GraphBase):
        SparseGraph() except +
        void loadData(string filename)
        vector[pair[int, int]] bfs(int startNode, int maxDepth)
        int getMaxDegreeNode()
        vector[int] getNeighbors(int node)
        int getNodeCount()
        int getEdgeCount()
        long long getMemoryUsage()

# Clase Wrapper de Python
cdef class NeuroNetEngine:
    cdef SparseGraph* c_graph  # Puntero a la instancia C++

    def __cinit__(self):
        self.c_graph = new SparseGraph()

    def __dealloc__(self):
        del self.c_graph

    def load_data(self, filename: str):
        # Convertir str python a std::string
        cdef string c_filename = filename.encode('utf-8')
        self.c_graph.loadData(c_filename)

    def bfs(self, start_node: int, max_depth: int):
        cdef vector[pair[int, int]] result = self.c_graph.bfs(start_node, max_depth)
        # Convertir vector<pair> a lista de tuplas de Python
        py_result = []
        for i in range(result.size()):
            py_result.append((result[i].first, result[i].second))
        return py_result

    def get_max_degree_node(self):
        return self.c_graph.getMaxDegreeNode()

    def get_neighbors(self, node: int):
        return self.c_graph.getNeighbors(node)

    def get_node_count(self):
        return self.c_graph.getNodeCount()

    def get_edge_count(self):
        return self.c_graph.getEdgeCount()
        
    def get_memory_usage(self):
        return self.c_graph.getMemoryUsage()
