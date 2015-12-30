# Simulation of Michaelis-Menten kinetics
# with explicit rate constant calculation
# Author: Joshua Fost PhD, joshua.fost@gmail.com
# Last modified: 27-Nov-2014

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from pylab import *

# Returns the probability that concepts i and j will be bound together
# in the same gamma circuit. 
def gammaProbability(i,j):
	return 0.95

class Concept:
	def __init__(self, name='(null)', parts=[]):
		self.name = name
		self.description = "No description"
		self.concentration = 0
		self.intrinsicEnergy = 0.1
		self.energy = self.intrinsicEnergy
		self.parts = []
		self.parts.extend(parts)
	def calcEnergy(self):
		energyOfParts = 0
		for x in self.parts:
			# intrinsic energy of each individual part
			x.calcEnergy
			energyOfParts += x.energy   
			# bond energy associated with self's relationship to that part
			energyOfParts += -np.log2(gammaProbability(self,x))
		self.energy = self.intrinsicEnergy + energyOfParts

# Create concepts
e = Concept("E")
s = Concept("S")
p = Concept("P")
es = Concept("ES",[e,s])

# Set initial conditions
e.concentration = .5
s.concentration = 1
es.concentration = 0
p.concentration = 0
y0 = [e.concentration, s.concentration, es.concentration, p.concentration]

# Update energy
concepts = [e,s,es,p]
for c in concepts:
	c.calcEnergy()

# Map into standard differential form
# y0 = [E]
# y1 = [S]
# y2 = [ES]
# y3 = [P]

# Define rate constants
# Defaults: k_f = 0.3, k_r = 0.01, k_cat = 0.1
A = 1.0
R = 1.0
T = 1.0
k_f = A * exp(-(es.energy - (e.energy + s.energy))/(R*T))
k_r = A * exp(-((e.energy + s.energy) - es.energy)/(R*T))
k_cat = A * exp(-((e.energy + p.energy) - es.energy)/(R*T))

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

# More output
print "Concept ES has %d parts" % len(es.parts)
for c in concepts:
	print "%s.energy = %.3f" % (c.name,c.energy)

