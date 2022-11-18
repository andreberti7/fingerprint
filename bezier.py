import numpy as np
from scipy.special import comb
import matplotlib.pyplot as plt

#matplotlib inline

# Use this to click points for Bezier curve
# Might have to run this block twice. (?)
#matplotlib osx
#plt.ion()

#polinomio di Bernstein per interpolazione
def B(i, N, t):
    val = comb(N,i) * t**i * (1.-t)**(N-i)
    return val

#plot del polinomio di Bernstein
#tt = np.linspace(0, 1, 100)
#N = 7
#for i in range(N+1):
#    plt.plot(tt, B(i, N, tt));


#curva di Bezier
def P(t, X):
    '''
     xx = P(t, X)
     
     Valuto la curva di Bezier nei punti in X.
     
     Input:
      X lista o array o coordinate 2D
      t è un numero o una lista di numeri in [0,1] dove si vuole valutare la curva di Bezier
      
     Output:
      xx insieme di punti 2D lungo la curva di Bezier
    '''
    #Crea un array dall'oggetto X
    X = np.array(X)
    #Ritorna la forma dell'array, quindi il numero dei punti e la dimensione
    N,d = np.shape(X)   # Number of points, Dimension of points
    N = N - 1
    #Creo un nuovo array con forma len(t) e tipo d popolata da zeri
    xx = np.zeros((len(t), d))

    #Calcolo xx facendo il prodotto tra due vettori
    for i in range(N+1):
        xx += np.outer(B(i, N, t), X[i])
    
    return xx

plt.figure(2, figsize=[8,8])
plt.clf()

#True -> Inserisci punti nel piano con il mouse
#False -> Prende i punti di C
clickable = True

if clickable:
    plt.plot([0,1],[0,1],'w.')
    plt.axis('equal');
    plt.draw()
    c = plt.ginput(20, mouse_stop=2) # on macbook, alt-click to stop
    plt.draw()
else: #C rappresenta i punti cioè i pixel della mia impronta
    c = [(0.09374999999999989, 0.15297619047619054),
         (0.549107142857143, 0.1648809523809524),
         (0.7083333333333335, 0.6142857142857144),
         (0.5282738095238095, 0.8940476190476193),
         (0.24404761904761907, 0.8776785714285716),
         (0.15327380952380942, 0.6321428571428573),
         (0.580357142857143, 0.08303571428571432),
         (0.8839285714285716, 0.28988095238095246)]

X = np.array(c)

tt = np.linspace(0, 1, 200)
xx = P(tt, X)

plt.plot(xx[:,0], xx[:,1])
plt.plot(X[:,0], X[:,1], 'ro')


def DrawBezier(p, n):

    x1 = p[0]
    y1 = p[1]
    x2 = p[2]
    y2 = p[3]
    x3 = p[4]
    y3 = p[5]
    x4 = p[6]
    y4 = p[7]

    t = np.linspace(0,1,n)

    xx = P(t, np.reshape(p, (4,2)))

    plt.plot([x1, x4], [y1, y4], 'ro') # knot point
    plt.plot([x1, x2], [y1, y2], 'r-') # tangent
    plt.plot([x3, x4], [y3, y4], 'r-') # tangent
    plt.plot(xx[:,0], xx[:,1], '-')                # curve


#plt.figure(3, figsize=[8,8])
#plt.clf()
#for segment in c:
#    DrawBezier(segment, 100)
#plt.axis('equal');


plt.show();




