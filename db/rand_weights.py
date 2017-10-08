import random
import numpy as np

def rand_init(n,m,epsilon):
	rand_weights = np.zeros((n, m))
	for i in range(n):
		for j in range(m):	
			rand_weights[i][j] = random.uniform(0,1)*(2*epsilon) - epsilon
	return rand_weights
