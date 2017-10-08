import json	
from pprint import pprint
import math
import numpy as np


## Create tuples of all features in the list ##
with open('mumbai_restaurants.json') as json_rest:
	dr = json.load(json_rest)	#dict
	res_lst = []
	
	
	dicr = dr['results']
	for el in range(len(dicr)):
	
		a = dicr[el]

		res_lst.append(a['name'])
res_tup = tuple(res_lst)


with open('user_db_1000.json') as json_data:
	d = json.load(json_data)


vac_tup = ("Cholera", "Dengue", "Diphtheria", "Hepatitis A", "Hepatitis B", "Hepatitis E", "Haemophilus influenzae type b (Hib)", "Human papillomavirus (HPV)", "Influenza", "Japanese encephalitis", "Malaria", "Measles", "Meningococcal meningitis", "Mumps", "Pertussis", "Pneumococcal disease", "Poliomyelitis", "Rabies", "Rotavirus", "Rubella", "Tetanus", "Tick-borne encephalitis", "Tuberculosis", "Typhoid", "Varicella", "Yellow Fever")
al_tup = ('shellfish', 'milk', 'eggs', 'nuts', 'soy', 'wheat', 'corn')

## Get matching tuples for training subjects ##
allergy_vec = []
restaurant_vec = []

for el in range(len(d)):
	dic = d[el]

	r = dic['restaurantVisits']	#list	

	id_res = []
	id_vac = []
	id_al = []
	
	for s in range(len(r)):
		if res_tup.index(r[s]) not in id_res:
			id_res.append(res_tup.index(r[s]))

	id_res.sort()

	h = dic['health']	#dict

	v = h['vaccinations']	#list

	for t in range(len(v)):
		if vac_tup.index(v[t]) not in id_vac:
			id_vac.append(vac_tup.index(v[t]))
	id_vac.sort()

	a = h['allergies']	#list

	for u in range(len(a)):
		if al_tup.index(a[u]) not in id_al:
			id_al.append(al_tup.index(a[u]))
			
	id_al.sort()
	
	if id_al and id_res:
		allergy_vec.append(id_al[0])	# take only first allergy
		restaurant_vec.append(id_res[0])	# take only first restaurant


X = np.zeros((len(al_tup), len(allergy_vec)))


y = np.zeros((len(res_tup), len(restaurant_vec)))

cnt = 0
for i in allergy_vec:
	X[i][cnt] = 1
	cnt += 1

count = 0
for j in restaurant_vec:
	y[j][count] = 1
	count += 1


## Create Neural Network ##
m = len(allergy_vec)

inp_lay_size = len(al_tup)

num_output = len(res_tup)

hid_lay_size = 30

# Visualize data
import matplotlib.pyplot as plt
plt.scatter(allergy_vec,restaurant_vec)
#plt.show()

# Random initialize weights
import rand_weights
epsilon = math.sqrt(6)/math.sqrt(inp_lay_size+num_output)

init_weights1 = rand_weights.rand_init(hid_lay_size,inp_lay_size+1,epsilon) # (30,8)
init_weights2 = rand_weights.rand_init(num_output,hid_lay_size+1,epsilon)	# (20,31)

####
import sigmoid
import dsig
delta1 = np.zeros((hid_lay_size,inp_lay_size))
delta2 = np.zeros((num_output,hid_lay_size))

w1_grad = np.zeros((hid_lay_size,len(al_tup))) #(30,7)
w2_grad = np.zeros((num_output,hid_lay_size)) #(20,30)


bias1 = np.ones((1,m))
Xb = np.concatenate((bias1,X)) # with bias of 1


for i in range(m):
	# Forward propagation
	a1 = np.dot(init_weights1,Xb[:,i]) # (30x1)
	z1 = sigmoid.sigmoid(a1)	# (30x1)

	z1b = [1]
	for s in range(len(z1)):
		z1b.append(z1[s]) # add bias of 1

	a2 = np.dot(init_weights2,z1b)	# (20x1)
	z2 = sigmoid.sigmoid(a2)	# (20x1)

	# Backward propagation
	
	delt3 = z2 - y[:,i] # (20x1)

	gacc2 = dsig.dsig(a1) # (30x1)
	iwt2 = init_weights2.transpose()	# (30x20)
	iwtr2 = iwt2[1:][:]

	delt2dp = np.dot(iwtr2,delt3)
	delt2 = np.multiply(delt2dp,gacc2)	# (30x1)

	d3 = np.matrix(delt3)
	d3t = d3.transpose() #(20x1)
	a_1 = np.matrix(a1)	#(1x30)
	add1 = np.dot(d3t,a_1)

	w2_grad = w2_grad + add1  # (20x30)

	d2 = np.matrix(delt2)
	d2t = d2.transpose()	#(30x1)
	Xm = np.matrix(X[:,i])	#(1x7)
	add2 = np.dot(d2t,Xm)
	
	w1_grad = w1_grad + add2 #(30x7)

## import test data here ##

with open('app_user_milk.json') as json_app:
	dapp = json.load(json_app)	#dict
	h_app = dapp['health']
	al_app = h_app['allergies']

	id_al_app = []
	for u in range(len(al_app)):
		if al_tup.index(al_app[u]) not in id_al_app:
			id_al.append(al_tup.index(al_app[u]))

	test_al = np.zeros(len(al_tup))
	for i in id_al:
		test_al[i] = 1


# Forward propagation
test_al_bias = [1]
for tb in range(len(test_al)):
		test_al_bias.append(test_al[tb]) # add bias of 1

test_al_mat = np.matrix(test_al)

a1_app = np.dot(w1_grad,test_al_mat.transpose()) # (30x1)

z1_app = sigmoid.sigmoid(a1_app)
z1_app_mat = np.matrix(z1_app)

a2_app = np.dot(z1_app_mat,w2_grad.transpose()) 
z2_app = sigmoid.sigmoid(a2_app.transpose())
z2_app_mat = np.matrix(z2_app)

sel_rest_val = np.amax(a2_app)
sel_rest_ind = np.argmax(a2_app)


print(res_tup[sel_rest_ind])

	







	






