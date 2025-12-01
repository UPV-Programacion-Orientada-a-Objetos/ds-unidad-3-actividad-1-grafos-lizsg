#include "SparseGraph.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <queue>
#include <set>
#include <iostream>

SparseGraph::SparseGraph() : numNodes(0), numEdges(0) {}

SparseGraph::~SparseGraph() {}

void SparseGraph::loadData(const std::string& filename) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
    std::cout << "[C++ Core] Cargando dataset '" << filename << "'..." << std::endl;

    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error al abrir el archivo: " << filename << std::endl;
        return;
    }

    // Paso 1: Determinar el número de nodos (max ID) y contar aristas
    int maxId = -1;
    int u, v;
    std::string line;
    int edgeCount = 0;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue; // Saltar comentarios
        std::stringstream ss(line);
        if (ss >> u >> v) {
            if (u > maxId) maxId = u;
            if (v > maxId) maxId = v;
            edgeCount++;
        }
    }

    numNodes = maxId + 1;
    numEdges = edgeCount;

    // Inicializar row_ptr con ceros
    // Tamaño es numNodes + 1
    row_ptr.assign(numNodes + 1, 0);

    // Paso 2: Calcular grados (frecuencia de cada nodo origen)
    file.clear();
    file.seekg(0, std::ios::beg);

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        if (ss >> u >> v) {
            row_ptr[u + 1]++;
        }
    }

    // Paso 3: Prefix Sum (Cumulative Sum) para determinar posiciones de inicio
    for (int i = 0; i < numNodes; ++i) {
        row_ptr[i + 1] += row_ptr[i];
    }

    // Paso 4: Llenar col_indices y values
    col_indices.resize(numEdges);
    values.assign(numEdges, 1); // Asumimos peso 1

    // Necesitamos un vector auxiliar para saber dónde insertar en cada fila
    // ya que row_ptr nos da el inicio, pero necesitamos avanzar
    std::vector<int> current_pos = row_ptr;

    file.clear();
    file.seekg(0, std::ios::beg);

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        if (ss >> u >> v) {
            int pos = current_pos[u];
            col_indices[pos] = v;
            current_pos[u]++;
        }
    }

    file.close();
    
    std::cout << "[C++ Core] Carga completa. Nodos: " << numNodes << " | Aristas: " << numEdges << std::endl;
    std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: " << getMemoryUsage() / (1024*1024) << " MB." << std::endl;
}

int SparseGraph::getMaxDegreeNode() {
    int maxDegree = -1;
    int maxNode = -1;

    for (int i = 0; i < numNodes; ++i) {
        // El grado de salida es la diferencia entre punteros de fila consecutivos
        int degree = row_ptr[i+1] - row_ptr[i];
        if (degree > maxDegree) {
            maxDegree = degree;
            maxNode = i;
        }
    }
    return maxNode;
}

std::vector<int> SparseGraph::getNeighbors(int node) {
    std::vector<int> neighbors;
    if (node < 0 || node >= numNodes) return neighbors;

    int start = row_ptr[node];
    int end = row_ptr[node + 1];

    for (int i = start; i < end; ++i) {
        neighbors.push_back(col_indices[i]);
    }
    return neighbors;
}

std::vector<std::pair<int, int>> SparseGraph::bfs(int startNode, int maxDepth) {
    std::cout << "[C++ Core] Ejecutando BFS nativo..." << std::endl;
    std::vector<std::pair<int, int>> resultEdges;
    
    if (startNode < 0 || startNode >= numNodes) return resultEdges;

    std::vector<int> distance(numNodes, -1);
    std::queue<int> q;

    distance[startNode] = 0;
    q.push(startNode);

    int nodesFound = 0;

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        if (distance[u] >= maxDepth) continue;

        int start = row_ptr[u];
        int end = row_ptr[u + 1];

        for (int i = start; i < end; ++i) {
            int v = col_indices[i];
            
            // Añadir arista al resultado (para visualización)
            // Solo añadimos si estamos dentro del rango de profundidad
            resultEdges.push_back({u, v});

            if (distance[v] == -1) {
                distance[v] = distance[u] + 1;
                nodesFound++;
                if (distance[v] < maxDepth) {
                    q.push(v);
                }
            }
        }
    }
    
    std::cout << "[C++ Core] Nodos encontrados: " << nodesFound << std::endl;
    return resultEdges;
}

int SparseGraph::getNodeCount() {
    return numNodes;
}

int SparseGraph::getEdgeCount() {
    return numEdges;
}

long long SparseGraph::getMemoryUsage() {
    long long size = 0;
    size += row_ptr.capacity() * sizeof(int);
    size += col_indices.capacity() * sizeof(int);
    size += values.capacity() * sizeof(int);
    return size;
}
