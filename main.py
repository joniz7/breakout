import pyglet
import random
from pyglet import clock
from pyglet.window import key
from Box2D import *
from itertools import chain
from view_helpers import *

# Setup the world and the window
world = b2World(gravity = (0,-10), doSleep=True)
window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)
clock.set_fps_limit(60)

drawables = []

# Setup some physics parameters
timeStep = 1.0/60
vel_iters, pos_iters = 10, 10

roof = world.CreateStaticBody(
  position=pixelToMeter(0, window.height),
  shapes=b2PolygonShape(box=pixelToMeter(window.width/2, 1))
  )

board = world.CreateKinematicBody(
    position=(15,11),
    shapes=b2PolygonShape(box=(10,3))
  )
board.gravityScale = 0
board.mass = 100

# Define dynamic body
body = world.CreateDynamicBody(
    position=(25.5,30)
  )
box = body.CreatePolygonFixture(box=(1,1), density=1, friction=0.3, restitution=1)
drawables.append(body)

body.mass = 1
body.angularVelocity = 1

print(board)

print window.height
print window.width

tempPosList = []
tempStartPos = (0,0)

def update(dt):
  global board
  world.Step(dt, vel_iters, pos_iters)
  world.ClearForces()

  if keys[key.LEFT]:
    board.linearVelocity = (-10, 0)
  elif keys[key.RIGHT]:
    board.linearVelocity = (10,0)
  elif keys[key.Z]:
    board.angularVelocity = 10
  elif keys[key.X]:
    board.angularVelocity = -10
  else:
    board.linearVelocity = (0,0)
    board.angularVelocity = 0

@window.event
def on_mouse_press(x, y, button, modifiers):
  global tempPosList
  global tempStartPos
  mPos = pixelToMeter(x,y)
  if button==1:
    if len(tempPosList) == 0:
      newBody = world.CreateDynamicBody(
          position=mPos
        )
      newBody.CreatePolygonFixture(box=(1,1), density=1, friction=0.3, restitution=1.0)
      drawables.append(newBody)
    else:
      newBody = world.CreateDynamicBody(
          position=tempStartPos
        )
      newBody.CreatePolygonFixture(shape=b2PolygonShape(vertices=tempPosList), density=1, friction=0.3)
      print tempPosList
      drawables.append(newBody)
      tempStartPos = (0,0)
      tempPosList = []
  elif button==4:
    if tempStartPos == (0,0):
      tempStartPos = mPos
    tempPosList.append((mPos[0]-tempStartPos[0], mPos[1]-tempStartPos[1]))

@window.event
def on_draw():
  dt = clock.tick()
  #print "FPS is %f"%clock.get_fps()
  window.clear()


  #print groundBody.position

  for fixture in board.fixtures:
    vertices = vertListToDrawTuple(fixture.shape.vertices, board.position, board.angle)
    pyglet.graphics.draw(len(vertices)/2, pyglet.gl.GL_POLYGON, ('v2f', vertices))

  for drawable in drawables:
    vertices = vertListToDrawTuple(drawable.fixtures[0].shape.vertices, drawable.position, drawable.angle)
    pyglet.graphics.draw(len(vertices)/2, pyglet.gl.GL_POLYGON, ('v2f', vertices))    

  for pos in tempPosList:
    print meterToPixel(pos[0]+tempStartPos[0], pos[1]+tempStartPos[1])
    pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2f', meterToPixel(pos[0]+tempStartPos[0], pos[1]+tempStartPos[1])))

clock.schedule_interval(update, timeStep)

pyglet.app.run()