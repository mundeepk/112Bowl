from cmu_graphics import *
from receiverMovement import *
import math

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def moveFootballLinearly(app):
    adjacentLength = distance(app.qbX, app.qbY, app.qbThrowLandX, app.qbY)
    hypotenusLength = distance(app.qbX, app.qbY, app.qbThrowLandX, app.qbThrowLandY)
    angle = math.acos(adjacentLength/hypotenusLength)
    app.footballX -= app.footballSpeed * math.cos(angle)
    if app.qbThrowLandY > app.qbY:
        app.footballY += app.footballSpeed * math.sin(angle)
    else:
        app.footballY -= app.footballSpeed * math.sin(angle)
    if app.footballX == app.qbThrowLandX and app.footballY == app.qbThrowLandY:
        app.ballIsDropped = True







