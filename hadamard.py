import numpy as np
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos
from itertools import chain, combinations

class Hadarmard:

    def __init__(self, t, max=0, prohibidos=[], fijos=[]):
        self.prohibidos = prohibidos
        self.fijos = fijos
        indices_cobordes = np.arange(t-1, 4*t-1) - 2
        indices_cobordes = np.delete(indices_cobordes, prohibidos)
        self.t = t
        self.max = max if max!=0 else 3*t-1
        self.possible_comb = self.obtener_combinaciones_posibles(indices_cobordes)
        # Contruccion de R
        self.R = self.construye_R(t, t*2, t*4)
        # Actualiza la fila i de cada coborde i para tener dos -1
        cobordes = genera_cobordes_espacio(t)
        self.cobordes = np.array([self.cambia_fila_i(c,j+1) for c,j in zip(cobordes, range(0,len(cobordes)))])
        # Calculo del parametro r_i
        self.r_i = np.array([np.sum(self.R[i,:]==-1) for i in range(1,t)])
        print('Maximo de cobordes:',indices_cobordes)

    def construye_R(self, t, dos_t, cuatro_t):
        matriz_R = np.ones( (cuatro_t, cuatro_t), dtype=np.int32)
        for i in range(1,dos_t):
            matriz_R[i,(dos_t-i):dos_t] = -1 
            matriz_R[i,(cuatro_t-i):cuatro_t] = -1
        for i in range(dos_t,cuatro_t):
            matriz_R[i,(i-dos_t+1):i+1] = -1
        return matriz_R.copy()

    def cambia_fila_i(self, m, i):
        m[i] = m[i]*(-1)
        return m.copy()

    def obtener_combinaciones_posibles(self, cobordes):
        possible_comb = []
        for x in range(self.t-1,self.max):
            possible_comb += combinations(cobordes,x)
        
        return possible_comb

    def obtiene_matriz_hadamard(self, t, comb):
        if all(fijo in comb for fijo in self.fijos):
            return all (clasifica_caminos(comb, self.cobordes.copy(), i, self.r_i[i-1], t, self.R.copy()) for i in range(1,t))

    def __main__(self, t):
        res = None
        for ind in range(len(self.possible_comb)):
            if self.obtiene_matriz_hadamard(t, self.possible_comb[ind]):
                res = self.possible_comb[ind]
                self.possible_comb = self.possible_comb[ind+1:]
                break
        return res