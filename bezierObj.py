import numpy as np
import bezier
import matplotlib.pyplot as plt
import json
import math
from math import cos, sin, radians
from numpy import array, dot

#x = coordinate x del ridge
#y = coordinate y del ridge
#id1,id2 = identificatore del ridge
#start,end = indici di inzio e fine ridge dopo aver analizzato i cambi di direzione
def generateCurve(x,y,k,id1,id2,start,end):
	
	#controllo se sono all'inizio
	if start == 0:
		print(f"-------- Inizio del ridge: {id1}-{id2} --------")
		print("")
		
	#print(f"Inizio ridge: {start}")
	#print(f"Fine ridge: {end}")

	#genero la curva di Bezier dalle coordinate x,y dei punti del ridge
	#k è il numero di punti del ridge
	
	#coontrollo se il ridge è stato spezzato e quindi se mi trovo all'inizio o in mezzo
	if k != end:
		k=end+1
		
	#problema con k > 1000, non calcola la curva e quindi devo diminuire i punti in ingresso -> RISOLTO SPEZZANDO I RIDGE
	#if k > 1000:
		#b = list(range(1, k,2))
		#x = np.delete(x,b,0)
		#y = np.delete(y,b,0)		
		#k = x.size
	
	match = 0.0 #percentuale di confronti corretti
	cp = 1 #numero minimo control points, parto da 1 per ridge con un solo punto poi 2,3,4,8,12,16...
	
	#controlli di fine ciclo alla fine del while
	while True:
		x1 = np.empty(shape=0, dtype=int) #array di x con cp punti dal quale costruisco la curva
		y1 = np.empty(shape=0, dtype=int) #array di y con cp punti dal quale costruisco la curva
		x_c = np.empty(shape=0) #array di x dove inserisco le coordinate corrette
		y_c = np.empty(shape=0) #array di y dove inserisco le coordinate corrette
		x_cn = np.empty(shape=0) #array di x dove inserisco le coordinate non corrette (?)
		y_cn = np.empty(shape=0) #array di y dove inserisco le coordinate non corrette (?)
		
		#creo x1 e y1 con cp punti presi da x e y in modo equidistante
		#esempio cp = 4 e k = 10 -> b = 0,3,6,9
		b = list(np.linspace(start, k-1, cp, dtype=int))
		x1 = np.insert(x1,0,x[b])
		y1 = np.insert(y1,0,y[b])
		#print(x1)
		
		#creo la curva
		nodes = np.asfortranarray([x1,y1])
		curve = bezier.Curve(nodes, degree=cp-1)
		
		#valuto la curva in k punti per poi fare il confronto con le coordinate iniziali
		s_vals = np.linspace(0.0, 1.0, k)
		x2=curve.evaluate_multi(s_vals)[0]
		y2=curve.evaluate_multi(s_vals)[1]
		
		#valuto l'errore
		a = 2 #soglia errore
		i = 0
		j = 0
		count = 0 #contatore confronti corretti
		countNeg = 0 #contatore confronti non corretti
		while i < len(x1):
			j=0
			while j < len(x2):
				if abs(x1[i]-int(x2[j])) <= a :
					if abs(int(y2[j])-y1[i]) <= a:
						x_c = np.append(x_c,[x2[j]])
						y_c = np.append(y_c,[y2[j]])
						count = count + 1
						j = len(x2)
					else:
						x_cn = np.append(x_cn,[x2[j]])
						y_cn = np.append(y_cn,[y2[j]])
						countNeg = countNeg + 1
				j += 1
			i += 1
		#print(f"ridge {id1}-{id2} cp:{cp} count:{count}/{k} -> {count*100/k}%")
		
		#calcolo match
		match = count*100/(k-start)
		if cp < 4:
			if cp+1 <= k-start and match <= 70.0:
				cp = cp + 1
			else:
				break
		else:
			if cp+4 <= k-start and match <= 70.0:
				cp = cp + 4
			else:
				break
	
	#print(f"Ridge {id1}-{id2} da {start}-{end} cp:{cp} count:{count}/{k-start} -> {count*100/(k-start)}%")	
	print(f"Da {start}-{end} cp:{cp} count:{count}/{k-start} -> {count*100/(k-start)}%")
	
	#plot delle coordinate calcolate correttamente in blu
	plt.scatter(x_c,y_c,s=10,c='blue')
					
	#plt.scatter(x_cn,y_cn,s=5,c='green')
				
	#curve.plot(k,color="green")
	
	
	#ruotare plot
	#bc=np.array([[1,0],[0,1]])
	#a=radians(90)
	#mr=array([[cos(a),sin(a)],[-sin(a),cos(a)]]) 
	#mr=dot(mr,bc)
	#X2=[] 
	#Y2=[] 
	#for j,k in zip(x,y): 
	#	p1=array([j,k]) 
	#	p2=dot(mr,p1) 
	#	X2.append(p2[0]) 
	#	Y2.append(p2[1])
	
	#plot coordinate iniziali in rosso
	plt.scatter(x,y,s=1,c='red')
	#plt.scatter(x1,y1,s=10,c='rosso')
	
	#valuto la curva in n punti
	#n = k
	#genero n punti equidistanti tra 0 e 1
	#s_vals = np.linspace(0.0, 1.0, n)
	#valuto la curva in n punti e genero n coordinate
	#più n è grande e più sarà precisa
	#x2=curve.evaluate_multi(s_vals)[0]
	#y2=curve.evaluate_multi(s_vals)[1]
	
	#plot delle coordinate calcolate
	#plt.scatter(x1,y1,s=10,c='red')	
	
	#controllo se sono alla fine
	if k == end:
		print("")
		print(f"-------- Fine del ridge: {id1}-{id2} --------")
	
	
def direction_lookup(destination_x, origin_x, destination_y, origin_y):

    deltaX = destination_x - origin_x

    deltaY = destination_y - origin_y

    degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180

    if degrees_temp < 0:

        degrees_final = 360 + degrees_temp

    else:

        degrees_final = degrees_temp

    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]

    compass_lookup = round(degrees_final / 45)

    return  degrees_final #compass_brackets[compass_lookup]#,
    
def genDir(x,y,k):
	i = 0
	direction=np.empty(shape=0, dtype=int)
	
	while i < k:
		if i > 0:
			direction = np.append(direction,[direction_lookup(x[i],x[i-1],y[i],y[i-1])])
		i = i + 1
		
	return direction	
	
def controlDir(i,k,direction,id1,id2):
	
	if direction.size == 0:
		return k
	direction[0] = direction[i]
	
	while i < k-1:
		if i > 0:
			if abs(direction[0] - direction[i]) == 180:
				#print("----Cambio di direzione -----")
				#print(f"Direzione iniziale: {direction[0]}")
				#print(f"Cambio direzione: {direction[i]}")
				#print("-----Spezzo ridge -----")
				return i+1
		i = i + 1
	return k

    

data = json.load(open("../Sourceafis/transparency_012_3_2.tif/inheritance/ridges.json"))
ridges = len(data["ridges"])

#estraggo le coordinate dei punti per ogni ridge e chiamo la funzione generateCurve
i=0
k=0
j=0
index = 0 #punto in cui spezzare il ridge
indexApp = 0
while i < ridges:#ridges
	points = len(data["ridges"][i]["pixels"])
	while k < points:
		if k == 0:
			x = np.array([data["ridges"][i]["pixels"][k]["X"]])
			y = np.array([data["ridges"][i]["pixels"][k]["Y"]])
		else:
			x = np.r_[x,[data["ridges"][i]["pixels"][k]["X"]]]
			y = np.r_[y,[data["ridges"][i]["pixels"][k]["Y"]]]
			
				
				#direction=np.empty(shape=0, dtype=int)
				#direction = np.append(direction,[direction_lookup(x[k],x[k-1],y[k],y[k-1])])
			
		k=k+1
	
	direction = genDir(x,y,k)
	index = controlDir(j,k,direction,data["ridges"][i]["ID1"],data["ridges"][i]["ID2"])
	#print(f"Inizio ridge: 0")
	#print(f"Fine ridge: {index}")
	generateCurve(x,y,k,data["ridges"][i]["ID1"],data["ridges"][i]["ID2"],0,index)
	while index != k:
		indexApp = index
		index = controlDir(index,k,direction,data["ridges"][i]["ID1"],data["ridges"][i]["ID2"])
		#print(f"Inizio ridge: {indexApp}")
		#print(f"Fine ridge: {index}")
		generateCurve(x,y,k,data["ridges"][i]["ID1"],data["ridges"][i]["ID2"],indexApp,index)
	i=i+1
	k=0
	#plt.scatter(x,y,s=1,c='green')
	


plt.xlim(0,500)
plt.ylim(0,500)

plt.show();
