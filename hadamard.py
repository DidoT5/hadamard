import numpy as np
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos
from itertools import combinations
import multiprocessing as mp
import timeit

class Hadarmard:

    def __init__(self, t):
        self.t = t
        self.comb_a = None
        self.comb_b = None
        # Contruccion de R
        self.R = self.construye_R(t, t*2, t*4)
        # Actualiza la fila i de cada coborde i para tener dos -1
        cobordes = genera_cobordes_espacio(t)
        self.cobordes = [self.cambia_fila_i(c,j+1) for c,j in zip(cobordes, range(0,len(cobordes)))]
        # Calculo del parametro r_i
        self.r_i = [np.sum(self.R[i,:]==-1) for i in range(1,t)]

    def obtener_combinacion_hadamard(self, num_cobordes, t):
        possible_comb_a = []
        possible_comb_b = []
        if(self.comb_a is None and self.comb_b is None):
            self.comb_a = 0
            self.comb_b = 0
            for x in range(3*t-1):
                possible_comb_a += combinations(range(2*t-1),x)
                possible_comb_b += combinations(range(2*t-1,4*t-3),x)
                
        for i in range(self.comb_a,len(possible_comb_a)):
            a = possible_comb_a[i]
            for j in range(self.comb_b, len(possible_comb_b)):
                b = possible_comb_b[j]
                if len(a) + len(b) < num_cobordes[-1]+1:
                    if (self.obtiene_matriz_hadamard(t, (a,b), self.cobordes.copy(), self.r_i, self.R.copy())):
                        self.comb_a = i
                        self.comb_b = j
                        return (a,b)
        return None

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
        return m

    def obtiene_matriz_hadamard(self, t, comb, cobordes, r_i, R):
        return all (clasifica_caminos(comb, cobordes, i, r_i[i-1], t, R) for i in range(1,t))

    def main(self, t):
        return self.obtener_combinacion_hadamard(range(3*t-1), t)