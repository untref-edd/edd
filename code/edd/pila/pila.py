class Pila:
    def __init__(self):
        self.__elementos = []

    def esta_vacia(self):
        return len(self.__elementos) == 0

    def apilar(self, elemento):
        self.__elementos += [elemento]

    def desapilar(self):
        *self.__elementos, elemento = self.__elementos

        return elemento

    def __str__(self):
        return f"[{', '.join(map(str, self.__elementos))}] <>"
