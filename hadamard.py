import numpy as np
import numexpr as ne
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos
from itertools import combinations
import multiprocessing as mp
import timeit

class Hadarmard:

    def __init__(self, t, max=0):
        self.t = t
        self.last = 2**(t-1) -2
        # Contruccion de R
        self.R = self.construye_R(t, t*2, t*4)
        # Actualiza la fila i de cada coborde i para tener dos -1
        cobordes = genera_cobordes_espacio(t)
        rango_cobordes =  range(0,len(cobordes))
        self.cobordes = np.array([self.cambia_fila_i(c,j+1) for c,j in zip(cobordes, rango_cobordes)])
        self.rango_cobordes = np.array(rango_cobordes)
        # Calculo del parametro r_i
        self.r_i = np.array([np.sum(self.R[i,:]==-1) for i in range(1,t)])
        self.max = max

    def genera_siguiente_comb(self, min, max, fijos, width, rango_cobordes):
        # -- Una iteración fuera del bucle por si la siguiente combinación ya es válida --
        self.last += 1
        last = self.last
        binary_array = np.array(list(np.binary_repr(last, width=width)), dtype=np.int64)
        rango = ne.evaluate("sum(binary_array)")

        # Contar el número de 1's que hay en las posiciones prohibidas y restarlos al min de 1's
        # que debe haber, de forma que se obtenga la cantidad de unos reales que hay, y tras el bucle
        # aquellos que no deban estar, sean eliminados
        while rango < min or rango > max:
            last += 1
            # Incrementar el valor del primer 1 después de la posición encontrada
            binary_array = np.array(list(np.binary_repr(last, width=width)), dtype=np.int64)
            rango = ne.evaluate("sum(binary_array)")

        self.last = last
        return rango_cobordes[np.bool_(np.flip(binary_array, axis=0))]

    def construye_R(self, t, dos_t, cuatro_t):
        matriz_R = np.ones( (cuatro_t, cuatro_t), dtype=np.int32)
        for i in range(1,dos_t):
            matriz_R[i,(dos_t-i):dos_t] = -1 
            matriz_R[i,(cuatro_t-i):cuatro_t] = -1
        for i in range(dos_t,cuatro_t):
            matriz_R[i,(i-dos_t+1):i+1] = -1
        return matriz_R

    def cambia_fila_i(self, m, i):
        m[i] = m[i]*(-1)
        return m.copy()

    def obtiene_matriz_hadamard(self, comb):
        return all(clasifica_caminos(comb, self.cobordes.copy(), i, self.r_i[i-1], self.t, self.R.copy()) for i in range(1,self.t))

    def __main__(self, t, fijos=0, prohibidos=0):
        width = 4*t - 3
        max_pred = 2**(width)
        if self.last > max_pred:
            return None
        max = 3*t-2 if self.max == 0 else self.max
        self.last = fijos if fijos>self.last else self.last
        self.prohibidos = prohibidos
        width = 4*t - 3
        array_proh = np.array(list(np.binary_repr(prohibidos, width=width)), dtype=np.int64)
        array_fijos = np.array(list(np.binary_repr(fijos, width=width)), dtype=np.int64)
        borrado = array_fijos + array_proh
        fijos = np.sum(array_fijos)
        # Convertimos los 1's en 0's para una mascara
        xor_borrado = np.bitwise_xor(borrado,np.ones(width, np.int64))
        array_fijos = self.rango_cobordes[np.bool_(np.flip(array_fijos,axis=0))]
        rango_cobordes = self.rango_cobordes[np.bool_(np.flip(xor_borrado,axis=0))]
        width = len(rango_cobordes)
        resultado = False
        comb = None
        min = t-1 - fijos
        max -= fijos
        while not resultado and self.last < max_pred:
            comb = np.concatenate((self.genera_siguiente_comb(min, max, fijos, width, rango_cobordes),array_fijos))
            resultado = self.obtiene_matriz_hadamard(comb)
        return comb