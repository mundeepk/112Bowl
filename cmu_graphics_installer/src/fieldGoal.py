from cmu_graphics import *
from scoring import *
import random
import math

def fieldGoalVariables(app):
    app.kickingFieldGoal = False
    app.kickPowerChosen = False
    app.kickAngleChosen = False
    app.didKickScore = None
    app.drawKick = False
    app.finishedKickAnimation = False

    app.powerMeterX = app.width/2 - app.width/4
    app.powerMeterY = 50
    app.powerMeterWidth = app.width/2
    app.powerMeterHeight = 75
    app.redWidth = app.width/8
    app.greenWidth = 1
    app.trueGreenPosition = app.powerMeterX + app.redWidth + app.greenWidth

    app.fieldGoalPostX = 25
    app.fieldGoalPostY = 175
    app.fieldGoalSupportX = app.fieldGoalPostX - 20
    app.fieldGoalSupportY = app.fieldGoalPostY + 125

    app.angleSelectorY = 351


def drawFieldGoalSetUp(app):
        drawRect(app.powerMeterX, app.powerMeterY, app.powerMeterWidth, app.powerMeterHeight)
        drawRect(app.powerMeterX, app.powerMeterY, app.redWidth, app.powerMeterHeight, fill = 'red')
        drawRect(app.powerMeterX + app.redWidth, app.powerMeterY, app.greenWidth, app.powerMeterHeight, fill='green')
        if app.downs != 25:
            drawPolygon(app.qbX, app.qbY, app.width/12, app.qbY, app.width/12, app.qbY - 100, fill = 'green', borderWidth = 2)
            drawPolygon(app.qbX, app.qbY, app.width/12, 350, app.width/12, app.qbY, fill = 'red', borderWidth = 2)
            drawPolygon(app.qbX, app.qbY, app.width/12, 150, app.width/12, 200, fill = 'red', borderWidth = 2)
            drawLine(app.qbX, app.qbY, app.width/12, app.angleSelectorY, fill = 'blue')
        else:
            drawPolygon(365, app.qbY, app.width/12, app.qbY, app.width/12, app.qbY - 100, fill = 'green', borderWidth = 2)
            drawPolygon(365, app.qbY, app.width/12, 350, app.width/12, app.qbY, fill = 'red', borderWidth = 2)
            drawPolygon(365, app.qbY, app.width/12, 150, app.width/12, 200, fill = 'red', borderWidth = 2)
            drawLine(365, app.qbY, app.width/12, app.angleSelectorY, fill = 'blue')

def drawFieldGoalPost(app):
    drawRect(app.fieldGoalPostX, app.fieldGoalPostY, 10, 125, fill = 'yellow')   
    drawRect(app.fieldGoalSupportX, app.fieldGoalSupportY, 10, 45, fill = 'yellow')
    drawRect(app.fieldGoalSupportX - 2, app.fieldGoalSupportY + 15, 14, 30, fill = 'blue')
    drawRect(app.fieldGoalSupportX, app.fieldGoalSupportY - 10, 20, 10, fill = 'yellow') 

def drawPowerMeter(app):
    app.greenWidth += 20
    if app.greenWidth + app.powerMeterX + app.redWidth >= app.powerMeterX + app.powerMeterWidth:
        app.greenWidth = 1

def drawAngleSelector(app):
    app.angleSelectorY -= 10
    if app.angleSelectorY < 150:
        app.angleSelectorY = 350    

def drawBallGoingIntoGoal(app):
    if app.downs == 25:
        adjacentLength = distance(365, app.qbY, 25, app.qbY)
        hypotenusLength = distance(365, app.qbY, 25, app.angleSelectorY)
    else:
        adjacentLength = distance(app.qbX, app.qbY, 25, app.qbY)
        hypotenusLength = distance(app.qbX, app.qbY, 25, app.angleSelectorY)
    angle = math.acos(adjacentLength/hypotenusLength)
    app.footballX -= app.footballSpeed * math.cos(angle)
    if app.angleSelectorY > app.qbY:
        app.footballY += app.footballSpeed * math.sin(angle)
    else:
        app.footballY -= app.footballSpeed * math.sin(angle)
    if app.footballX <= 10:
        if not app.finishedKickAnimation:
            app.displayKickResult = True
            if app.downs == 4 and app.didKickScore:
                app.offensiveScore += 3
            elif app.downs == 25 and app.didKickScore:
                app.offensiveScore += 1
            else:
                app.offensiveScore += 3
                app.downs = 5
            app.finishedKickAnimation = True
   
def determineIfKickScores(app):
    app.trueGreenPosition = app.powerMeterX + app.redWidth + app.greenWidth

    if 200 <= app.angleSelectorY <= 260: #Green Angle Chosen
        if 833 <= app.trueGreenPosition <= 938: #Great Power Chosen
            app.didKickScore = True
        elif 625 <= app.trueGreenPosition <= 833: #Fair Power Chosen
            if random.random() < 0.80: app.didKickScore = True
            else: app.lastPlayResult = 'Kick Missed, not enough power!'
        else: #Poor Power Chosen
            if random.random() < 0.20: app.didKickScore = True
            else: app.lastPlayResult = 'Kick Missed, not enough power!'

    else: #Poor Angle Chosen
        app.didKickScore = False
        app.lastPlayResult = 'Kick Missed, bad angle!'
    
    if app.didKickScore != True: app.didKickScore = False
    if app.didKickScore:
        print("Scored!!!")
        app.lastPlayResult = 'Kick Scored!!!'
    else:
        print("Missed")
        
    app.drawKick = True
    app.finishedKickAnimation = False



