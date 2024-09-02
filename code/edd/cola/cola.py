class Cola:
    def __init__(self):
        self.__elementos = []

    def esta_vacia(self):
        return len(self.__elementos) == 0

    def encolar(self, elemento):
        self.__elementos += [elemento]

    def desencolar(self):
        elemento, *self.__elementos = self.__elementos

        return elemento

    def __str__(self):
        return f"< {repr(self.__elementos)} <"
