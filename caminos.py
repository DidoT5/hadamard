import numpy as np

def multiplica_matriz_punto_por_punto(ma, a, mb):
    ma[a] = ma[a]*(-1)
    return np.multiply(ma,mb)

def calcula_numero_caminos_e_intersecciones(ma, mb, i):
    ac = 0
    for j in range(1,t):
        ac += ma[i,j] == mb[i,j] == -1
    return ac

def clasifica_caminos():
    pass

'''
Hacer método para guardar las combinaciones que forman un i-camino con memoria,
es decir, crear un diccionario en el que se almacenan las combinaciones de matrices y la matriz con la que forman un i-camino
y una cola de posibles combinaciones de las que se eliminen los elementos reversos
Ejemplo: (m1,m2) == (m2,m1) -> Sólo se comprueba el primer literal

El número de intersecciones en i se define como la cantidad -1 que tienen en las mismas posiciones la matriz R y las combinaciones
de los cobordes
'''


    