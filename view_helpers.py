pixelPerMeter = 10.0
from itertools import chain
from math import sin, cos

def vertListToDrawTuple(vertices, pos, angle):
  for i, v in enumerate(vertices):
    vertices[i] = ((v[0]*cos(angle)-(v[1]*sin(angle))+pos[0])*pixelPerMeter, ((v[0]*sin(angle)+v[1]*cos(angle)+pos[1])*pixelPerMeter))
  return tuple(list(chain(*vertices)))

def pixelToMeter(*pos):
  return (pos[0]/pixelPerMeter, pos[1]/pixelPerMeter)

def meterToPixel(*pos):
  return (pos[0]*pixelPerMeter, pos[1]*pixelPerMeter)