import numpy as np

def dsig(a):
	gacc =[]
	for e in range(len(a)):
		gacc.append(a[e]*(1-a[e]))
	return gacc
		


