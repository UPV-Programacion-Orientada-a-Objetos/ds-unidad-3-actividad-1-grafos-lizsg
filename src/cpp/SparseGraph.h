#ifndef SPARSEGRAPH_H
#define SPARSEGRAPH_H

#include "GraphBase.h"
#include <vector>
#include <string>
#include <iostream>

class SparseGraph : public GraphBase {
private:
    // CSR Format
    std::vector<int> values;        // Pesos de las aristas (asumiremos 1)
    std::vector<int> col_indices;   // Índices de columna (destino de la arista)
    std::vector<int> row_ptr;       // Punteros de fila (índice de inicio para cada nodo)
    
    int numNodes;
    int numEdges;

public:
    SparseGraph();
    ~SparseGraph();

    void loadData(const std::string& filename) override;
    std::vector<std::pair<int, int>> bfs(int startNode, int maxDepth) override;
    int getMaxDegreeNode() override;
    std::vector<int> getNeighbors(int node) override;
    int getNodeCount() override;
    int getEdgeCount() override;
    
    // Método auxiliar para depuración
    long long getMemoryUsage();
};

#endif
