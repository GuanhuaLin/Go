# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 21:55:24 2021

@author: LIN03
"""

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

image = Image.open('img_wood.png')

ar = np.array(image)
plt.imshow(ar)
plt.show()
ar[:,:,3] = 175
#new = np.zeros((70,70,4))

'''
new[34:36,:36]=[0,0,0,1]
new[:,34:36]=[0,0,0,1]
'''
'''
for i in range(70):
    for j in range(70):
        d2 = (i-34.5)**2+(j-34.5)**2
        if d2 <= 26.5**2:
            new[i,j] = [0,0,0,1]
        elif d2 <= 28.5**2:
            new[i,j] = [0,0,0,1]
        else:
            new[i,j] = [0,0,0,0] # transparent
'''      

plt.imshow(ar)
plt.show()
plt.imsave('img_wood2.png',ar)
