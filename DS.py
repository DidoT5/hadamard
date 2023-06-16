import numpy as np
import numexpr as ne
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos
from hadamard import construye_R
import random

class DS:
    def __init__(self, t, max_cobordes=None):
        self.t = t
        cobordes = genera_cobordes_espacio(t)
        rango_cobordes =  range(0,len(cobordes))
        self.cobordes = np.array([self.cambia_fila_i(c,j+1) for c,j in zip(cobordes, rango_cobordes)])
        self.rango_cobordes = np.array(rango_cobordes)
        self.R = construye_R(t, t*2, t*4)
        self.r_i = np.array([np.sum(self.R[i,:]==-1) for i in range(1,t)])
        self.max_profundidad = max_cobordes if max_cobordes is not None else 4*t-2

    def cambia_fila_i(self, m, i):
        m[i] = m[i]*(-1)
        return m.copy()

    def fitness(self, comb):
        fitness = 0
        mat_comb = np.ones((4*self.t,4*self.t), dtype = np.int32)
        for c in comb:
            producto = self.cobordes[c].copy()
            mat_comb = ne.evaluate('mat_comb*producto')
        for i in range(1, self.t):
            if clasifica_caminos(comb, mat_comb[i], i, self.r_i[i-1], self.t, self.R.copy()):
                fitness += 1
        
        return fitness
    
    def fitlra_cobordes(self, selected):
        return self.rango_cobordes[np.bool_(selected)]

    def genera_inicio(self):
        estado = np.zeros(4*self.t-3, dtype=int)
        estado[:self.t-1] = 1
        np.random.shuffle(estado)
        return estado


#   Función DeepSearchConMemoria(estado, memoria):
    def deep_search(self, estado, memoria, fitness_actual, cobordes, profundidad):
#       Si estado es una solución:
        if fitness_actual == self.t-1:
#           Devolver solución
            return estado
    
#       Si estado está en memoria:
        if estado in memoria or profundidad == self.max_profundidad:
#           Devolver fracaso
            return None
    
#       Agregar estado a memoria
        memoria += [estado]

#       Para cada acción en acciones(estado):
        for i in range(len(cobordes)):
#           SiguienteEstado = aplicarAcción(estado, acción)
            siguiente_estado = np.sort(np.append(estado, cobordes[i]))
            fitness_siguiente_estado = self.fitness(siguiente_estado)
#           Si DeepSearchConMemoria(SiguienteEstado, memoria) es una solución:
            if fitness_siguiente_estado > fitness_actual:
                res = self.deep_search(siguiente_estado, memoria, fitness_siguiente_estado, np.delete(cobordes, i), profundidad+1)
                if res is not None:
    #               Devolver solución
                    return res
        
#       Eliminar estado de memoria
        memoria.remove(estado)
#       Devolver fracaso
        return None
    
    def __main__(self):
        res = None
        estado = self.genera_inicio()
        estado = self.fitlra_cobordes(estado)
        restantes = np.delete(self.rango_cobordes.copy(), estado)
        fitness_inicial = self.fitness(estado)
        res = self.deep_search(estado, [], fitness_inicial, restantes, self.t-1)
        return res