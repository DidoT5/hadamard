import numpy as np
import numexpr as ne

def calcula_intersecciones(fila_i, R_i, t):
    return np.sum((fila_i[1:4*t] == R_i[1:4*t]) & (fila_i[1:4*t] == -1))

def calcula_caminos_combinacion(comb, i, t):
    # -- Declaración de variables --
    comb_a =comb[ne.evaluate("comb < (t*2)-1")]
    comb_b = comb[ne.evaluate("comb >= (t*2)-1")]
    dos_t = 2*t
    cuatro_t = 4*t
    caminos = 0
    # -- Cálculo de los caminos del conjunto a --
    if len(comb_a) > 0:
        def coincidente_a(c):
            return (c+i)%(dos_t)
        def coincidente_a_neg(c):
            return (c-i)%(dos_t)
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
                    caminos += 1
                comb_a = np.delete(comb_a,camino)
            else:
                coincidente_neg = np.argmax(comb_a == coincidente_a_neg(c))
                if coincidente_neg != 0:
                    camino = [0]
                    while coincidente_neg != 0:
                        camino.append(coincidente_neg)
                        coin_value = coincidente_a_neg(comb_a[coincidente_neg])
                        coincidente_neg = np.argmax(comb_a == coin_value)
                    if not (coin_value==comb_a[camino[0]]):
                        caminos += 1
                    comb_a = np.delete(comb_a,camino)
                else:
                    comb_a = np.delete(comb_a,0)
                    caminos += 1

    # -- Cálculo de los caminos del conjunto b --
    if len(comb_b) > 0:
        def coincidente_b(c):
            res = (c+i)%(cuatro_t)
            return res if res >= (dos_t-1) else res + dos_t -1
        def coincidente_b_neg(c):
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
                    caminos += 1
                comb_b = np.delete(comb_b,camino)
            else:
                coincidente_neg =  np.argmax(comb_b == coincidente_b_neg(c))
                if coincidente_neg != 0:
                    camino = [0]
                    while coincidente_neg != 0:
                        camino.append(coincidente_neg)
                        coin_value = coincidente_b_neg(comb_b[coincidente_neg])
                        coincidente_neg = np.argmax(comb_b == coin_value)
                    if not (coin_value==comb_b[camino[0]]):
                        caminos += 1
                    comb_b = np.delete(comb_b,camino)
                else:
                    comb_b = np.delete(comb_b,0)
                    caminos += 1
    return caminos

def es_fila_i_hadamard(c_i, I_i, t, r_i):
    return (2*c_i - 2*I_i) - (2*t - r_i) == 0

def clasifica_caminos(comb, fila_i, i, r_i, t, R):
    c_i = calcula_caminos_combinacion(comb, i, t)
    I_i = calcula_intersecciones(fila_i, R[i,:], t)
    return es_fila_i_hadamard(c_i, I_i, t, r_i)