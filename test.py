# Simulation of Michaelis-Menten kinetics
# Author: Joshua Fost PhD, joshua.fost@gmail.com
# Last modified: 26-Nov-2014

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from pylab import *

class Concept:
	def __init__(self, title='_null'):
		self.title = title
	description = "This concept has no description"
	concentration = 0

# Create concepts
e = Concept("E")
s = Concept("S")
p = Concept("P")
es = Concept("ES")

# Set initial conditions
e.concentration = .5
s.concentration = 1
es.concentration = 0
p.concentration = 0
y0 = [e.concentration, s.concentration, es.concentration, p.concentration]

# Map into standard differential form
# y0 = [E]
# y1 = [S]
# y2 = [ES]
# y3 = [P]

# Define rate constants
k_f = .3
k_r = .01
k_cat = .1

# Define Michaelis-Menten kinetics
def func(y,t):
	return [-k_f*y[0]*y[1]+(k_cat+k_r)*y[2], -k_f*y[0]*y[1]+k_r*y[2], k_f*y[0]*y[1]-k_r*y[2]-k_cat*y[2], k_cat*y[2]]

# Set time range for integration
t = np.arange(0, 60, .01)

# Integrate
y = odeint(func, y0, t)

# Output
figure()
plt.plot(t,y)
xlabel('time')
ylabel('concentration')
title('Michaelis-Menten kinetics')
show()