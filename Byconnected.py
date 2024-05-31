import random
import time
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, virsunes):
        self.virsunes = virsunes
        self.graph = defaultdict(list)
        self.laikas = 0

    def prideti_briauna(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def rasti_dvigubai_komponentes_ir_artikuliacijos_taskis(self):
        atradimo_laikas = [-1] * self.virsunes
        mazas = [-1] * self.virsunes
        tevas = [-1] * self.virsunes
        bcc_stackas = []
        bcc = []
        articuliacijos_taskas = set()

        def dfs_bcc(start):
            stack = [(start, iter(self.graph[start]))]
            atradimo_laikas[start] = mazas[start] = self.laikas
            self.laikas += 1
            vaikai = 0
            while stack:
                u, neighbors = stack[-1]
                try:
                    v = next(neighbors)
                    if atradimo_laikas[v] == -1:  # jei v dar neaplankyta
                        tevas[v] = u
                        vaikai += 1
                        atradimo_laikas[v] = mazas[v] = self.laikas
                        self.laikas += 1
                        bcc_stackas.append((u, v))
                        stack.append((v, iter(self.graph[v])))
                    elif v != tevas[u]:  # pakeiciam mazao reiksmia u tevo funkcijoms.
                        mazas[u] = min(mazas[u], atradimo_laikas[v])
                        if atradimo_laikas[v] < atradimo_laikas[u]:
                            bcc_stackas.append((u, v))
                except StopIteration:
                    stack.pop()
                    if tevas[u] != -1:
                        mazas[tevas[u]] = min(mazas[tevas[u]], mazas[u])
                        if mazas[u] >= atradimo_laikas[tevas[u]]:
                            articuliacijos_taskas.add(tevas[u])
                            komponente = set()
                            while bcc_stackas and bcc_stackas[-1] != (tevas[u], u):
                                edge = bcc_stackas.pop()
                                komponente.update(edge)
                            if bcc_stackas:
                                edge = bcc_stackas.pop()
                                komponente.update(edge)
                            if len(komponente) > 0:
                                bcc.append(komponente)
                    elif tevas[u] == -1 and vaikai > 1:
                        articuliacijos_taskas.add(u)
                        komponente = set()
                        while bcc_stackas:
                            edge = bcc_stackas.pop()
                            komponente.update(edge)
                        if len(komponente) > 0:
                            bcc.append(komponente)

        start_time = time.time()  # Start the timer
        for pradine_virsune in range(self.virsunes):
            if atradimo_laikas[pradine_virsune] == -1 and self.graph[pradine_virsune]:  # pradeti DFS virsunem kurios turi kraštine
                dfs_bcc(pradine_virsune)
                # Jeigu dar yra likusiu kraštiniu stecke reiskiasi jos irgi yra antskira jungi komponente
                if bcc_stackas:
                    komponente = set()
                    while bcc_stackas:
                        edge = bcc_stackas.pop()
                        komponente.update(edge)
                    if len(komponente) > 0:
                        bcc.append(komponente)
        end_time = time.time()  # End the timer

        print(f"Algoritmo veikimo laikas: {end_time - start_time:.6f} sekundes")

        return bcc, list(articuliacijos_taskas)

    @staticmethod
    def sugeneruoti_atsitiktini_grafa(num_virsunes, num_krastines):
        g = Graph(num_virsunes)
        krastines = set()

        while len(krastines) < num_krastines:
            u = random.randint(0, num_virsunes - 1)
            v = random.randint(0, num_virsunes - 1)
            if u != v and (u, v) not in krastines and (v, u) not in krastines:
                g.prideti_briauna(u, v)
                krastines.add((u, v))

        return g

    @staticmethod
    def draw_graph(graph):
        G = nx.Graph()
        for u in range(graph.virsunes):
            for v in graph.graph[u]:
                if u < v:
                    G.add_edge(u, v)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=15)
        plt.show()


# Example usage:
if __name__ == "__main__":
    specifinis_graphas = Graph.sugeneruoti_atsitiktini_grafa(1000000, 5000000)

    #print("Specifinio grafo kraštinės:")
    #for u in range(specifinis_graphas.virsunes):
    #    for v in specifinis_graphas.graph[u]:
    #       if u < v:
    #            print(f"({u}, {v})")

    bcc, articuliacijos_taskas = specifinis_graphas.rasti_dvigubai_komponentes_ir_artikuliacijos_taskis()
    #print("Artikuliacijos taškai:", articuliacijos_taskas)
    #print("Dvigubai sujungtos komponentės (viršūnės):")
    #for komponente in bcc:
    #   print(komponente)

    #Graph.draw_graph(specifinis_graphas)
