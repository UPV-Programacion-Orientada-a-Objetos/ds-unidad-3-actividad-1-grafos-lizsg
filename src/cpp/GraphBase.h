#ifndef GRAPHBASE_H
#define GRAPHBASE_H

#include <vector>
#include <string>
#include <utility>

class GraphBase {
public:
    virtual ~GraphBase() {}
    
    // Carga los datos desde un archivo de texto (Edge List)
    virtual void loadData(const std::string& filename) = 0;
    
    // Ejecuta BFS desde un nodo inicio hasta una profundidad máxima
    // Retorna pares de (origen, destino) de las aristas visitadas para visualización
    virtual std::vector<std::pair<int, int>> bfs(int startNode, int maxDepth) = 0;
    
    // Retorna el ID del nodo con mayor grado
    virtual int getMaxDegreeNode() = 0;
    
    // Obtiene los vecinos de un nodo
    virtual std::vector<int> getNeighbors(int node) = 0;
    
    // Métricas básicas
    virtual int getNodeCount() = 0;
    virtual int getEdgeCount() = 0;
};

#endif
