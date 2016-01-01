# ---------------------------
# LIBRARIES
# ---------------------------
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# CONSTANTS
# ---------------------------
TIME_LIMIT = 100
TIME_INCREMENT = 0.1
READING_SPEED = 50.0
MINIMUM_ACTIVATION_THRESHOLD = 0.001
CONCEPT_DECAY = .95
CONCEPT_IMPULSE = 1.0

# ---------------------------
# CLASSES
# ---------------------------
class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y

  def __str__(self):
    return "{}, {}".format(self.x, self.y)

  def __neg__(self):
    return Point(-self.x, -self.y)

  def __add__(self, point):
    return Point(self.x+point.x, self.y+point.y)

  def __sub__(self, point):
    return self + -point

class Concept:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.activation = 0.0

    def __str__(self):
        return "{}: {}".format(self.name, self.activation)

    def __cmp__(self, other):
        if self.name == other.name:
            return 1
        else:
            return 0

class Datum:
    def __init__(self, concept, point):
        self.concept = concept
        self.point = point

    def __str__(self):
        return "{}: {}, {}".format(self.concept, self.point.x, self.point.y)


# ---------------------------
# FUNCTION DEFINITIONS
# ---------------------------
def read_words(file):
    with open(file) as f:
        words = f.read().split()
    f.close()
    return words

def load_concepts(file):
    with open(file) as f:
        concepts = f.read().split()
    f.close()
    return concepts

# ---------------------------
# MAIN LOGIC
# ---------------------------
# read concepts file
conceptList = []
conceptNames = []
for c in load_concepts('concepts.txt'):
    conceptList.append(Concept(c))
    conceptNames.append(c)

# read sensory input file
sensoryInput = []
sensoryInput = read_words('input.txt')
# print sensoryInput

# main loop
t = wordIndex = ticks = 0
data = []
stillRunning = True

while stillRunning:

    if (ticks % READING_SPEED) == 0:    # every READING_SPEED time steps, read another word
        if wordIndex < len(sensoryInput):
            nextWord = sensoryInput[wordIndex]
            print ("t = {}, read:{}".format(t,nextWord))
            wordIndex += 1                # increment index so reading moves to next word
        else:
            nextWord = None
        for c in conceptList:
            if c.name == nextWord:  # check if the read word is a known concept
                c.activation += CONCEPT_IMPULSE  # impulse the recognized concept

    for c in conceptList:      # passive dynamics for concept activation
        d = Datum (c.name, Point(t, c.activation))   # create data point for concept activation at this time
        data.append(d)
        if c.activation < MINIMUM_ACTIVATION_THRESHOLD:
            c.activation = 0.0
        c.activation = c.activation * CONCEPT_DECAY # exponential decay for each concept
        # print ("{} act = {}".format(c.name,c.activation))

    t += TIME_INCREMENT # read next word
    ticks += 1

    if t >= TIME_LIMIT: # if time reaches time limit
        stillRunning = False # break out of main loop

# figure 1
plotDataX = []
plotDataY = []
for d in data:
    if d.concept == "mortal":
        plotDataX.append (d.point.x)
        plotDataY.append (d.point.y)
    plt.plot(plotDataX, plotDataY)
    plt.axis([0,TIME_LIMIT,0,2.0])
plt.show()
