from django.test import TestCase

# Create your tests here.

from .models import *

class CifradoTest(TestCase):
    def test_cifrado_simetrico(self):
        cadena="1234"
        cadena_cifrada=cifrar(cadena, "abc")
        cadena_descifrada=descifrar(cadena_cifrada, "abc")
        self.assertEqual(cadena_cifrada, cadena_descifrada)