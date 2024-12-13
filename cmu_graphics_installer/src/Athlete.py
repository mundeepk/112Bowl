from cmu_graphics import *
import math
import random

class Athlete:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.route = []
        self.routeDestinations = []
        self.caughtTheBall = False
        self.playDead = False
        self.receiverAffiliated = None
        self.isCornerDefending = False
        self.isCorner = False
        self.isFootballBehind = True

    def __repr__(self):
        print(self.x, self.y)
    
    def isGoingOffScreen(self):
        self.speed = 3.5 if self.isCorner else 2.5
        if self.y > 590 or self.y < 5 or self.caughtTheBall: 
            self.x -= self.speed
        if self.x < 5:
            self.x = 5      

    def iterateThroughRouteDestinations(self, routeDestinations):
        if self.isCorner:
            self.speed = random.choice([0.5, 1.5, 2.5, 3, 3.25, 4, 5])
        else: self.speed = 3

        if self.playDead:
            self.routeDestinations = []
        if self.y > 585 or self.y < 35 or self.caughtTheBall: 
            if not self.playDead:
                self.x -= self.speed
                if self.x < 5:
                    self.x = 5   
        else:
            if len(routeDestinations) == 2:
                if self.isCorner:
                    if self.isCorner:
                        self.speed = random.choice([0.5, 1.5, 2.5, 3, 3.25, 4, 5])
                    if self.isCornerDefending:
                        if self.isFootballBehind == True:
                            self.speed = random.choice([0.5, 1.5, 2.5])
                        else:
                            self.speed = random.choice([3.4, 3.5, 3.75, 4])
                hypotenusLength = distance(routeDestinations[0][0], routeDestinations[0][1],
                                            routeDestinations[1][0], routeDestinations[1][1])
                adjacentLength = distance(routeDestinations[0][0], routeDestinations[0][1],
                                            routeDestinations[1][0], routeDestinations[0][1])
                angle = math.acos(adjacentLength/hypotenusLength)
                if not self.playDead:
                    self.x -= self.speed * math.cos(angle)
                if routeDestinations[1][1]> routeDestinations[0][1]:
                    if not self.playDead:
                        self.y += (self.speed) * math.sin(angle) 
                else:
                    if not self.playDead:
                        self.y -= (self.speed) * math.sin(angle)
                self.isGoingOffScreen()
            else:
                for i in range(len(routeDestinations) - 1):
                    tempRouteDestinations = routeDestinations[0:2]
                    if self.x > routeDestinations[1][0]:
                        self.iterateThroughRouteDestinations(tempRouteDestinations)
                    else:
                        self.routeDestinations.pop(0)




