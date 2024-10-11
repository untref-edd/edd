from __future__ import annotations

from importlib.util import find_spec
from math import inf
from typing import Callable

from ..cola import Cola
from ..coladeprioridad import ColaDePrioridad


class Vertice:
    def __init__(self, _id: str) -> None:
        self._id = _id
        self._aristas: set[Arista] = set()
        self._grado_entrada = 0

    @property
    def id(self) -> str:
        return self._id

    @property
    def aristas(self) -> set[Arista]:
        return set(self._aristas)

    @property
    def grado_entrada(self) -> int:
        return self._grado_entrada

    @property
    def adyacentes(self) -> set[Vertice]:
        return {arista.destino for arista in self.aristas}

    def agregar_arista(self, arista: Arista) -> None:
        if arista not in self._aristas:
            self._aristas.add(arista)
            arista.destino._grado_entrada += 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vertice):
            return False

        return self._id == other._id

    def __hash__(self):
        return hash((self._id,))

    def __repr__(self) -> str:
        return f"Vertice({repr(self._id)})"

    def __str__(self) -> str:
        return self._id

    def __lt__(self, other: Vertice) -> bool:
        """
        Se implementa para poder comparar vértices en un heap.
        """
        return False


class Arista:
    def __init__(self, origen: Vertice, destino: Vertice, peso: int | float | None = None) -> None:
        self._origen = origen
        self._destino = destino
        self._peso = peso

    @property
    def vertices(self) -> tuple[Vertice, Vertice]:
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

    def __iter__(self):
        """
        Se implementa para poder desempaquetar la arista de la forma:

        >>> arista = Arista(Vertice("A"), Vertice("B"), 10)
        >>> origen, destino, peso = arista
        """
        return iter((self._origen, self._destino, self._peso))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Arista):
            return False

        return (self._origen, self._destino, self._peso) == (other._origen, other._destino, other._peso)

    def __hash__(self):
        return hash((self._origen, self._destino, self._peso))

    def __repr__(self) -> str:
        return f"Arista({repr(self.origen)}, {repr(self.destino)}, {repr(self.peso)})"


class Grafo:
    def __init__(self) -> None:
        self._vertices: dict[str, Vertice] = {}
        self._aristas: set[Arista] = set()
        self._dirigido: bool = False
        self._ponderado: bool = False

    @property
    def vertices(self) -> set[Vertice]:
        return set(self._vertices.values())

    @property
    def aristas(self) -> set[Arista]:
        return self._aristas

    @property
    def dirigido(self) -> bool:
        return self._dirigido

    @property
    def ponderado(self) -> bool:
        return self._ponderado

    def adyacentes(self, vertice: str) -> set[Vertice]:
        return self._vertices[vertice].adyacentes

    def agregar_arista(self, origen: str, destino: str, peso: int | float | None = None) -> None:
        vertice_origen = self._vertices.setdefault(origen, Vertice(origen))
        vertice_destino = self._vertices.setdefault(destino, Vertice(destino))

        self.__agregar_arista(vertice_origen, vertice_destino, peso)

        if not self._dirigido:
            self.__agregar_arista(vertice_destino, vertice_origen, peso)

        if peso is not None:
            self._ponderado = True

    def __agregar_arista(self, origen: Vertice, destino: Vertice, peso: int | float | None = None) -> None:
        arista = Arista(origen, destino, peso)
        if arista not in self._aristas:
            self._aristas.add(arista)
            origen.agregar_arista(arista)

    def __getitem__(self, id: str) -> Vertice | None:
        return self._vertices.get(id)

    def __str__(self) -> str:
        out = f"Vertices: { {str(v) for v in self.vertices} }\n\n"
        arrow_head = ">" if self._dirigido else ""
        for arista in self.aristas:
            if self._ponderado:
                out += f"\t{arista.origen} --{arista.peso or 0}--{arrow_head} {arista.destino}\n"
            else:
                out += f"\t{arista.origen} --{arrow_head} {arista.destino}\n"

        return out

    def to_networkx(self):
        if find_spec("networkx") is None:
            print("networkx no instalado")
            return None

        import networkx as nx  # type: ignore

        G = nx.DiGraph() if self._dirigido else nx.Graph()

        for arista in self.aristas:
            G.add_edge(arista.origen.id, arista.destino.id, weight=arista.peso)

        return G

    def draw(
        self,
        highlight_edges=None,
        highlight_nodes=None,
        nodes_group=None,
        node_labels=None,
        output_file=None,
        pos=None,
        curved_edges=False,
        layout="circular",
    ) -> None:
        import importlib.util

        if find_spec("matplotlib") is None:
            print("matplotlib no instalado")
            return None

        G = self.to_networkx()

        import matplotlib.pyplot as plt
        import networkx as nx

        label_offset = lambda x, y: (x + 0, y + 0.15)

        if pos is None:
            match layout, find_spec("pygraphviz") is not None:
                case "graphviz", True:
                    pos = nx.nx_agraph.graphviz_layout(G)
                    label_offset = lambda x, y: (x + 0, y + 25)
                case "circular", _:
                    pos = nx.circular_layout(G)
                    label_offset = lambda x, y: (x + 0, y + 0.15)
                case _:
                    pos = nx.circular_layout(G)
                    label_offset = lambda x, y: (x + 0, y + 0.15)

        network_options = {
            "pos": pos,
            "font_size": 16,
            "font_color": "w",
            "font_family": "monospace",
            "node_size": 1000,
            "node_color": "tab:blue",
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

        if nodes_group:
            nodes_options = {
                "pos": pos,
                "node_size": 1000,
                "node_color": "tab:green",
                "nodelist": nodes_group,
            }
            nx.draw_networkx_nodes(G, **nodes_options)

        if self._ponderado:
            edge_labels_options = {
                "pos": pos,
                "edge_labels": nx.get_edge_attributes(G, "weight"),
                "font_size": 12,
                "font_family": "monospace",
                "rotate": False,
            }
            nx.draw_networkx_edge_labels(G, **edge_labels_options)

        if node_labels:
            node_labels_options = {
                "pos": {v: label_offset(x, y) for v, (x, y) in pos.items()},
                "labels": node_labels,
                "font_size": 12,
                "font_family": "monospace",
                "font_weight": "bold",
                "font_color": "tab:green",
                "bbox": {
                    "facecolor": "w",
                    "edgecolor": "none",
                    "alpha": 0.8,
                    "boxstyle": "round, pad=0.3",
                },
            }
            nx.draw_networkx_labels(G, **node_labels_options)

        plt.axis("off")
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file)

        plt.show()


class GrafoConCicloError(Exception):
    pass


class GrafoConCicloNegativoError(Exception):
    pass


class DiGrafo(Grafo):
    def __init__(self):
        super().__init__()
        self._dirigido = True

    def orden_topologico(self, visitar: Callable[[Vertice], None]) -> None:
        q: Cola = Cola()

        grado_entrada: dict[Vertice, int] = {v: v.grado_entrada for v in self.vertices}
        for v, grado in grado_entrada.items():
            if grado == 0:
                q.encolar(v)

        while not q.esta_vacia():
            v = q.desencolar()

            visitar(v)

            for w in v.adyacentes:
                grado_entrada[w] -= 1
                if grado_entrada[w] == 0:
                    q.encolar(w)

        if any(grado > 0 for grado in grado_entrada.values()):
            raise GrafoConCicloError("El grafo presenta un ciclo y no es posible definir un orden topológico")

    def dijkstra(self, s: Vertice | str) -> tuple[dict[Vertice, float], dict[Vertice, Vertice | None]]:
        s = self._vertices[str(s)]

        pq: ColaDePrioridad = ColaDePrioridad()

        distancia: dict[Vertice, float] = {v: inf for v in self.vertices}
        previo: dict[Vertice, Vertice | None] = {v: None for v in self.vertices}
        visitado: dict[Vertice, bool] = {v: False for v in self.vertices}

        distancia[s] = 0
        pq.encolar(s, distancia[s])

        while not pq.esta_vacia():
            v, _ = pq.desencolar_minimo()

            visitado[v] = True

            for _, w, peso_v_w in v.aristas:
                if not visitado[w] and distancia[v] + peso_v_w < distancia[w]:
                    distancia[w] = distancia[v] + peso_v_w
                    previo[w] = v
                    pq.encolar(w, distancia[w])

        return distancia, previo

    def bellman_ford(self, s: Vertice | str) -> tuple[dict[Vertice, float], dict[Vertice, Vertice | None]]:
        s = self._vertices[str(s)]

        distancia: dict[Vertice, float] = {v: inf for v in self.vertices}
        previo: dict[Vertice, Vertice | None] = {v: None for v in self.vertices}

        distancia[s] = 0

        for i in range(1, len(self.vertices)):
            for v, w, peso_v_w in self.aristas:
                if distancia[v] + peso_v_w < distancia[w]:
                    distancia[w] = distancia[v] + peso_v_w
                    previo[w] = v

        for v, w, peso_v_w in self.aristas:
            if distancia[v] + peso_v_w < distancia[w]:
                raise GrafoConCicloNegativoError("El grafo contiene un ciclo de peso negativo")

        return distancia, previo
