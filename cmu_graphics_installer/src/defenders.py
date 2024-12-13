from Athlete import *
import random

def makeCornerBacks(app):
    for i in range(len(app.players)):
        createdCorner = Athlete((app.players[i].x-25), app.players[i].y)
        createdCorner.receiverAffiliated = i
        createdCorner.isCorner = True
        app.cornerBacks.append(createdCorner)
    # for i in range(len(app.runningBack)):
    #     createdDefensiveBack = Athlete((app.runningBack[i].x-80), app.runningBack[i].y)
    #     app.defensiveBacks.append(createdDefensiveBack)

def runCornerBackDefense(app):
    if not app.playIsDead:
        for i in range(len(app.cornerBacks)):
            if app.cornerBacks[i] in app.defenderWhoNeedsToTackleReceiver:
                if app.cornerBacks[i].y == app.receiverWhoCaughtTheBall[0].y: 
                    app.cornerBacks[i].y -= 2
                app.cornerBacks[i].isCornerDefending = True
                app.cornerBacks[i].routeDestinations = [(app.cornerBacks[i].x, app.cornerBacks[i].y), 
                                                        (app.receiverWhoCaughtTheBall[0].x, app.receiverWhoCaughtTheBall[0].y)]
                if app.footballX >= app.cornerBacks[i].x:
                    app.cornerBacks[i].isFootBallBehind = True
                elif app.footballX < app.cornerBacks[i].x:
                    app.cornerBacks[i].isFootballBehind = False
            else:
                app.cornerBacks[i].routeDestinations = app.players[i].routeDestinations
            # for j in range(len(app.cornerBacks[i].routeDestinations)):
            #     app.cornerBacks[i].routeDestinations
        # app.defensiveBacks[0].routeDestinations = [(app.defensiveBacks[0].x, app.defensiveBacks[0].y), 
        #                                                 (app.runningBack[0].x, app.runningBack[0].y)]
        for i in range(len(app.cornerBacks)):
        #     # if app.players[i].caughtTheBall:
        #         # app.cornerBacks[i].isCornerDefending = True
            app.cornerBacks[i].iterateThroughRouteDestinations(app.cornerBacks[i].routeDestinations)
        # app.defensiveBacks[0].iterateThroughRouteDestinations(app.defensiveBacks[0].routeDestinations)
        #     # print(f'{i}, {app.players[i].playDead}, CB {app.cornerBacks[i].playDead}')


    # app.cornerBacks[0].routeDestinations = app.players[0].routeDestinations
    # app.cornerBacks[1].routeDestinations = app.players[1].routeDestinations
    # app.cornerBacks[2].routeDestinations = app.players[2].routeDestinations
# def runCornerBackDefense(app):
#     for cB in app.cornerBacks:
#         # randomScaleFactor = [-3, -2, -1, 0, 1, 2, 3]
#         # random1 = random.random()
#         # random2 = random.random()
#         # random.choice(randomScaleFactor)
#         # - 20 + random.choice(randomScaleFactor)
#         cB.x = app.players[cB.receiverAffiliated].x - 20
#         cB.y = app.players[cB.receiverAffiliated].y  
#         if cB.y > 585 or cB.y < 35:
#             cB.x -= 3
#         if cB.x < 5:
#             cB.x = 5 
#     for dB in app.defensiveBacks:

#         dB.x = app.runningBack[0].x - 20
#         dB.y = app.runningBack[0].y 
#         if dB.y > 585 or dB.y < 35:
#             cB.x -= 3
#         if dB.x < 5:
#             cB.x = 5 

def checkIfBallIsIntercepted(app):
    for cB in app.cornerBacks:
        if ((app.footballX - 13) <= cB.x <= (app.footballX + 13) 
            and (app.footballY - 13) <= cB.y <= (app.footballY + 13) and not app.ballIsCaught):
            app.intercepted = True
            app.ballIsDropped = True
            app.cornerWhoInterceptedTheBall.append(cB)