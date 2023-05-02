import numpy as np
import numexpr as ne

def calcula_intersecciones(fila_i, R_i, t):
    return np.sum((fila_i[1:4*t] == R_i[1:4*t]) & (fila_i[1:4*t] == -1))

def calcula_caminos_combinacion(comb, i, t):
    # -- Declaración de variables --
    comb = np.array(comb)
    comb_a =comb[ne.evaluate("comb < (t*2)-1")]
    comb_b = comb[ne.evaluate("comb >= (t*2)-1")]
    dos_t = 2*t
    cuatro_t = 4*t
    caminos_a = []
    caminos_b = []

    # -- Cálculo de los caminos del conjunto a --
    if len(comb_a) > 0:
        def coincidente_a(c):
            return (c+i)%(dos_t)
        caminos_a = []
        while len(comb_a)>0:
            c = comb_a[0]
            coincidente = np.argmax(comb_a == coincidente_a(c))
            if coincidente != 0:
                camino = [0]
                while coincidente != 0:
                    camino.append(coincidente)
                    coin_value = coincidente_a(comb_a[coincidente])
                    coincidente = np.argmax(comb_a == coin_value)
                if not (coin_value==comb_a[camino[0]]):
                    caminos_a.append(comb_a[camino])
                comb_a = np.delete(comb_a,camino)
            else:
                comb_a = np.delete(comb_a,0)
                caminos_a.append(np.array([c]))

    # -- Cálculo de los caminos del conjunto b --
    if len(comb_b) > 0:
        def coincidente_b(c):
            res = (c+i)%(cuatro_t)
            return res if res >= (dos_t-1) else res + dos_t -1
        while len(comb_b)>0:
            c = comb_b[0]
            coincidente = np.argmax(comb_b == coincidente_b(c))
            if coincidente != 0:
                camino = [0]
                while coincidente != 0:
                    camino.append(coincidente)
                    coin_value = coincidente_b(comb_b[coincidente])
                    coincidente = np.argmax(comb_b == coin_value)
                if not (coin_value==comb_b[camino[0]]):
                    caminos_b.append(comb_b[camino])
                comb_b = np.delete(comb_b,camino)
            else:
                comb_b = np.delete(comb_b,0)
                caminos_b.append(np.array([c]))
    caminos = caminos_a + caminos_b
    return caminos

def es_fila_i_hadamard(c, I_i, t, r_i):
    return (2*c - 2*I_i) - (2*t - r_i) == 0

def clasifica_caminos(comb, cobordes, i, r_i, t, R):
    caminos = calcula_caminos_combinacion(comb, i, t)
    fila_i = np.ones(4*t, dtype = np.int32)
    c_i = len(caminos)
    for c in comb:
        producto = cobordes[c][i]
        fila_i = ne.evaluate('fila_i*producto')
    I_i = calcula_intersecciones(fila_i, R[i,:], t)
    return es_fila_i_hadamard(c_i, I_i, t, r_i)