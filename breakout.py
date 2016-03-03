import pyglet
import random
from pyglet import clock
from pyglet.window import key
from Box2D import *
from itertools import chain
from view_helpers import *

class Breakout:
  def __init__(self, window):
    # Setup the world and the window
    self.world = b2World(gravity = (0,-10), doSleep=True)
    self.window = window
    self.keys = key.KeyStateHandler()
    self.window.push_handlers(self.keys)
    clock.set_fps_limit(60)

    self.drawables = []

    # Setup some physics parameters
    self.timeStep = 1.0/60
    self.vel_iters, self.pos_iters = 10, 10

    #Create the roof
    self.world.CreateStaticBody(
      position=pixelToMeter(self.window.width/2, self.window.height),
      shapes=b2PolygonShape(box=pixelToMeter(self.window.width/2, 1))
    )

    self.board = self.world.CreateKinematicBody(
        position=(15,11),
        shapes=b2PolygonShape(box=(10,1))
    )
    self.board.gravityScale = 0
    self.board.mass = 100

    # Define the ball
    body = self.world.CreateDynamicBody(
        position=(25.5,30)
      )
    body.CreatePolygonFixture(box=(1,1), density=1, friction=0.3, restitution=0.5)
    self.drawables.append(body)
    body.mass = 1
    body.angularVelocity = 1

    # Set up variables for dynamicall creating shapes
    self.tempPosList = []
    self.tempStartPos = (0,0)

  def update(self, dt):
    # Tick the physics
    self.world.Step(dt, self.vel_iters, self.pos_iters)
    self.world.ClearForces()
    board = self.board
    keys = self.keys
    # Update velocity of the board based on user input
    if keys[key.LEFT]:
      board.linearVelocity = (-20, 0)
    elif keys[key.RIGHT]:
      board.linearVelocity = (20,0)
    else:
      board.linearVelocity = (0,0)
    if keys[key.Z]:
      board.angularVelocity = 5
    elif keys[key.X]:
      board.angularVelocity = -5
    else:
      board.angularVelocity = 0

  def draw(self):
    print "draw"
    for fixture in self.board.fixtures:
      vertices = vertListToDrawTuple(fixture.shape.vertices, board.position, board.angle)
      pyglet.graphics.draw(len(vertices)/2, pyglet.gl.GL_POLYGON, ('v2f', vertices))

    for drawable in self.drawables:
      vertices = vertListToDrawTuple(drawable.fixtures[0].shape.vertices, drawable.position, drawable.angle)
      pyglet.graphics.draw(len(vertices)/2, pyglet.gl.GL_POLYGON, ('v2f', vertices))    

    for pos in self.tempPosList:
      print meterToPixel(pos[0]+tempStartPos[0], pos[1]+tempStartPos[1])
      pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2f', meterToPixel(pos[0]+tempStartPos[0], pos[1]+tempStartPos[1])))

if __name__ == "__main__":
  window = pyglet.window.Window()
  game = Breakout(window)
  clock.schedule_interval(game.update, game.timeStep)
  pyglet.app.run()

@window.event
def on_mouse_press(x, y, button, modifiers):
  global game
  tempPosList, tempStartPos, world, drawables = game.tempPosList, game.tempStartPos, game.world, game.drawables

  print("mouse")

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
  game.draw()