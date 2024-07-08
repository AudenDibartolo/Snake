import random
import math
app.direction = 0
app.stepsPerSecond = 3

#determine how big you want each cell to be by changing scale ex: a scale of 80 will result in each cell being 80x80#
scale = 40
numOfCells = int(math.floor(400/scale))

#makes the grid#
grid = []
def rowMaker(row):
    column = 0
    for i in range(numOfCells):
        grid.append(Rect(column, row, scale, scale, fill = 'white', border = 'black', borderWidth = .5))
        column += scale

def gridMaker():
    for i in range(numOfCells):
        rowMaker(i*scale)
gridMaker()

#dictionary to keep track of what is in each cell#
gridColors = {}
for cell in grid:
    gridColors[(cell.centerX, cell.centerY)] = 'white'
    
#apple eaten counter#
app.score = Label(0, 200, 20, size = 30)
app.score.toFront()

#make the snake body#
snakeBody = []
def bodyMaker(xadd, yadd):
    if len(snakeBody) == 0:
        snakeBody.append(Rect(snakeHead[1].centerX + xadd, snakeHead[1].centerY + yadd, scale, scale, fill = 'green', border = 'black', borderWidth = 1))
    else:
        snakeBody.append(Rect(snakeBody[-1].centerX + xadd, snakeBody[-1].centerY + yadd, scale, scale, fill = 'green', border = 'black', borderWidth = 1))


#list that holds all apples#
apples = []

def appleMaker():
    selectedGrid = grid[random.randint(0,int(400/scale)**2)-1]
    if gridColors[selectedGrid.centerX, selectedGrid.centerY] == 'white':
        apples.append([
            Circle(selectedGrid.centerX, selectedGrid.centerY, scale/3.2, fill = 'crimson'),
            Oval(selectedGrid.centerX + scale/12, selectedGrid.centerY - scale/3.5, scale/2.8, 
            scale/6, fill = 'limeGreen', rotateAngle = 300),
            Oval(selectedGrid.centerX - scale/12 , selectedGrid.centerY - scale/4, scale/3.4, 
            scale/6.3, fill = 'limeGreen', rotateAngle = 45)
            ])
    else:
        appleMaker()
        quit()
    
#make three initial apples, once on is eaten a new one will be generated#    
appleMaker()
appleMaker()
appleMaker()


#snake head#
snakeHead = [Oval((scale *4), 3.5*scale, scale -10, (scale-10)/2, fill = 'paleVioletRed'), 
Rect(int(scale*3), int(scale*3), scale, scale, fill = 'green', borderWidth = 1, border = 'black'), 
Circle(3.75*scale, 3.25*scale, scale/12), Circle(3.75*scale, 3.75*scale, scale/12)]

#helper function to move features of the snake (eyes and tongue)  when the player changes direction#
def featureHelper(toungePosRot, toungePosX, toungePosY, direc1, direc2, direc3, direc4):
    snakeHead[0].rotateAngle = toungePosRot
    snakeHead[0].centerX = toungePosX
    snakeHead[0].centerY = toungePosY
    snakeHead[2].centerX = snakeHead[1].centerX + direc1
    snakeHead[2].centerY = snakeHead[1].centerY + direc2
    snakeHead[3].centerX = snakeHead[1].centerX + direc3
    snakeHead[3].centerY = snakeHead[1].centerY + direc4
    
#calling helper function to move features when player changes direction#
direcScale = scale/4
def featureMover(direction):
    if direction == 'up' and app.direction != 1:
        featureHelper(90, snakeHead[1].centerX, snakeHead[1].top, direcScale, -direcScale, -direcScale, -direcScale)
        
        
    if direction == 'down' and app.direction != 3:
        featureHelper(90, snakeHead[1].centerX, snakeHead[1].bottom, -direcScale, direcScale, direcScale, direcScale)
        
        
    if direction == 'right' and app.direction != 2:
        featureHelper(0, snakeHead[1].right, snakeHead[1].centerY, direcScale, -direcScale, direcScale, direcScale)
        
        
    if direction == 'left' and app.direction != 0:
        featureHelper(0, snakeHead[1].left, snakeHead[1].centerY, -direcScale, direcScale, -direcScale, -direcScale)
        
        

#change the position of the head based on directional user input#
def onKeyPress(key):

    if key == 'w':
        featureMover('up')
        app.direction = 3

    elif key == 'd':
        featureMover('right')
        app.direction = 0

    elif key == 's':
        featureMover('down')
        app.direction = 1

    elif key == 'a':
        featureMover('left')
        app.direction = 2

#function that places the fail screen over the screen when the snake runs into itself or the wall#
def failScreen():
    Rect(0, 0, 400, 400, fill = 'red')
    Label("Your Snake Tied Itself Into a Knot", 200, 180, size = 20)
    Label("Press Run to Try Again", 200, 230, size = 20)
    for part in snakeHead:
        part.visible = False
    snakeBody.clear()
    
#fucntion to detect if the snake hits itself#
def hitDetection():
    if gridColors[snakeHead[1].centerX, snakeHead[1].centerY] == 'green':
        #display fail screen#
        failScreen()
            
#function that provides the illusion of the snake moving. Only the tail is deleted, the head is moved in whichever direction, and a new body piece is added behind the head#            
def snakeBodyMover():
    #move snake body parts with head#
    if len(snakeBody) > 0:
        gridColors[snakeBody[-1].centerX, snakeBody[-1].centerY] = 'white'
        snakeBody[-1].visible = False
        snakeBody.remove(snakeBody[-1])
        gridColors[snakeHead[1].centerX, snakeHead[1].centerY] = 'green'
        snakeBody.insert(0, Rect(snakeHead[1].left, snakeHead[1].top, scale, scale, fill = 'green', border = 'black', borderWidth = 1))
        
#function to move the head of the snake forward#        
def snakeHeadMover():
    #snakeHead movement#
    for part in snakeHead:
        if app.direction == 0:
            part.centerX += scale
        elif app.direction == 1:
            part.centerY += scale
        elif app.direction == 2:
            part.centerX -= scale
        elif app.direction ==3:
            part.centerY -= scale
            
            
#function to determine if the snakehead has run into a apple. if so, remove the apple, increase the score, make a new apple, and add a new body piece on to the end of the snake#            
def appleCollision(pointX, pointY):
    for apple in apples:
        if apple[0].contains(pointX, pointY):
            apples.remove(apple)
            for part in apple:
                part.visible = False
            appleMaker()
            app.score.value += 1
            
            if app.direction == 0:
                bodyMaker(-scale/2, 0)
                
            if app.direction == 1:
                bodyMaker(0, scale/2)
                
            if app.direction == 2:
                bodyMaker(scale/2, 0)
             
            if app.direction == 3:
                bodyMaker(0, scale/2)

#function that determines if the head of the snake has reached the end of the screen. If so, end the game with the fail screen# 
def wallCollision():
    if snakeHead[1].centerX > numOfCells*scale:
        failScreen()
        snakeHead[1].left = 0
        
    if snakeHead[1].centerX < 0:
        failScreen()
        snakeHead[1].right = scale*numOfCells
        
    if snakeHead[1].centerY > numOfCells*scale:
        failScreen()
        snakeHead[1].top = 0
        
    if snakeHead[1].centerY < 0:
        failScreen()
        snakeHead[1].bottom = numOfCells*scale

def onStep():
    
    appleCollision(snakeHead[1].centerX, snakeHead[1].centerY)
    
    #hit detection#
    hitDetection()
         
    #move snake body parts with head#
    snakeBodyMover()

    #snakeHead movement#
    snakeHeadMover()
    
    #wall collision check#
    wallCollision()
