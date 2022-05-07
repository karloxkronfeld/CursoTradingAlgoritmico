import pandas as pd
import numpy as np


def presentar_carro(modelo, color, peso):
    print('Estre auto es un', modelo, 'de color', color, 'y pesa', peso)


modelo = 'Chevy del 76'
color = 'Rojo'
peso = 60

presentar_carro(modelo, color, peso)


class Crear_autos():
    def __init__(self, modelo, color, peso):
        self.modelo = modelo
        self.color = color
        self.peso = peso

    def presentar_carro(self):
        print('Estre auto es un', self.modelo, 'de color', self.color, 'y pesa', self.peso)


carro1 = Crear_autos('Bently', 'Azul', 35)
carro1.presentar_carro()


class Personas():
    def __init__(self, edad, altura, nombre):
        self.edad = edad
        self.altura = altura
        self.nombre = nombre

    def presentarse(self):
        print('Hola mi nombre es', self.nombre, 'y tengo', self.edad)


persona1 = Personas(38, 177, 'Carlos')

persona1.propietario = carro1
persona1.propietario.presentar_carro()
