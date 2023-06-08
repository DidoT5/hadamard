import numpy as np
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos
import random

class GA:
    def __init__(self, t, n_individuals, n_selection, n_generations=200, mutation_rate = 0.1):
        self.t = t
        self.combinacion_hadamard = []
        self.mutation_rate = mutation_rate
        self.n_individuals = n_individuals
        self.n_selection = n_selection
        # Contruccion de R
        self.R = self.construye_R(t, t*2, t*4)
        cobordes = genera_cobordes_espacio(t)
        rango_cobordes =  range(0,len(cobordes))
        self.cobordes = np.array([self.cambia_fila_i(c,j+1) for c,j in zip(cobordes, rango_cobordes)])
        self.rango_cobordes = np.array(rango_cobordes)
        self.r_i = np.array([np.sum(self.R[i,:]==-1) for i in range(1,t)])
        self.n_generations = n_generations

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
        return m.copy()

    def create_individual(self):
        return np.random.choice([0, 1], size=(4*self.t-3,), p=[0.5, 0.5])

    def create_population(self):
        return [self.create_individual() for _ in range(self.n_individuals)]

    def fitness(self, individual):
        fitness = 0
        comb = self.rango_cobordes[np.bool_(np.flip(individual, axis=0))]
        for i in range(1, self.t):
            if clasifica_caminos(comb, self.cobordes.copy(), i, self.r_i[i-1], self.t, self.R.copy()):
                fitness += 1
        if fitness == self.t-1:
            self.combinacion_hadamard.append(individual)
        return fitness
    
    def selection(self, population):

        scores = [(self.fitness(i), i) for i in population]
        scores = [gen[1] for gen in sorted(scores, key=lambda x: (x[0]))]

        return scores[len(scores)-self.n_selection:]
    
    def reproduction(self, population, selected):

        tam = len(population[0])

        for i in range(len(population)):
            point = np.random.randint(0, tam - 1)
            father = random.sample(selected, 2)
            population[i][:point] = father[0][:point]
            population[i][point:] = father[1][point:]
        
        return population
    
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
            selected = self.selection(population)
            population = self.reproduction(population, selected)
            population = self.mutation(self.t, population)
            if len(self.combinacion_hadamard) > 0:
                return self.combinacion_hadamard[0]
        return None

    def __main__(self):
        return self.run_geneticalgo()