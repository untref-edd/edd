from unittest import TestCase

from edd.cola import Cola


class TestCola(TestCase):
    def test_cola(self):
        q = Cola()
        q.encolar("A")
        q.encolar("B")
        self.assertFalse(q.esta_vacia())
        self.assertEqual(q.desencolar(), "A")
        self.assertEqual(q.desencolar(), "B")
        self.assertTrue(q.esta_vacia())
