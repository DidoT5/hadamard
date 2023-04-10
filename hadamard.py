import numpy as np
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos, obtener_combinaciones_posibles

class Hadarmard:

    def __init__(self, t):
        self.t = t
        self.possible_comb = obtener_combinaciones_posibles(t)
        # Contruccion de R
        self.R = self.construye_R(t, t*2, t*4)
        # Actualiza la fila i de cada coborde i para tener dos -1
        cobordes = genera_cobordes_espacio(t)
        self.cobordes = [self.cambia_fila_i(c,j+1) for c,j in zip(cobordes, range(0,len(cobordes)))]
        # Calculo del parametro r_i
        self.r_i = [np.sum(self.R[i,:]==-1) for i in range(1,t)]

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

    def obtiene_matriz_hadamard(self, t, comb):
        return all (clasifica_caminos(comb, self.cobordes.copy(), i, self.r_i[i-1], t, self.R.copy()) for i in range(1,t))

    def main(self, t):
        res = None
        for ind in range(len(self.possible_comb)):
            if self.obtiene_matriz_hadamard(t, self.possible_comb[ind]):
                res = self.possible_comb[ind]
                self.possible_comb = self.possible_comb[ind+1:]
                break
        return res