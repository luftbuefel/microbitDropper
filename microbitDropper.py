from microbit import *
from random import *
import music

movable = True
playerPosition = 2
maxPlayerX = 4
minPlayerX = 0
fallingLightPosition = 0
fallingLightRow = 0
EMPTY_ROW = "00000:"
dropDelay = 50
playerLife = 9
lightShowing = False
gameOver = False
lightMovementTimer = dropDelay
score = 0

def spawnLight():
    global lightShowing
    global fallingLightRow
    global fallingLightPosition
    lightShowing = True
    fallingLightRow = 0
    fallingLightPosition = randint(0,4)
    return

def moveLight():
    global fallingLightRow
    global lightMovementTimer
    global dropDelay
    fallingLightRow+=1
    lightMovementTimer = dropDelay
    return
    
def moveRight():
    global playerPosition
    global maxPlayerX
    if playerPosition < maxPlayerX:
        playerPosition+=1
    return

def moveLeft():
    global playerPosition
    global minPlayerX
    if playerPosition > minPlayerX:
        playerPosition-=1
    return
    
def redrawScreen():
    global playerPosition
    global lightMovementTimer
    #check if we need to spawn a falling light
    if lightShowing is False:
        spawnLight()
    #draw the falling light
    if(lightMovementTimer<=0):
        moveLight()
    else:
        lightMovementTimer-=1
   
    screenContents=""
    for row in range(0,4):
        if(fallingLightRow == row):
            nextRow = EMPTY_ROW[:fallingLightPosition] +"9" +EMPTY_ROW[fallingLightPosition:]
        else:
            nextRow = EMPTY_ROW
        screenContents+=nextRow
    #update the player position
    lastRow = "00000"
    lastRow = lastRow[:playerPosition] + str(playerLife) + lastRow[playerPosition:]
    screenContents+=lastRow
    #draw the falling light
    display.show(Image(screenContents))
    return    
    
def checkForCatch():
    global fallingLightRow
    global fallingLightPosition
    global playerPosition
    global playerLife
    global gameOver
    global score
    global dropDelay
    if(fallingLightRow==4):
       if(fallingLightPosition==playerPosition):
           #gameOver = True
           #player caughdet the light
           #speed up the drops for ever two points earned
           if score%2 is 0:
               dropDelay-=5
           #display.scroll("You win")
           spawnLight()
           music.play(music.BA_DING)
           score+=1
       else:
           #dim the playerLife
           playerLife-=3
           #playerLife is not working properly, I need to add a switch for changing the number of lives the player has left
           if(playerLife<=0):
               #out of life, game over
               gameOver = True
               music.play(music.POWER_DOWN)
               display.show(Image.SKULL)
               sleep(1000)
               display.scroll("Score: "+str(score))
       #the light has hit the bottom so change the flag so another light will spawn
       lightShowing = False
    return
    
def update():
    global movable
    global gameOver
    if gameOver is False:
        #get buttonA input
        if button_a.is_pressed() and movable is True:
            movable = False
            moveLeft()
        elif button_b.is_pressed() and movable is True:
            movable = False
            moveRight()
        if not button_a.is_pressed() and not button_b.is_pressed():
            movable = True
        
        redrawScreen()
        checkForCatch()
    return
    
while True:
    update()
