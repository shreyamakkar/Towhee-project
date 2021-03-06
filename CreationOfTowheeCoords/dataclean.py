# -*- coding: utf-8 -*-
"""dataclean.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17GyeqcSGDZqisukjP1_Ypsnuezl-y31h
"""

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import math

data = pd.read_csv("data.txt", sep="              ",names = ["element", "xyz"])

from google.colab import drive
drive.mount('/content/drive')

data_new = data.loc[0:408:3]

data_new=data_new.drop(['element'], axis = 1)

data_new.to_csv("data_new.csv", index = False, header = False)

data_coords = pd.read_csv("data_new.csv", sep='    ', names = ['x', 'y', 'z'])

data_coords

coords = data_coords.to_numpy()
hull = ConvexHull(coords)
hullpoints = coords[hull.vertices, :]
hdist = cdist(hullpoints, hullpoints, metric = 'euclidean')
bestpair = np.unravel_index(hdist.argmax(), hdist.shape)

print([hullpoints[bestpair[0]], hullpoints[bestpair[1]]])
print(bestpair)

less_data = pd.read_csv("data.txt", sep="              ",names = ["element", "xyz"])
less_data= less_data.drop(['element'], axis = 1)
less_data.to_csv("less_data.csv", index = False, header = False)
less_data_coords = pd.read_csv("less_data.csv", sep='    ', names = ['x', 'y', 'z'])

#for each point in data, add 7 more points
multiplier1 = np.matrix('-1, 0, 0; 0, 1, 0; 0, 0, 1')
multiplier2 = np.matrix('1, 0, 0; 0, -1, 0; 0, 0, 1')
multiplier3 = np.matrix('1, 0, 0; 0, 1, 0; 0, 0, -1')

less_coords = less_data_coords.to_numpy()

new_coords = np.matmul(less_coords, multiplier1)

less_coords = np.append(less_coords, new_coords, axis =0)

new_coords = np.matmul(less_coords, multiplier2)
less_coords = np.append(less_coords, new_coords, axis =0)

new_coords = np.matmul(less_coords, multiplier3)
less_coords = np.append(less_coords, new_coords, axis =0)

less_coords.shape

l_coords = less_coords#.to_numpy()
hull = ConvexHull(l_coords)
hullpoints = l_coords[hull.vertices, :]
hdist = cdist(hullpoints, hullpoints, metric = 'euclidean')
bestpair = np.unravel_index(hdist.argmin(), hdist.shape)

print([hullpoints[bestpair[0]], hullpoints[bestpair[1]]])
print(bestpair)

l_coords = less_coords#.to_numpy()
hull = ConvexHull(l_coords)
hullpoints = l_coords[hull.vertices, :]
hdist = cdist(hullpoints, hullpoints, metric = 'euclidean')
bestpair = np.unravel_index(hdist.argmax(), hdist.shape)

print([hullpoints[bestpair[0]], hullpoints[bestpair[1]]])
print(bestpair)

less_coords

oxygen = less_coords[0:3264:3]
oxygen = pd.DataFrame(oxygen, columns = ['x', 'y', 'z'])
xOw= oxygen.loc[:, "x"]
yOw=oxygen.loc[:, "y"]
zOw=oxygen.loc[:, "z"]

hydrogen1 = less_coords[1:3264:3]
hydrogen1 = pd.DataFrame(hydrogen1, columns = ['x', 'y', 'z'])
xH1= hydrogen1.loc[:, "x"]
yH1= hydrogen1.loc[:, "y"]
zH1= hydrogen1.loc[:, "z"]

hydrogen2 = less_coords[2:3264:3]
hydrogen2 = pd.DataFrame(hydrogen2, columns = ['x', 'y', 'z'])
xH2= hydrogen2.loc[:, "x"]
yH2= hydrogen2.loc[:, "y"]
zH2= hydrogen2.loc[:, "z"]

rOH = 0.9572
rOM = 0.1546 #TIP4P2005 0.1577; TIP4P-Ice
angleHOH = 104.52*math.pi/180.0 #radians 
cosHOH2 = math.cos(0.5*angleHOH)
a = rOM/(rOH*cosHOH2)
b = 1-a

def setCoordsM(i):
  x1= (b*xOw[i]+a*xH1[i])/(a+b)
  y1= (b*yOw[i]+a*yH1[i])/(a+b) 
  z1= (b*zOw[i]+a*zH1[i])/(a+b) 
  x2= (b*xOw[i]+a*xH2[i])/(a+b) 
  y2= (b*yOw[i]+a*yH2[i])/(a+b) 
  z2= (b*zOw[i]+a*zH2[i])/(a+b) 

  xM = np.zeros(408) ; yM = np.zeros(408) ; zM = np.zeros(408)
  xM[i] = 0.5*(x1+x2) 
  yM[i] = 0.5*(y1+y2) 
  zM[i] = 0.5*(z1+z2) 

  return xM[i], yM[i], zM[i]

new_coords = pd.DataFrame(columns = ['x', 'y', 'z'])
Mcoords = []
for i in range(407):
  #take x,y,zOw x,y,zH1 x,y,zH2 to get x,y,zM
  Mcoords= [setCoordsM(i)[0], setCoordsM(i)[1], setCoordsM(i)[2]]
  #append oxygen[i], hydrogen1[i], hydrogen2[i], M[i] to coords
  row = pd.Series({'x': xOw[i], 'y': yOw[i], 'z': zOw[i]}, name = 'O')
  new_coords = new_coords.append(row)
  row = pd.Series({'x': xH1[i], 'y': yH1[i], 'z': zH1[i]}, name = 'H')
  new_coords = new_coords.append(row)
  row = pd.Series({'x': xH2[i], 'y': yH2[i], 'z': zH2[i]}, name = 'H')
  new_coords = new_coords.append(row)
  row = pd.Series({'x': Mcoords[0], 'y': Mcoords[1], 'z': Mcoords[2]}, name = 'M')
  new_coords = new_coords.append(row)

new_coords

new_coords['index']=new_coords.index

new_coords.to_csv("new_coords.csv", index = False, header = False)

import csv

reader = csv.reader(open("new_coords.csv", "rU"), delimiter=',')
writer = csv.writer(open("output.txt", 'w'), delimiter=' ')
writer.writerows(reader)

print("Delimiter successfully changed")