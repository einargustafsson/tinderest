import numpy as np

def sigmoid(z):
	"""Compute sigmoid of z"""
	h = np.zeros(len(z))
	for i in range(len(z)):
		h[i] = 1.0 / (1.0 + np.exp(-z[i]));
	return h


