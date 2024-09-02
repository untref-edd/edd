from unittest import TestCase

from edd.pila import Pila


class TestPila(TestCase):
    def test_pila(self):
        s = Pila()
        s.apilar("A")
        s.apilar("B")
        self.assertFalse(s.esta_vacia())
        self.assertEqual(s.desapilar(), "B")
        self.assertEqual(s.desapilar(), "A")
        self.assertTrue(s.esta_vacia())
