import numpy as np
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos, obtener_combinaciones_posibles

class Hadarmard:

    def __init__(self):
        pass

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

    def obtiene_matriz_hadamard(self, t, comb, cobordes, r_i, R):
        return all (clasifica_caminos(comb, cobordes.copy(), i, r_i[i-1], t, R.copy()) for i in range(1,t))

    def main(self, t):
        # Calculo del parametro w
        num_cobordes = range(t-1,3*t-1)
        # Creamos una lista de todas las posibles combinaciones de cobordes
        possible_comb = obtener_combinaciones_posibles(num_cobordes, t)
        # Contruccion de R
        R = self.construye_R(t, t*2, t*4)
        # Actualiza la fila i de cada coborde i para tener dos -1
        cobordes = genera_cobordes_espacio(t)
        cobordes = [self.cambia_fila_i(c,j+1) for c,j in zip(cobordes, range(0,len(cobordes)))]
        # Calculo del parametro r_i
        r_i = [np.sum(R[i,:]==-1) for i in range(1,t)]
        res = None
        for comb in possible_comb:
            if self.obtiene_matriz_hadamard(t, comb, cobordes, r_i, R):
                res = comb
                break
        return res