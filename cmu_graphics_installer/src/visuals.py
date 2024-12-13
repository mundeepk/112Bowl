from cmu_graphics import *

def drawField(app):
    drawRect(0, 0, app.tenYardIncrement, app.height, fill = 'darkGreen')
    drawRect(app.tenYardIncrement*11, 0, app.tenYardIncrement, app.height, fill = 'darkGreen')
    for i in range(1, 13):
        drawLine(app.tenYardIncrement * i, 0, app.tenYardIncrement * i, app.height, dashes = True) 