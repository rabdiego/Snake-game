# Importing modules
import pygame
import random

# Creating the canvas
SIZE = 600
display = pygame.display.set_mode((SIZE, SIZE))
background = pygame.image.load('background.png').convert_alpha()
GRID = 15

# Importing the labels
scoreLabel = pygame.image.load('score.png').convert_alpha()
gameOverLabel = pygame.image.load('gameover.png').convert_alpha()

clock = pygame.time.Clock() # Creating the game clock

# Initializing the fonts
pygame.font.init()
scoreFont = pygame.font.SysFont('ccredalertlan', 25)
gameOverFont = pygame.font.SysFont('ccredalertlan', 75)
highScoreFont = pygame.font.SysFont('ccredalertlan', 30)

WHITE = (255,255,255) # Creating the white color

# Importing sounds
pygame.mixer.init()

music = pygame.mixer.music.load('snakesong.wav')
pygame.mixer.music.play(-1)

appleSfx = pygame.mixer.Sound('applesfx.wav')

# Creating the Snake class
class Snake():
    def __init__(self):
        self.x = 0 # X-axis position
        self.y = 0 # Y-axis position
        self.velX = SIZE/GRID # X-axis velocity
        self.velY = 0 # Y-axis velocity
        self.rects = [0] # This array will contain the number of the snake's body parts

        # self.positions will contain the positions (x, y) the first body part had been.
        # I noticed that every body part is just the first one (I'll call it the head)
        # but in a delayed frame, for instance, the second body part is an one-delayed-frame
        # head, the third is a two-delayed-frame and so on. Inside the Snake().run() function
        # I will explain it with more details how it works.
        self.positions = [[self.x, self.y]]

        # Importing the snake's sprites
        self.headUp = pygame.image.load('snake_head_up.png').convert_alpha()
        self.headDown = pygame.image.load('snake_head_down.png').convert_alpha()
        self.headRight = pygame.image.load('snake_head_right.png').convert_alpha()
        self.headLeft = pygame.image.load('snake_head_left.png').convert_alpha()

        self.body = pygame.image.load('snake_body.png').convert_alpha()


    def restart(self):
        self.x = 0
        self.y = 0
        self.velX = SIZE/GRID
        self.velY = 0
        self.rects = [0]
        self.positions = [[self.x, self.y]]
        # This function bring back the snake to its initial position, while restarting the
        # self.rects to 1 element.


    def pause(self):
        self.velX = 0
        self.velY = 0
        # This function is used when the game over screen is displayed to pause the snake and avoid
        # it eating the apple and modifying the score.


    def run(self):
        global running, display
        self.x += self.velX # Will add the X-axis velocity to the position
        self.y += self.velY # Will add the Y-axis velocity to the position
        self.positions.append([self.x, self.y]) # Will append the position the head is in that moment
        
        # This area will draw the snake's body parts
        for index in range(len(self.rects)): # Will draw each body part according to the lenght of self.rects
            i = len(self.positions) - index - 1 # Just to simplificate
            if index == 0:
                if self.velX > 0:
                    display.blit(self.headRight, (self.positions[i][0], self.positions[i][1]))
                if self.velX < 0:
                    display.blit(self.headLeft, (self.positions[i][0], self.positions[i][1]))
                if self.velY > 0:
                    display.blit(self.headDown, (self.positions[i][0], self.positions[i][1]))
                if self.velY < 0:
                    display.blit(self.headUp, (self.positions[i][0], self.positions[i][1]))
            else:
                display.blit(self.body, (self.positions[i][0], self.positions[i][1]))

        # This area will delete all the unused positions.
        for position in range(len(self.positions)):
            if len(self.positions) - len(self.rects) > position:
                self.positions.pop(position)

        
    # This function will verify if one element in self.positions is duplicate,
    # so it means that one body part is touching another, or if the snake hit
    # the wall. And them return a True value
    # indicating that the snake is dead.
    def isDead(self):
        if any(self.positions.count(element) > 1 for element in self.positions):
            return True
        
        if self.x >= SIZE:
            return True
        if self.x < 0:
            return True
        if self.y >= SIZE:
            return True
        if self.y < 0:
            return True


    def add(self): # It will add a value to self.rects, so the number of body parts is increased. It will be used when the snake eat an apple.
        self.rects.append(0)
    

    # This section is used to move the player.
    def up(self):
        self.velX, self.velY = 0, -(SIZE/GRID)
    def down(self):
        self.velX, self.velY = 0, (SIZE/GRID)
    def right(self):
        self.velX, self.velY = (SIZE/GRID), 0
    def left(self):
        self.velX, self.velY = -(SIZE/GRID), 0


class Food(): # Creating the food class
    def __init__(self):
        self.LENGHT = 30 # Apple size
        self.x = random.randint(1, 9) * (SIZE/GRID) # Randomizing the X-axis position
        self.y = random.randint(1, 9) * (SIZE/GRID) # Randomizing the Y-axis position

        # Note: the snake game run in a grid-system layout, here the apple will randomize it position
        # Between 1 and 19, but it will be multiplicate by 30 to fit into the screen. Note that the snake
        # Don't need it, as it velocity is an multiple of 30, and the initial position too.

        self.sprite = pygame.image.load('apple.png').convert_alpha()
    

    def restart(self): # Will randomize it position when the snake eat it
        self.x = random.randint(1, 9) * (SIZE/GRID)
        self.y = random.randint(1, 9) * (SIZE/GRID)
    

    def draw(self): # Will draw the apple on the screen
        global display
        display.blit(self.sprite, (self.x, self.y))


def wasEaten(snake, food): # Will check if the snake eat the apple
    if snake.x == food.x and snake.y == food.y: # Check if the head position is equal to the apple position
        # This try-except part is used to guarantee that the apple won't generate in the same position one snake
        # body part is. 
        while True:
            try:
                food.restart()
                assert [food.x, food.y] not in snake.positions
                snake.add()
                break
            except:
                pass
        appleSfx.play()


def gameOver(snake, food): # Will check if the snake is dead
    global isGameOver, display
    if snake.isDead():
        isGameOver = True # Then the isGameOver variable will return True
    if isGameOver:
        snake.pause() # The snake will pause

        # Display the final score
        display.blit(gameOverLabel, (50, 206))
        gameOverScore = gameOverFont.render(f'Score: {len(player.rects)}', True, WHITE)

        # Check if the player got a new highscore
        with open('highscore.txt', 'r') as highScoreData:
            highScore = int(highScoreData.read())
            if len(player.rects) > highScore:
                with open('highscore.txt', 'w') as highScoreData:
                    highScoreData.write(f'{len(player.rects)}')
        highScoreData.close()

        highScoreText = highScoreFont.render(f'High score: {highScore}', True, WHITE) # Display the highscore

        # Display the text
        display.blit(gameOverScore, (166, 266))
        display.blit(highScoreText, (204, 346))


player = Snake() # player variable
apple = Food() # apple variable
isGameOver = False # isGameOver variable

running = True
while running:
    for event in pygame.event.get():
        # Quit the game
        if event.type == pygame.QUIT:
            running = False
        # The commands. WASD to move and spacebar to restart when the game is over.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.up()
            if event.key == pygame.K_s:
                player.down()
            if event.key == pygame.K_d:
                player.right()
            if event.key == pygame.K_a:
                player.left()
            if event.key == pygame.K_SPACE:
                if isGameOver == True:
                    player.restart()
                    apple.restart()
                    isGameOver = False

    display.blit(background, (0, 0)) # Display the background

    # The functions being activated.
    apple.draw()
    player.run()
    wasEaten(player, apple)
    gameOver(player, apple)

    # Display the score in real time
    display.blit(scoreLabel, (480, 545))
    score = scoreFont.render(f'{len(player.rects)}', True, WHITE)
    display.blit(score, (530, 550))

    clock.tick(9) # 10fps is a good velocity to me.
    pygame.display.update() # Update the display.
