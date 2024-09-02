class Pila:
    def __init__(self):
        self._elementos = []

    def esta_vacia(self):
        return len(self._elementos) == 0

    def apilar(self, elemento):
        self._elementos += [elemento]

    def desapilar(self):
        *self._elementos, elemento = self._elementos

        return elemento

    def __str__(self):
        return f"{repr(self.__elementos)} <>"
