import numpy as np

# constants
AROUSAL = 1.0   # Analogy to temperature in Micahelis-Menten kinetics
R = 1.0
A = 1.0


class Concept:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.activation = 0.0
        self.R = []


# read input file
input = ["socrates is man","man is mortal","#modusponens"]

# main loop
while (true):
    # pick random elements from input to focus attention
    spotlight = []
    spotlight.append(input[0],input[1],input[2])

    # calculate binding energy for all possible 2- and (ultimately) 3-concept compounds
    for c1 in np.nditer(spotlight):
        for c2 in np.nditer(spotlight):
            if (c1 != c2):
                # calculate binding energy for c1-c2 compound
                E = -np.log2(probFromMemory(c1,c2))
                # calcuate k of the forward reaction
                k = A * np.exp(-E/(R*AROUSAL))
                #


mp = Concept("#modusponens","Modus Ponens")
# Dictionary object to store all catalytic relations.
# Maps concepts onto concepts.
#   If [P] then [Q] <-- Evoked concept. Micky reads it, activation bump, expo decay.
#   [P] <-- Same thing

cp = Concept("#conditional","Conditional")
# Matches anything of the forms:
#   - If [P] then [Q]
#   - If [x] is [F] then [x] is [G]
#   - All [x] are [y]
# If Micky reads such a form in perceptual stream, new instance of Conditional, activation bump, expo decay

a = Concept("Assertion")
# Matches anything of the form:
#   - [x] is [F]

# Note: give Micky an initial page of text as input, but let him write on it too, so that his intermediate output can become a later input. Extended mind.
