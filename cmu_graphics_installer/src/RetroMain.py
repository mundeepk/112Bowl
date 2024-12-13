from cmu_graphics import *
from Athlete import *
from receiverMovement import *
from fieldGoal import *
from scoring import *
from visuals import *
from footballMechanics import *
from defenders import *
from scoring import *
import math
import random
import time

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5
    
def onAppStart(app): 
    fullGameReset(app)

def fullGameReset(app):
    app.gameFrozen = False
    app.width = 1250
    app.height = 600
    app.stepsPerSecond = 30
    app.receiverRoute = {'Go': [(-300, 0)],
                        'Slant': [(-100, 0), (-50, 100)],
                        'SlantOther': [(-100,0), (50, 100)],
                        'In': [(-25, 0), (-25, 0)],
                        'InOther': [(-50, 0), (50, 0)],
                        'Post': [(-100, 0), (-200, 300)]
                        }
    app.lastPlayResult = None

    scoringVariables(app)
    resetDowns(app)
    resetVariables(app)
    resetPlay(app)

def resetDowns(app):
    app.downs = 1
    app.offenseScored = False

def resetVariables(app):

    app.tenYardIncrement = app.width/12
    app.players = [Athlete(885, 200), Athlete(885, 450), Athlete(885, 550)]
    app.runningBack = [Athlete(920, app.height/2 + 30)]
    app.qbX = app.width - 3.5 * app.tenYardIncrement
    app.qbY = app.height/2
    app.ballIsDropped = False
    app.ballDropMessageDisplayed = False
    app.footballSpeed = 10

def resetPlay(app):
    fieldGoalVariables(app)

    app.cornerBacks = []
    app.gamePaused = False
    app.defensiveBacks = []
    makeCornerBacks(app)
    app.counter = 0
    app.paused = False
    app.footballPaused = False
    app.receiverWhoCaughtTheBall = []
    app.defenderWhoNeedsToTackleReceiver = []
    app.cornerWhoInterceptedTheBall = []
    app.receiverWhoNeedsToRunToCorner = []
    app.displayKickResult = False

    app.receieverRouteDestinations = []
    #app.currentReceiverRoutePart = app.receiverRoute[0]
    app.theta = 0
    app.receiverXMovement = -3
    app.receiverYMovement = 0
    
    app.qbThrowX = app.qbX
    app.qbThrowY = app.qbY
    app.qbThrowLandX = app.qbX - 10
    app.qbThrowLandY = app.qbY 
    app.qbThrowLandYMidPoint = app.qbY + (app.qbY - app.qbThrowLandY)/2 
    app.qbThrowLandXMidPoint = app.qbX + (app.qbX - app.qbThrowLandX)/2
    app.archX = app.qbX - app.qbThrowLandX
    app.archY = app.qbY - app.qbThrowLandY
    app.archRadius = 1
    app.aimingBall = None
    app.gameStarted = True
    app.footballX, app.footballY = app.qbX, app.qbY
    app.ballIsCaught = False
    app.runningTheBall = False
    app.intercepted = False
    app.playIsDead = True
    app.tackledCornerBack = False
    app.offensivePlayerTackled = False
    app.ballIsReleased = False

    resetReceiverAttributes(app)
       
def onMouseHover(app, mouseX, mouseY):
    if app.gameStarted:
        app.aimingBall = False
    # app.footballY = app.runningBack[0].x

def onMouseRelease(app, mouseX, mouseY):
    app.aimingBall = False
    app.ballIsReleased = True

def onMouseDrag(app, mouseX, mouseY): 
    if not app.ballIsReleased:
        app.gameStarted = False
        app.playIsDead = False
        app.aimingBall = True
        if app.aimingBall:
            app.qbThrowX = mouseX
            app.qbThrowY = mouseY
            app.qbThrowLandX = app.qbX - (app.qbThrowX - app.qbX)
            app.qbThrowLandY = app.qbY - (app.qbThrowY - app.qbY)
            app.qbThrowLandYMidPoint = app.qbThrowLandY + (app.qbY - app.qbThrowLandY)/2 
            app.qbThrowLandXMidPoint = app.qbThrowLandX + (app.qbX - app.qbThrowLandX)/2
            app.archX = app.qbX - (app.qbThrowX - app.qbX)/2
            app.archY = app.qbY - (app.qbThrowY - app.qbY) / 2
            app.archRadius = distance(app.qbX, app.qbY, app.qbThrowLandX, app.qbThrowLandY)/2

# def getThetaFromGiven(app):
#         radianAngle = math.acos(distance(app.qbThrowLandXMidPoint, app.qbThrowLandYMidPoint, 
#                                   app.qbX, app.qbThrowLandYMidPoint)/
#                         distance(app.qbThrowLandXMidPoint, app.qbThrowLandYMidPoint,
#                                  app.qbX, app.qbY))
#         finalAngleInDegrees = radianAngle * (180/math.pi)
#         return finalAngleInDegrees

def redrawAll(app):
    
    drawField(app)
    drawScoreBoard(app)

    if app.offenseScored:
        drawLabel("TOUCHDOWN!!! Make the extra point! Press 'k' to select your power and 'a' for your angle ", app.width/2, 15, size = 18, fill = 'white')
    if app.kickingFieldGoal and app.downs != 25 and not app.finishedKickAnimation:
        drawLabel("Press 'k' to select your power, and 'a' for your angle", app.width/2, 15, size = 18, fill = 'white')
    if app.finishedKickAnimation:
        drawLabel(f'{app.lastPlayResult}', app.width/2, 15, size = 18, fill = 'white')

    if not app.kickingFieldGoal:
        if app.gameStarted and app.downs != 4:
            if app.downs == 1 and app.lastPlayResult == 'Tackled the Corner Back!':
                drawLabel(f'You tackled the cornerback! The defense only got 3 points! Now lead the offense!', app.width/2, 15, size = 18, fill = 'white')
            elif app.downs == 1:
                drawLabel('Drag your mouse from the QB start the play and aim; release to throw the ball! Click the RB to run!', 
                    app.width/2, 15, size = 18, fill = 'white')
        if app.aimingBall:
            drawLabel('Throw to a receiver!', app.width/2, 15, size = 18, fill = 'white')
        if not app.playIsDead and not app.aimingBall and not app.intercepted:
            drawLabel('Will the receiver catch it?', app.width/2, 15, size = 18, fill = 'white')
        if not app.aimingBall and app.playIsDead:
            if app.downs == 2 or app.downs == 3:
                if app.lastPlayResult == 'Drop':
                    drawLabel('The ball was dropped! This play will be better!', app.width/2, 15, size = 18, fill = 'white')
        if app.intercepted:
            drawLabel(f'{app.lastPlayResult}', app.width/2, 15, size = 18, fill = 'white')
            drawLabel('Use the arrow keys to chase the corner down before they score!', app.width/2, 50, size = 16)
        if app.ballIsCaught:
            drawLabel('Caught! Use the arrow keys to score!', app.width/2, 50, size = 16)
            # drawLabel("Press 't' to simulate a defensive tackle", app.width/2, 65, size = 16)
            
        drawRect(app.players[0].x, app.players[0].y, 15, 15, fill = 'blue')
        drawRect(app.players[1].x, app.players[1].y, 15, 15, fill = 'purple')
        drawRect(app.players[2].x, app.players[2].y, 15, 15, fill = 'orange')

        drawRect(app.qbX + 10, app.qbY, 20, 20, fill = 'pink', align = 'center')
        drawLabel('QB', app.qbX + 10, app.qbY, fill = 'black')
        # for person in app.players:
        #     drawRect(person.x, person.y, 10, 10, fill = 'blue')

        for cB in app.cornerBacks:
            drawRect(cB.x, cB.y, 15, 15, fill = 'red')
        
        # for dB in app.defensiveBacks:
        #     drawRect(dB.x, dB.y, 15, 15, fill = 'red')

        # drawRect(app.runningBack[0].x, app.runningBack[0].y, 10, 10)
        if app.aimingBall and not app.ballIsReleased:
            drawLine(app.qbX, app.qbY, app.qbThrowLandX, app.qbThrowLandY, fill = 'red')

        if not app.aimingBall and not app.gameStarted or app.runningTheBall and not app.ballIsDropped:
            drawCircle(app.footballX, app.footballY, 10, fill = 'brown', rotateAngle = 20)
    
    if app.teamWhoWon != None:
        drawLabel(f'{app.teamWhoWon} won!!!', app.width/2, app.height/2, size = 50)
        drawLabel(f"Press 'r' to play again!", app.width/2, app.height/2 + 50, size = 15)

    if app.downs == 4 and app.playIsDead:
        fieldGoalAttemptCheck(app)

    if app.kickingFieldGoal:
        drawFieldGoalSetUp(app)

    drawFieldGoalPost(app)

    if app.drawKick:
        drawCircle(app.footballX, app.footballY, 10, fill = 'brown', rotateAngle = 20)

def takeStep(app):
    if app.kickingFieldGoal and not app.kickPowerChosen:
        drawPowerMeter(app)
    if app.kickingFieldGoal and app.kickPowerChosen and not app.kickAngleChosen:
        drawAngleSelector(app)
    if app.kickPowerChosen and app.kickAngleChosen and app.didKickScore == None:
        determineIfKickScores(app)
    if app.drawKick:
        drawBallGoingIntoGoal(app)
        
    runReceiverRoutes(app)

    if not app.aimingBall and not app.gameStarted and not app.footballPaused and not app.ballIsDropped:
        if not app.ballIsCaught and not app.runningTheBall:
            moveFootballLinearly(app)
            if app.footballX <= app.qbThrowLandX:
                if not app.ballIsCaught:
                    app.ballIsDropped = True

    if app.ballIsCaught:
        app.lastPlayResult = "Caught"
        giveBallToReceiever(app)
        for cB in app.cornerBacks:
            if app.receiverWhoCaughtTheBall[0] == app.players[cB.receiverAffiliated]:
                app.defenderWhoNeedsToTackleReceiver.append(cB)
        checkForDefensiveTackle(app)
        if app.offensivePlayerTackled and not app.kickingFieldGoal:
            print('304')
            app.downs += 1
            resetPlayerPositions(app)
            resetPlay(app)
            app.ballIsDropped = False
    if not app.offenseScored:
        checkIfBallIsIntercepted(app)

    if not app.intercepted:
        runCornerBackDefense(app)
       

    if app.intercepted:
        if not app.tackledCornerBack:
            app.lastPlayResult = 'Intercepted!'
            if app.cornerWhoInterceptedTheBall[0].x < app.width - 10:
                app.cornerWhoInterceptedTheBall[0].x += 2
                app.footballX = app.cornerWhoInterceptedTheBall[0].x
                app.footballY = app.cornerWhoInterceptedTheBall[0].y
                receiversRunToCorner(app)
                for cB in app.cornerBacks:
                    if cB not in app.cornerWhoInterceptedTheBall:
                        cB.x += 2.5
        elif app.tackledCornerBack:
            app.lastPlayResult = 'Tackled the Corner Back!'
            app.defensiveScore += 3
            resetDowns(app)
            resetVariables(app)
            resetPlay(app)
        else:
            makeDefenseScore(app)
            resetDowns(app)
            resetVariables(app)
            resetPlay(app)

    if not app.intercepted and not app.ballIsDropped:
        checkIfBallIsCaught(app)

    checkIfOffensivePlayerScored(app)
    
    checkWinner(app)
    
    if app.offenseScored:
        app.kickingFieldGoal = True


    if app.ballIsDropped and not app.intercepted:
        app.playIsDead = True
        app.lastPlayResult = 'Drop'
        stopRouteRunning(app)
        if app.ballIsCaught:
            app.qbX = app.receiverWhoCaughtTheBall[0].x 
        elif app.runningTheBall:
            app.qbX = app.runningBack[0].x 
        elif app.kickingFieldGoal:
            print('kicking Fieldgoal!')
        else:
            print('ball dropped!')
        if not app.kickingFieldGoal:
            print('304')
            app.downs += 1
            resetPlayerPositions(app)
            resetPlay(app)
            app.ballIsDropped = False
       

    if app.kickingFieldGoal and (app.downs == 4 or app.downs == 25): 
        if app.finishedKickAnimation:
            # print('line 326')
            makeDefenseScore(app)
            resetDowns(app)
            resetVariables(app)
            resetPlay(app)
    if app.downs == 5:
        print('line 332')
        makeDefenseScore(app)
        resetDowns(app)
        resetVariables(app)
        resetPlay(app)

    if app.runningTheBall or app.paused and not app.intercepted:
        app.runningBack[0].x -= 3
        app.footabllY = app.runningBack[0].y
        app.footballX = app.runningBack[0].x

def onStep(app):
    if not app.gamePaused:
        if not app.gameFrozen:
            takeStep(app)

def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    if key == 'f':
        app.footballPaused = not app.footballPaused
    if key == 'r':
        scoringVariables(app)
        resetDowns(app)
        resetVariables(app)
        resetPlay(app)
    if key == 't':
        app.playIsDead = True
        stopRouteRunning(app)
        if app.ballIsCaught:
            app.qbX = app.receiverWhoCaughtTheBall[0].x 
        elif app.runningTheBall:
            app.qbX = app.runningBack[0].x 
        else:
            print('play is live!')

        if not app.kickingFieldGoal:
            resetPlayerPositions(app)
            resetPlay(app)
            app.downs += 1
            print('386')
            app.ballIsDropped = False
        
    if key == 'g':
        app.kickingFieldGoal = not app.kickingFieldGoal
    if key == 'k':
        app.kickPowerChosen = True
    if key == 'a':
        app.kickAngleChosen = True
    if key == 'w':
        app.offensiveScore = 112

def onMousePress(app, mouseX, mouseY):
    pass

def onKeyHold(app, keys):
    if app.ballIsCaught:
        receiverWhoCaughtTheBall = app.receiverWhoCaughtTheBall[0]
        if 'down' in keys: 
            receiverWhoCaughtTheBall.y += 3
        if 'up' in keys:
            receiverWhoCaughtTheBall.y -= 3

        if 'right' in keys:
            receiverWhoCaughtTheBall.x += 3
        app.footballY = receiverWhoCaughtTheBall.y
    elif app.runningTheBall:
        runningBackWithTheBall = app.runningBack[0]
        if 'down' in keys: 
            runningBackWithTheBall.y += 3
        if 'up' in keys:
            runningBackWithTheBall.y -= 3
       
        if 'right' in keys:
            runningBackWithTheBall.x += 3
        app.footballX = runningBackWithTheBall.x
        app.footballY = runningBackWithTheBall.y
    if app.intercepted:
        if 'down' in keys: 
            app.receiverWhoNeedsToRunToCorner[0].y += 3
        if 'up' in keys:
            app.receiverWhoNeedsToRunToCorner[0].y -= 3
        if 'left' in keys:
            app.receiverWhoNeedsToRunToCorner[0].x -= 3
        if 'right' in keys:
            app.receiverWhoNeedsToRunToCorner[0].x += 5
        

runApp()