import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Añadir el directorio raíz al path para importar el módulo compilado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

try:
    import neuronet
except ImportError:
    messagebox.showerror("Error", "No se pudo importar el módulo 'neuronet'. Asegúrate de haber compilado la extensión con 'python setup.py build_ext --inplace'.")
    sys.exit(1)

class NeuroNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet: Análisis de Redes Masivas")
        self.root.geometry("1000x700")

        self.engine = neuronet.NeuroNetEngine()
        self.graph_loaded = False

        # --- Panel de Control (Izquierda) ---
        self.control_panel = tk.Frame(root, width=300, bg="#f0f0f0", padx=10, pady=10)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Título
        tk.Label(self.control_panel, text="NeuroNet Control", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        # Carga de Datos
        tk.Label(self.control_panel, text="1. Ingesta de Datos", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(10, 5))
        self.btn_load = tk.Button(self.control_panel, text="Cargar Dataset (SNAP)", command=self.load_dataset, bg="#4CAF50", fg="white")
        self.btn_load.pack(fill=tk.X, pady=5)
        self.lbl_file = tk.Label(self.control_panel, text="Ningún archivo cargado", bg="#f0f0f0", fg="gray", wraplength=280)
        self.lbl_file.pack(pady=5)

        # Métricas
        tk.Label(self.control_panel, text="Métricas del Grafo", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(20, 5))
        self.lbl_nodes = tk.Label(self.control_panel, text="Nodos: -", bg="#f0f0f0")
        self.lbl_nodes.pack(anchor="w")
        self.lbl_edges = tk.Label(self.control_panel, text="Aristas: -", bg="#f0f0f0")
        self.lbl_edges.pack(anchor="w")
        self.lbl_memory = tk.Label(self.control_panel, text="Memoria (Est): - MB", bg="#f0f0f0")
        self.lbl_memory.pack(anchor="w")
        
        # Análisis Topológico
        tk.Label(self.control_panel, text="2. Análisis Topológico", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(20, 5))
        self.btn_max_degree = tk.Button(self.control_panel, text="Identificar Nodo Crítico", command=self.find_critical_node, state=tk.DISABLED)
        self.btn_max_degree.pack(fill=tk.X, pady=5)
        self.lbl_critical = tk.Label(self.control_panel, text="Nodo Crítico: -", bg="#f0f0f0", fg="blue")
        self.lbl_critical.pack(pady=5)

        # Simulación BFS
        tk.Label(self.control_panel, text="3. Simulación BFS", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(20, 5))
        
        frame_bfs = tk.Frame(self.control_panel, bg="#f0f0f0")
        frame_bfs.pack(fill=tk.X)
        
        tk.Label(frame_bfs, text="Nodo Inicio:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        self.entry_start = tk.Entry(frame_bfs, width=10)
        self.entry_start.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_bfs, text="Profundidad:", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
        self.entry_depth = tk.Entry(frame_bfs, width=10)
        self.entry_depth.grid(row=1, column=1, padx=5)
        self.entry_depth.insert(0, "2")

        self.btn_bfs = tk.Button(self.control_panel, text="Ejecutar BFS y Visualizar", command=self.run_bfs, state=tk.DISABLED, bg="#2196F3", fg="white")
        self.btn_bfs.pack(fill=tk.X, pady=10)

        # --- Área de Visualización (Derecha) ---
        self.viz_panel = tk.Frame(root, bg="white")
        self.viz_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.figure = plt.Figure(figsize=(6, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Visualización de Subgrafo")
        self.ax.axis('off')
        
        self.canvas = FigureCanvasTkAgg(self.figure, self.viz_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_dataset(self):
        initial_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return

        try:
            self.lbl_file.config(text=f"Cargando: {os.path.basename(file_path)}...")
            self.root.update()
            
            self.engine.load_data(file_path)
            
            nodes = self.engine.get_node_count()
            edges = self.engine.get_edge_count()
            mem = self.engine.get_memory_usage() / (1024 * 1024)
            
            self.lbl_nodes.config(text=f"Nodos: {nodes:,}")
            self.lbl_edges.config(text=f"Aristas: {edges:,}")
            self.lbl_memory.config(text=f"Memoria (Est): {mem:.2f} MB")
            self.lbl_file.config(text=os.path.basename(file_path))
            
            self.graph_loaded = True
            self.btn_max_degree.config(state=tk.NORMAL)
            self.btn_bfs.config(state=tk.NORMAL)
            
            messagebox.showinfo("Éxito", "Dataset cargado correctamente en estructura CSR.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar dataset: {str(e)}")

    def find_critical_node(self):
        if not self.graph_loaded:
            return
        
        node = self.engine.get_max_degree_node()
        self.lbl_critical.config(text=f"Nodo Crítico (Mayor Grado): {node}")

    def run_bfs(self):
        if not self.graph_loaded:
            return
            
        try:
            start_node = int(self.entry_start.get())
            depth = int(self.entry_depth.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos para Nodo y Profundidad.")
            return

        # Ejecutar BFS en C++
        edges = self.engine.bfs(start_node, depth)
        
        if not edges:
            messagebox.showinfo("Info", "No se encontraron nodos o el nodo de inicio no existe.")
            return

        # Visualizar con NetworkX
        self.ax.clear()
        G = nx.DiGraph()
        G.add_edges_from(edges)
        
        pos = nx.spring_layout(G, seed=42)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_size=300, node_color='lightblue')
        # Dibujar nodo inicio diferente
        if start_node in G:
            nx.draw_networkx_nodes(G, pos, ax=self.ax, nodelist=[start_node], node_size=500, node_color='red')
            
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, ax=self.ax, arrows=True, edge_color='gray')
        # Etiquetas
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=8)
        
        self.ax.set_title(f"Resultado BFS: Nodo {start_node}, Profundidad {depth} ({len(G.nodes)} nodos)")
        self.ax.axis('off')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetApp(root)
    root.mainloop()
