import numpy as np

def multiplica_matriz_punto_por_punto(ma, a, mb, b, tam):
    ma[a] = ma[a]*(-1)
    mb[b] = mb[b]*(-1)
    return np.multiply(ma,mb)

def es_i_camino(ma, mb, i):
    return ma[i] == mb[i]
    