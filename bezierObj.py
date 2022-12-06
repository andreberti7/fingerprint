import numpy as np
import bezier
import matplotlib.pyplot as plt
import json


def generateCurve(x,y,k,id1,id2):
	#genero la curva di Bezier da tutte le coordinate x,y dei punti del ridge
	#k è il numero di punti del ridge
	#faccio il plot della curva
	
	
	#problema con k > 1000, non calcola la curva e quindi devo diminuire i punti in ingresso
	if k > 1000:
		b = list(range(1, k-1,2))
		x = np.delete(x,b,0)
		y = np.delete(y,b,0)		
		k = x.size
	
	nodes = np.asfortranarray([x,y])
	
	curve = bezier.Curve(nodes, degree=k-1)
	#curve.plot(k,color="green")
	
	#valuto la curva in n punti
	n = k
	#genero n punti equidistanti tra 0 e 1
	s_vals = np.linspace(0.0, 1.0, n)
	#valuto la curva in n punti e genero n coordinate
	#più n è grande e più sarà precisa
	x1=curve.evaluate_multi(s_vals)[0]
	y1=curve.evaluate_multi(s_vals)[1]
	#plot delle coordinate calcolate
	#plt.scatter(x1,y1,s=10,c='red')
	
	
	#a = soglia di correttezza approssimazione
	a = 1
	i = 0
	count = 0
	while i < n:
		if abs(x1[i]-x[i]) <= a:
			count = count + 1
		#else:
			#print(x1[i]-x[i])
			
		if abs(y1[i]-y[i]) <= a:
			count = count + 1
		#else:
			#print(y1[i]-y[i])
		i=i+1
	print(f"Approssimazioni corrette ridge {id1}-{id2}: {count}/{n*2}")

data = json.load(open("../Sourceafis/transparency_012_3_2.tif/inheritance/ridges.json"))
ridges = len(data["ridges"])


i=0
k=0
while i < ridges:#ridges
	points = len(data["ridges"][i]["pixels"])
	while k < points:
		if k == 0:
			x = np.array([data["ridges"][i]["pixels"][k]["X"]])
			y = np.array([data["ridges"][i]["pixels"][k]["Y"]])
		else:
			x = np.r_[x,[data["ridges"][i]["pixels"][k]["X"]]]
			y = np.r_[y,[data["ridges"][i]["pixels"][k]["Y"]]]
		k=k+1
	generateCurve(x,y,k,data["ridges"][i]["ID1"],data["ridges"][i]["ID2"])
	i=i+1
	k=0
	#plt.scatter(x,y,s=1,c='green')
	
	


#plt.xlim(0,500)
#plt.ylim(0,500)

#plt.show();
