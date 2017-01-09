#coding=utf-8
from django.test import TestCase

# Create your tests here.

from .models import *

class CifradoTest(TestCase):
    def test_cifrado_simetrico(self):
        cadena="áéíóúAEIOU"
        cadena_cifrada=cifrar(cadena, "abc")
        #print(cadena_cifrada)
        cadena_descifrada=descifrar(cadena_cifrada, "abc")
        #print(cadena_descifrada)
        self.assertEqual(cadena, cadena_descifrada)
        
    def test_cifrado_2(self):
        cadena="áéíóúAEIOU "
        clave="ÑñÚü"
        cadena_cifrada=cifrar(cadena, clave)
        #print(cadena_cifrada)
        cadena_descifrada=descifrar(cadena_cifrada, clave)
        #print(cadena_descifrada)
        self.assertEqual(cadena, cadena_descifrada) 
        
    def test_cifrado_3(self):
        cadena="!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÝÞßàáâãäåæçèéêëìíîïðñòó"
        clave="ÑñÚü"
        cadena_cifrada=cifrar(cadena, clave)
        #print(cadena_cifrada)
        cadena_descifrada=descifrar(cadena_cifrada, clave)
        #print(cadena_descifrada)
        self.assertEqual(cadena, cadena_descifrada)
        
    def test_cifrado_4(self):
        cadena="!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÝÞßàáâãäåæçèéêëìíîïðñòó"
        clave=cadena[4:40]
        cadena_cifrada=cifrar(cadena, clave)
        #print(cadena_cifrada)
        cadena_descifrada=descifrar(cadena_cifrada, clave)
        #print(cadena_descifrada)
        self.assertEqual(cadena, cadena_descifrada)