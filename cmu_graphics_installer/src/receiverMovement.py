from footballMechanics import *
import random

#source for randomness in picking key in dictionary
#https://www.geeksforgeeks.org/python-get-random-dictionary-pair/

def runReceiverRoutes(app):
    if not app.intercepted:
        #Randomness logic citation above
        for receiver in app.players:
            randomKey = random.choice(list(app.receiverRoute.keys()))
            randomRoute = app.receiverRoute[randomKey]
            receiver.route = randomRoute
        # randomKey = random.choice(list(app.receiverRoute.keys()))
        # randomRoute = app.receiverRoute[randomKey]
        # if not app.runningTheBall:
        #     app.runningBack[0].route = randomRoute
        # app.players[0].route = app.receiverRoute['Go']
        # app.players[1].route = app.receiverRoute['Slant']
        # app.players[2].route = app.receiverRoute['In']
        if not app.playIsDead:
            getTupleDestinations(app)
            for receiver in app.players:
                receiver.iterateThroughRouteDestinations(receiver.routeDestinations)
            # if not app.runningTheBall:
            #     app.runningBack[0].iterateThroughRouteDestinations(app.runningBack[0].routeDestinations)
            # app.players[0].iterateThroughRouteDestinations(app.players[0].routeDestinations)
            # app.players[1].iterateThroughRouteDestinations(app.players[1].routeDestinations)
            # app.players[2].iterateThroughRouteDestinations(app.players[2].routeDestinations)
        else:
            for receiver in app.players:
                receiver.routeDestinations = []
            # if not app.runningTheBall:
            #     app.runningBack[0].routeDestinations = []


def getTupleDestinations(app):
    # if app.aimingBall != False:
    for receiver in app.players:
        if receiver.routeDestinations == []:
            receiver.routeDestinations.append((receiver.x, receiver.y))
        if len(receiver.routeDestinations) == 1:
            for i in range(len(receiver.route)):
                deltaX, deltaY = receiver.route[i]
                xPositionToAdd = deltaX + receiver.routeDestinations[i][0]
                yPositionToAdd = deltaY + receiver.routeDestinations[i][1]
                receiver.routeDestinations.append((xPositionToAdd, yPositionToAdd))
    # if not app.runningTheBall:
    #     if app.runningBack[0].routeDestinations == []:
    #         app.runningBack[0].routeDestinations.append((app.runningBack[0].x, app.runningBack[0].y))
    #         if len(app.runningBack[0].routeDestinations) == 1:
    #             for i in range(len(app.runningBack[0].route)):
    #                 deltaX, deltaY = app.runningBack[0].route[i]
    #                 xPositionToAdd = deltaX + app.runningBack[0].routeDestinations[i][0]
    #                 yPositionToAdd = deltaY + app.runningBack[0].routeDestinations[i][1]
    #                 app.runningBack[0].routeDestinations.append((xPositionToAdd, yPositionToAdd))


def giveBallToReceiever(app):
    app.receiverWhoCaughtTheBall[0].caughtTheBall = True
    #print(app.receiverWhoCaughtTheBall[0].x, app.receiverWhoCaughtTheBall[0].y)
    # app.footballX = app.players[2].x
    # app.fofotabllY = app.players[2].y
    app.footballX = app.receiverWhoCaughtTheBall[0].x
    app.footabllY = app.receiverWhoCaughtTheBall[0].y

def checkIfBallIsCaught(app):
    for person in app.players:
        if ((app.footballX - 17) <= person.x <= (app.footballX + 17) 
            and (app.footballY - 17) <= person.y <= (app.footballY + 17) and not app.ballIsCaught):
            app.receiverWhoCaughtTheBall.append(person)  
            app.ballIsCaught = True

            # if random.random() < 0.95:
            #     app.receiverWhoCaughtTheBall.append(person)  
            #     app.ballIsCaught = True
            #     print('caught!')
            # else:
            #     app.intercepted = True

def giveBallToRunningBack(app):
    app.runningBack[0].x -= 3
    app.footabllY = app.runningBack[0].y
    app.footballX = app.runningBack[0].x

def checkIfRunningBackClicked(app, mouseX, mouseY):
    if mouseX - 10 < app.runningBack[0].x < mouseX + 10:
        if mouseY - 10 < app.runningBack[0].y < mouseY + 10:
            app.runningTheBall = True
            app.footballX = app.runningBack[0].x
            app.footballY = app.runningBack[0].y

def resetPlayerPositions(app):
    for receiver in app.players:
            receiver.x = app.qbX 
    app.players[0].y = 200
    app.players[1].y = 450
    app.players[2].y = 550
    app.runningBack[0].x = app.qbX + 35
    app.runningBack[0].y = app.qbY + 50

def stopRouteRunning(app):
    for receiver in app.players:
        receiver.playDead = True
    
def resetReceiverAttributes(app):
    for receiver in app.players:
        receiver.playDead = False
        receiver.caughtTheBall = False    

def receiversRunToCorner(app):
    app.receiverWhoNeedsToRunToCorner.append(app.players[app.cornerWhoInterceptedTheBall[0].receiverAffiliated])
    for receiver in app.players:
        if receiver not in app.receiverWhoNeedsToRunToCorner:
            receiver.x += 2.55
    if app.receiverWhoNeedsToRunToCorner[0].x - 4 <= app.cornerWhoInterceptedTheBall[0].x <= app.receiverWhoNeedsToRunToCorner[0].x + 4:
        if app.receiverWhoNeedsToRunToCorner[0].y - 8 <= app.cornerWhoInterceptedTheBall[0].x <= app.receiverWhoNeedsToRunToCorner[0].x + 8:
            app.tackledCornerBack = True

def checkForDefensiveTackle(app):
    if app.defenderWhoNeedsToTackleReceiver[0].x - 5 <= app.receiverWhoCaughtTheBall[0].x <= app.defenderWhoNeedsToTackleReceiver[0].x + 5:
        if app.defenderWhoNeedsToTackleReceiver[0].y - 5 <= app.receiverWhoCaughtTheBall[0].y <= app.defenderWhoNeedsToTackleReceiver[0].y + 5:
            print('offensivePlayer Tackled')
            app.offensivePlayerTackled = True
            app.playIsDead = True
            app.lastPlayResult = 'Defensive Tackle'
            stopRouteRunning(app)
            if app.ballIsCaught:
                app.qbX = app.receiverWhoCaughtTheBall[0].x 
            elif app.runningTheBall:
                app.qbX = app.runningBack[0].x 
            elif app.kickingFieldGoal:
                print('kicking Fieldgoal!')