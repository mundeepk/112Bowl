from cmu_graphics import *
import random

def scoringVariables(app):

    app.offensiveScore = 0
    app.defensiveScore = 0
    app.offensiveTeamName = 'OFF'
    app.defensiveTeamName = 'DEF'
    app.teamWhoWon = None

def makeDefenseScore(app):
    if random.random() < 0.6: 
        app.defensiveScore += 7
    else:
        app.defensiveScore += 3
    app.downs = 1
    
def drawScoreBoard(app):
    if app.downs == 1: suffix = 'st'
    elif app.downs == 2: suffix = 'nd'
    elif app.downs == 3: suffix = 'rd'
    elif app.downs == 4: suffix = 'th'
    else: suffix = 'th'
    drawRect(0, 0, app.width, 30, fill = 'black')
    drawLabel(f'{app.offensiveTeamName}: {app.offensiveScore}', 35, 15, fill = 'white', bold = True, size = 14)
    drawLabel(f'{app.defensiveTeamName}: {app.defensiveScore}', 95, 15, fill = 'white', bold = True, size = 14)
    if app.downs <= 4:
        drawLabel(f'{app.downs}{suffix}', app.width - 25, 15, fill = 'white', bold = True, size = 14)
    if app.downs == 26: 
        drawLabel(f'Extra Point Attempt', app.width - 80, 15, fill = 'white', bold = True, size = 14)


def fieldGoalAttemptCheck(app):
    if not app.kickingFieldGoal:
        drawLabel("Press 'g' to attempt a field goal, or play on 4th down! ", app.width/2, 15, size = 18, fill = 'white')
   

def checkIfOffensivePlayerScored(app):
    if app.ballIsCaught:
        if app.receiverWhoCaughtTheBall[0].x <= app.width/12:
            app.offensiveScore += 6
            app.offenseScored = True
            app.ballIsCaught = False
            app.downs = 25
    if app.runningTheBall:
        if app.runningBack[0].x <= app.width/12:
            app.offensiveScore += 6
            app.offenseScored = True
            app.runningTheBall = False
            app.downs = 25
    if app.offenseScored and app.drawKick == False:
        app.footballX = 325
        app.footballY = app.qbY

def checkWinner(app):
    if app.offensiveScore >= 112:
        app.teamWhoWon = app.offensiveTeamName
    elif app.defensiveScore >= 112:
        app.teamWhoWon = app.defensiveTeamName
    
        