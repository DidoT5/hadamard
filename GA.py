import numpy as np
import numexpr as ne
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos
from hadamard import construye_R
import random

class GA:
    def __init__(self, t, n_individuals, n_selection, n_generations=200, mutation_rate = 0.1):
        self.t = t
        self.combinacion_hadamard = []
        self.mutation_rate = mutation_rate
        self.n_individuals = n_individuals
        self.n_selection = n_selection
        # Contruccion de R
        self.R = construye_R(t, t*2, t*4)
        cobordes = genera_cobordes_espacio(t)
        rango_cobordes =  range(0,len(cobordes))
        self.cobordes = np.array([self.cambia_fila_i(c,j+1) for c,j in zip(cobordes, rango_cobordes)])
        self.rango_cobordes = np.array(rango_cobordes)
        self.r_i = np.array([np.sum(self.R[i,:]==-1) for i in range(1,t)])
        self.n_generations = n_generations

    def cambia_fila_i(self, m, i):
        m[i] = m[i]*(-1)
        return m.copy()

    def create_individual(self):
        return np.random.choice([0, 1], size=(4*self.t-3,), p=[0.5, 0.5])

    def create_population(self):
        return [self.create_individual() for _ in range(self.n_individuals)]

    def fitness(self, individual):
        fitness = 0
        comb = self.rango_cobordes[np.bool_(np.flip(individual, axis=0))]
        mat_comb = np.ones((4*self.t,4*self.t), dtype = np.int32)
        for c in comb:
            producto = self.cobordes[c].copy()
            mat_comb = ne.evaluate('mat_comb*producto')
        for i in range(1, self.t):
            if clasifica_caminos(comb, mat_comb[i], i, self.r_i[i-1], self.t, self.R.copy()):
                fitness += 1
        if fitness == self.t-1:
            self.combinacion_hadamard.append(comb)
        return fitness
    
    def selection(self, population):

        scores = [(self.fitness(i), i) for i in population]
        scores = [gen[1] for gen in sorted(scores, key=lambda x: (x[0]))]

        return scores
    
    def reproduction(self, non_selected, selected):

        tam = len(selected[0])

        for i in range(self.n_individuals-self.n_selection):
            point = np.random.randint(0, tam - 1)
            father = random.sample(selected, 2)
            non_selected[i][:point] = father[0][:point]
            non_selected[i][point:] = father[1][point:]
        
        return selected+non_selected
    
    def mutation(self, t, population):
        
        for i in range(len(population)):
            if random.random() <= self.mutation_rate:
                point = np.random.randint(4*t-3)
                if population[i][point]:
                    population[i][point] = 1
                else:
                    population[i][point] = 0

        return population
    
    def run_geneticalgo(self):
        population = self.create_population()
        for i in range(self.n_generations): 
            ordered_population = self.selection(population)
            selected = ordered_population[self.n_individuals-self.n_selection:]
            non_selected = ordered_population[:self.n_individuals-self.n_selection]
            population = self.reproduction(non_selected, selected)
            population = self.mutation(self.t, population)
            if len(self.combinacion_hadamard) > 0:
                return self.combinacion_hadamard[0]
        return None

    def __main__(self):
        res = None
        res = self.run_geneticalgo()
        return res