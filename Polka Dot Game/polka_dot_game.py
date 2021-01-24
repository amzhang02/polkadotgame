from graphics import *
import random
import math

makeGraphicsWindow(1440,900)

#Class for player
class Player:
    #initializer function
    def __init__(player):
        player.x = getWindowWidth()/2
        player.y = getWindowHeight()/2
        moveMouse(getWindowWidth()/2, getWindowHeight()/2)
        player.radius = 10
    
    #make the player cirle move with the mouse
    def move(player):
        (player.x, player.y) = getMousePosition()      
    
    #draw the player in light grey
    def draw(player):
        fillCircle(player.x, player.y, player.radius, "lightgrey")

#Class for other circles        
class Circle:
    #initializer function
    def __init__(circle):
        #choose random screen side and spawn circle there with randomly chosen velocity inwards
        screen_side = random.choice(["top", "bottom", "left", "right"])
        if screen_side == "top":
            circle.x = random.randint(0, getWindowWidth())
            circle.y = 0
            circle.velocityx = random.choice([-4,-3,-2,-1,1,2,3,4])
            circle.velocityy = random.choice([1,2,3,4])            
        elif screen_side == "bottom":
            circle.x = random.randint(0, getWindowWidth())
            circle.y = 900
            circle.velocityx = random.choice([-4,-3,-2,-1,1,2,3,4])
            circle.velocityy = random.choice([-4,-3,-2,-1])            
        elif screen_side == "left":
            circle.x = 0
            circle.y = random.randint(0, getWindowHeight())
            circle.velocityx = random.choice([1,2,3,4])
            circle.velocityy = random.choice([-4,-3,-2,-1,1,2,3,4])
        elif screen_side == "right":
            circle.x = 1440
            circle.y = random.randint(0, getWindowHeight())
            circle.velocityx = random.choice([-4,-3,-2,-1])
            circle.velocityy = random.choice([-4,-3,-2,-1,1,2,3,4])            
        
        #set radius to random integer between 5 and 100, inclusive of 5
        circle.radius = random.randint(5,100)
        #randomly choose circle color in this list of colors
        circle.color = random.choice(["aquamarine", "darksalmon", "gold", "lightpink", "springgreen", "yellowgreen", "sandybrown", "plum", "crimson", "deepskyblue", "indianred"])
    
    #make the circles move randomly in any direction around the screen
    def move(circle):
        circle.x = circle.x + circle.velocityx
        circle.y = circle.y + circle.velocityy
    
    #draw the circles    
    def draw(circle):
        fillCircle(circle.x, circle.y, circle.radius, circle.color)
        
#Class for bonus circles
class BonusCircle:
    #initializer function
    def __init__(bonus, x, y):
        bonus.x = random.randint(0, getWindowWidth())
        bonus.y = random.randint(0, getWindowHeight())
        bonus.radius = 10
        bonus.color = "black"
        
    #Draw bonus circle    
    def draw(bonus):
        fillCircle(bonus.x, bonus.y, bonus.radius, bonus.color)

def startWorld(world):
    #hide the mouse so it's just a circle moving where your mouse is
    hideMouse()
    
    #Background will be white
    setBackground("white")
    
    #List for all the other circles
    world.circles = []
    
    #assign circles random coordinates and random radius
    for n in range(50):
        newCircle = Circle()
        world.circles.append(newCircle)
        
    #Display instructions
    world.instructions = True
    
    #Press enter to start the game
    onKeyPress(startGame, "enter")
    
    #Game isn't over yet
    world.gameover = False
    
    #Set score to 0
    world.score = 0
    
    #Press space to restart
    onKeyPress(startWorld, "space")
    
    #Player object
    world.player = Player()
    
    #Bonus circle
    world.bonus = BonusCircle(random.randint(0, getWindowWidth()), random.randint(0, getWindowHeight()))

def startGame(world):
    #Start the game on the instructions page
    if world.instructions == True:
        world.instructions=False
        world.gameover=False        
    
def updateWorld(world):
    #hides mouse
    hideMouse()
    #If game ends, stop the game
    if world.instructions == True:
        return
    
    if world.gameover==True:
        return
    
    #Make the circles move    
    for circle in world.circles:
        circle.move()
    
    #call the move function
    world.player.move()
    
    #call the collision function
    circle_collision(world)
    

#Collisions with circles that are bigger than you
def circle_collision(world):
    #if the distance between the 2 centerpoints is less than the sum of the 2 radii, collision happens
    for circle in world.circles:
        #collision with larger circles
        if circle.radius > world.player.radius:
            if math.sqrt((world.player.x - circle.x)**2 + (world.player.y - circle.y)**2) < (circle.radius + world.player.radius):
                #your circle disappears and display game over page
                world.gameover = True
        #Collisions with smaller circles   
        elif math.sqrt((world.player.x - circle.x)**2 + (world.player.y - circle.y)**2) < (circle.radius + world.player.radius):
            #smaller circle disappears and your radius grows by a certain increment and you earn one point
            world.score = world.score + 1
            world.player.radius = world.player.radius + 1
            world.circles.remove(circle)
            newCircle = Circle()
            world.circles.append(newCircle)
            
        #make off-screen circle disappear and replace with new circle       
        if circle.x < 0 or circle.x > 1440 or circle.y < 0 or circle.y > 900:
            newCircle = Circle()
            world.circles.remove(circle)
            world.circles.append(newCircle)            
            
    #collision between player and bonus circle 
    if math.sqrt((world.player.x - world.bonus.x)**2 + (world.player.y - world.bonus.y)**2) < (world.bonus.radius + world.player.radius):
        world.score = world.score + 5
        world.player.radius = world.player.radius + 5
        world.bonus.x = random.randint(5,1435)
        world.bonus.y = random.randint(5,895)
        
            
    
def drawWorld(world):
    #Instructions
    if world.instructions == True:
        drawString("Welcome to the Polka Dot Game!", 500, 300, 40, "deeppink")
        drawString("The objective of the game is to eat as many circles smaller than you as possible", 330, 350, color="deepskyblue")
        drawString("The ball will move with your mouse", 550, 400, color="lightskyblue")
        drawString("If you hit any of the bigger circles, you die", 520, 450, color="red")
        drawString("Press enter/return to start the game. Good luck!", 490, 500, color="black")
    #Run the game if the game isn't over
    elif world.gameover == False:
        for circle in world.circles:
            circle.draw()
        world.player.draw()
        world.bonus.draw()
    #If the game is over, print message and stop game   
    if world.gameover==True:
        drawString("YOU DIED!", 600, 350, 80, "red")
        drawString("Press space to restart", 630, 400, color="black") 
        
    #Score
    drawString("Score:"+str(world.score), 1100, 20, color="red")    

runGraphics(startWorld, updateWorld, drawWorld)