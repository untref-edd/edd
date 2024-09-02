from __future__ import annotations

from importlib.util import find_spec


class Vertice:
    def __init__(self, _id: str) -> None:
        self._id = _id
        self._aristas: dict[Arista, Arista] = {}
        self._grado_entrada = 0

    @property
    def id(self) -> str:
        return self._id

    @property
    def aristas(self) -> set[Arista]:
        return set(self._aristas.values())

    @property
    def grado_entrada(self) -> int:
        return self._grado_entrada

    @property
    def adyacentes(self) -> set[Vertice]:
        return {arista.destino for arista in self.aristas}

    def agregar_arista(self, arista: Arista) -> None:
        arista = self._aristas.setdefault(arista, arista)
        arista.destino._grado_entrada += 1

    def __eq__(self, other: Vertice) -> bool:
        if not isinstance(other, Vertice):
            return False

        return self._id == other._id

    def __hash__(self):
        return hash((self._id,))

    def __repr__(self) -> str:
        return f"Vertice({repr(self._id)})"

    def __lt__(self, other: Vertice) -> bool:
        """
        Se implementa para poder comparar vértices en un heap.
        """
        return False


class Arista:
    def __init__(self, origen: Vertice, destino: Vertice, peso: int | float = None) -> None:
        self._origen = origen
        self._destino = destino
        self._peso = peso

    @property
    def vertices(self) -> Vertice:
        return (self._origen, self._destino)

    @property
    def origen(self) -> Vertice:
        return self._origen

    @property
    def destino(self) -> Vertice:
        return self._destino

    @property
    def peso(self) -> int | float | None:
        return self._peso

    def __contains__(self, vertice: Vertice) -> bool:
        return vertice in self.vertices

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Arista):
            return False

        return (self._origen, self._destino, self._peso) == (other._origen, other._destino, other._peso)

    def __hash__(self):
        return hash((self._origen, self._destino, self._peso))

    def __repr__(self) -> str:
        return f"Arista({repr(self.destino)}, {repr(self.destino)}, {repr(self.peso)})"


class Grafo:
    def __init__(self):
        self._vertices: dict[Vertice, Vertice] = {}
        self._aristas: dict[Arista, Arista] = {}
        self._dirigido: bool = False
        self._ponderado: bool = False

    @property
    def vertices(self) -> set[Vertice]:
        return set(self._vertices.values())

    @property
    def aristas(self) -> set[Arista]:
        return set(self._aristas.values())

    @property
    def dirigido(self) -> bool:
        return self._dirigido

    @property
    def ponderado(self) -> bool:
        return self._ponderado

    def agregar_arista(self, origen: str, destino: str, peso: int | float = None) -> None:
        vertice_origen = Vertice(origen)
        vertice_destino = Vertice(destino)

        vertice_origen = self._vertices.setdefault(vertice_origen, vertice_origen)
        vertice_destino = self._vertices.setdefault(vertice_destino, vertice_destino)

        self.__agregar_arista(vertice_origen, vertice_destino, peso)

        if not self._dirigido:
            self.__agregar_arista(vertice_destino, vertice_origen, peso)

        if peso is not None:
            self._ponderado = True

    def __agregar_arista(self, vertice_origen: str, vertice_destino: str, peso: int | float = None) -> None:
        arista = Arista(vertice_origen, vertice_destino, peso)
        arista = self._aristas.setdefault(arista, arista)
        vertice_origen.agregar_arista(arista)

    def __getitem__(self, id: str) -> Vertice:
        return self._vertices.get(Vertice(id))

    def __str__(self) -> str:
        out = f"Vertices: { {v.id for v in self.vertices} }\n\n"
        arrow_head = ">" if self._dirigido else ""
        for vertice in self.vertices:
            for arista in vertice.aristas:
                if arista.peso is not None:
                    out += f"\t{vertice.id} --{arista.peso}--{arrow_head} {arista.destino.id}\n"
                else:
                    out += f"\t{vertice.id} --{arrow_head} {arista.destino.id}\n"

        return out

    def to_networkx(self):
        if find_spec("networkx") is None:
            print("networkx no instalado")
            return None

        import networkx as nx

        G = nx.DiGraph() if self._dirigido else nx.Graph()

        for vertice_origen in self._vertices:
            for arista in vertice_origen.aristas:
                G.add_edge(vertice_origen.id, arista.destino.id, weight=arista.peso)

        return G

    def draw(
        self,
        highlight_edges=None,
        highlight_nodes=None,
        output_file=None,
        pos=None,
        curved_edges=False,
    ) -> None:
        import importlib.util

        if find_spec("matplotlib") is None:
            print("matplotlib no instalado")
            return None

        G = self.to_networkx()

        import matplotlib.pyplot as plt
        import networkx as nx

        if find_spec("pygraphviz"):
            pos = pos or nx.nx_agraph.graphviz_layout(G)
        else:
            pos = pos or nx.circular_layout(G)

        network_options = {
            "pos": pos,
            "font_size": 16,
            "font_color": "w",
            "font_family": "monospace",
            "node_size": 1000,
            "connectionstyle": "arc3, rad=-0.7" if curved_edges else "arc3",
        }

        if G.is_directed():
            network_options["arrowsize"] = 20

        if highlight_nodes:
            highlight_nodes_options = network_options | {
                "node_size": 1300,
                "node_color": "tab:orange",
            }
            nx.draw_networkx(G.subgraph(highlight_nodes), **highlight_nodes_options)

        if highlight_edges:
            edges_options = {
                "pos": pos,
                "edgelist": highlight_edges,
                "width": 5,
                "edge_color": "tab:orange",
            }
            nx.draw_networkx_edges(G, **edges_options)

        nx.draw_networkx(G, **network_options)

        if self._ponderado:
            edge_labels_options = {
                "pos": pos,
                "edge_labels": nx.get_edge_attributes(G, "weight"),
                "font_size": 12,
                "font_family": "monospace",
                "rotate": False,
            }
            nx.draw_networkx_edge_labels(G, **edge_labels_options)

        plt.axis("off")
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file)

        plt.show()


class DiGrafo(Grafo):
    def __init__(self):
        super().__init__()
        self._dirigido = True
