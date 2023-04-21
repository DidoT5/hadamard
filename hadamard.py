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

    def genera_siguiente_comb(self, min, max, array_proh, xor_prohib, array_fijos, width):
        # -- Una iteración fuera del bucle por si la siguiente combinación ya es válida --
        self.last += 1
        last = self.last
        binary_array = np.array(list(np.binary_repr(last, width=width)), dtype=np.int64) | self.array_fijos
        coincidentes_prohib = ne.evaluate("sum(binary_array * array_proh)")
        rango = ne.evaluate("sum(binary_array)")
        if coincidentes_prohib > 0:
            rango = ne.evaluate("rango - coincidentes_prohib - 1")

        # Contar el número de 1's que hay en las posiciones prohibidas y restarlos al min de 1's
        # que debe haber, de forma que se obtenga la cantidad de unos reales que hay, y tras el bucle
        # aquellos que no deban estar, sean eliminados
        while rango < min or rango > max:
            last += 1
            # Incrementar el valor del primer 1 después de la posición encontrada
            binary_array = np.array(list(np.binary_repr(last, width=width)), dtype=np.int64) | self.array_fijos
            coincidentes_prohib = ne.evaluate("sum(binary_array * array_proh)")
            rango = ne.evaluate("sum(binary_array)")
            if coincidentes_prohib > 0:
                rango = ne.evaluate("rango - coincidentes_prohib - 1")
            
        # Si algún número resultante es coincidente con un prohibido
        if coincidentes_prohib > 0:
            # Eliminamos los 1's prohibidos con los 0's de la máscara
            binary_array = ne.evaluate("binary_array * xor_prohib")
        self.last = last
        return self.rango_cobordes[np.bool_(np.flip(binary_array, axis=0))]

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
        self.array_proh = np.array(list(np.binary_repr(prohibidos, width=width)), dtype=np.int64)
        self.array_fijos = np.array(list(np.binary_repr(fijos, width=width)), dtype=np.int64)
        # Convertimos los 1's en 0's para una mascara
        xor_prohib = np.bitwise_xor(self.array_proh,np.ones(width, np.int64))
        resultado = False
        comb = None
        while not resultado and self.last < max_pred:
            comb = self.genera_siguiente_comb(t-1, max, self.array_proh, xor_prohib, self.array_fijos, width)
            resultado = self.obtiene_matriz_hadamard(comb)
        return comb