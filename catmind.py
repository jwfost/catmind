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

# define constants
DEFAULT_INTRINSIC_ENERGY = 0.1
A = 0.3			# pre-exponential constant
R = 1.0			# gas constant
T = 1.0			# temperature
T_MAX = 60		# end point for simulation
T_INC = 0.1		# time increment

# Returns the probability that concepts i and j will be bound together
# in the same gamma circuit.
def gamma_probability(i,j):
	return 0.99

class Concept:
	def __init__(self, name='(null)', parts=[]):
		self.name = name
		self.description = "No description"
		self.concentration = 0
		self.intrinsic_energy = DEFAULT_INTRINSIC_ENERGY
		self.energy = self.intrinsic_energy
		self.parts = []
		self.parts.extend(parts)
	def calc_energy(self):
		if len(self.parts) == 0:
			self.energy = self.intrinsic_energy
		elif len(self.parts) >= 2:
			energy_of_parts = 0
			for part in self.parts:
				energy_of_parts += part.calc_energy() - np.log2(gamma_probability(self,part))
			self.energy = energy_of_parts
		return self.energy

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
state0 = [e.concentration, s.concentration, es.concentration, p.concentration]

# Define rate constants
# Defaults: k_f = 0.3, k_r = 0.01, k_cat = 0.1
es_E = float(es.calc_energy())
s_E = float(s.calc_energy())
e_E = float(e.calc_energy())
p_E = float(p.calc_energy())
k_f = A * exp(-(es_E - (e_E + s_E))/(R*T))
k_r = A * exp(-((e_E + s_E) - es_E)/(R*T))
k_cat = A * exp(-((e_E + p_E) - es_E)/(R*T))

# Define Michaelis-Menten kinetics
def func(state,t):
	# unpack the state vector
	e = state[0]
	s = state[1]
	es = state[2]
	p = state[3]

	# compute state derivatives
	# the '_d' means "dot," as in "derivative."
	e_d = -k_f * e * s + (k_cat + k_r) * es
	s_d = -k_f * e * s + k_r * es
	es_d = k_f * e * s - k_r * es - k_cat * es
	p_d = k_cat * es

	# return the state derivatives
	return [e_d, s_d, es_d, p_d]

# Set time range for integration
t = np.arange(0, T_MAX, T_INC)

# Integrate
y = odeint(func, state0, t)

# Output
figure()
plt.plot(t,y)
xlabel('time')
ylabel('concentration')
title('Michaelis-Menten kinetics')
show()

# More output
# print "Concept ES has %d parts" % len(es.parts)
for c in [e,s,es,p]:
	print "%s.energy = %.3f" % (c.name,c.energy)
