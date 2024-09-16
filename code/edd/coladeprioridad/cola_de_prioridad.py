from heapq import heappop, heappush


class ColaDePrioridad:
    def __init__(self):
        self.__elementos = []

    def esta_vacia(self):
        return len(self.__elementos) == 0

    def encolar(self, elemento, prioridad):
        heappush(self.__elementos, (prioridad, elemento))

    def desencolar_minimo(self):
        prioridad, elemento = heappop(self.__elementos)

        return elemento, prioridad

    def __str__(self):
        return f"< [{", ".join(map(str, self.__elementos))}] <"
