from unittest import TestCase

from edd.coladeprioridad import ColaDePrioridad


class TestColaDePrioridad(TestCase):
    def test_cola_de_prioridad(self):
        pq = ColaDePrioridad()
        pq.encolar("A", 3)
        pq.encolar("B", 2)
        pq.encolar("C", 4)
        pq.encolar("D", 1)
        self.assertFalse(pq.esta_vacia())
        self.assertEqual(pq.desencolar(), ("D", 1))
        self.assertEqual(pq.desencolar(), ("B", 2))
        self.assertEqual(pq.desencolar(), ("A", 3))
        self.assertEqual(pq.desencolar(), ("C", 4))
        self.assertTrue(pq.esta_vacia())
