# Name: Nima Dehkordi
# Date: January 27th 2020
# Project Description: Simple 2-D shooter where the spaceship has to live as long as possible.

# import libraries
import random
import pygame

# initialize pygame
pygame.init()
# initialize pygame sounds
pygame.mixer.init()
# plays background music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
# variables for screen width and height
width = 500
height = 700
# initialize screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ALEC")
# Use clock to make sure game doesn't drop below FPS variable during main game loop.
clock = pygame.time.Clock()
FPS = 30
# Make varibles for color RGB profiles
green = ((0, 255, 0))
red = ((255, 0, 0))
black = ((0, 0, 0))
# initialize game variables
# difficulty variable changes the speed of the asteroids.
difficulty = 1
# variable defines whether the player is shooting 3 lasers at a time
shotgun_shot = False
# alive is the boolean that keeps the main loop running
alive = True
# initialize fonts
font = pygame.font.SysFont('Comic Sans MS', 30)
Titlefont = pygame.font.Font('AmazDooMRight2.ttf', 250)
# score variable keeps track of players score
score = 0
# health variable keeps track of players health and checks if it dips below 0.
health = 100
# variable used for boss' health and to track the damage player has done to it
boss_health = 200
# variable used to keep track of events that only happen when boss is spawned, like whether the player damages it or not
boss_spawned = False
# used as a timer
frames = 0
# keep track of players high score and find their highest score through txt file
highscores = open('highscores.txt', 'r')
highscore = 0
# read through each line of the txt file to find the highscore by using max function
for num in highscores.readlines():
    highscore = max(highscore, int(num))
# initialize sounds
boss_sound = pygame.mixer.Sound('boss_spawn.wav')
boss_sound.set_volume(1)
boss_death_sound = pygame.mixer.Sound('yay.wav')
boss_death_sound.set_volume(1)
dmg = pygame.mixer.Sound('damage.wav')
powerUp = pygame.mixer.Sound('powerup.wav')

# initialize images
player_img = pygame.image.load('spaceship.png')
boss_img = pygame.image.load('boss.png')
boss_img = pygame.transform.scale(boss_img, (80, 80))
boss_img = pygame.transform.flip(boss_img, False, True)
sheild_img = pygame.image.load('sheild.png')
sheild_img = pygame.transform.scale(sheild_img, (15, 15))
gun_img = pygame.image.load('gun.png')
gun_img = pygame.transform.scale(gun_img, (15, 15))
rock_img = pygame.image.load('rock.png')
laser_img = pygame.image.load('laser.png')
laser_img = pygame.transform.scale(laser_img, (10, 20))
background = pygame.image.load('background.png')


# Sprites
# all sprites are classes that are initialized with an image and rectangle.

# player sprite
class Player(pygame.sprite.Sprite):
    global shotgun_shot

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # set image
        self.image = pygame.transform.scale(player_img, (60, 40))
        # make hurtbox the rectangle from the image
        self.rect = self.image.get_rect()
        # position the sprite
        self.rect.centerx = width / 2
        self.rect.centery = 650
        # set speed variables
        self.speedx = 0
        self.speedy = 0

    # resets player to original spawn position
    def reset(self):
        self.rect.centerx = width / 2
        self.rect.centery = 650

    # update function
    def update(self):
        self.speedx = 0
        self.speedy = 0
        # find key player pressed
        pressedkey = pygame.key.get_pressed()
        # Change sprite speed by determining what key the player pressed.
        if pressedkey[pygame.K_RIGHT]:
            # make x value positive so the player moves right
            self.speedx = 5
        if pressedkey[pygame.K_LEFT]:
            # make x value negative so player moves left
            self.speedx = -5
        if pressedkey[pygame.K_UP]:
            # make y value negative so player moves up
            self.speedy = -5
        if pressedkey[pygame.K_DOWN]:
            # make y value positive so player goes down.
            self.speedy = 5
        # Change player rectangle by the speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # conditional statements for boundaries
        if self.rect.right > width:
            # check if player moves past the right of the screen and move them back
            self.rect.right = width
        if self.rect.left < 0:
            # check if player moves past the left of the screen and move them back
            self.rect.left = 0
        if self.rect.top < 0:
            # check if player moves past the top of the screen and move them back
            self.rect.top = 0
        if self.rect.bottom > height:
            # check if player moves past the bottom of the screen and move them back
            self.rect.bottom = height

    # function that makes the player shoots laser
    def shoot(self):
        #play laser sound effect
        laser_sound = pygame.mixer.Sound('laser.mp3')
        laser_sound.set_volume(0.5)
        laser_sound.play()
        # check if player has shotgun powerup on
        if shotgun_shot:
            # create 3 different laser that are spread out from eachother, and add them to sprite lists
            laser1 = Laser(self.rect.centerx - 20, self.rect.y, 1)
            all_sprites.add(laser1)
            lasers.add(laser1)
            laser2 = Laser(self.rect.centerx + 20, self.rect.y, 1)
            all_sprites.add(laser2)
            lasers.add(laser2)
            laser3 = Laser(self.rect.centerx, self.rect.y, 1)
            all_sprites.add(laser3)
            lasers.add(laser3)
        else:
            #fire laser from the center of the spaceship by creating a laser sprite in that position
            laser = Laser(self.rect.centerx, self.rect.y, 1)
            #add laser to sprite groups
            all_sprites.add(laser)
            lasers.add(laser)

# Asteriod sprite
class Asteroid(pygame.sprite.Sprite):
    #define global variable of difficulty
    global difficulty

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # scale image to random sizes for random sized asteroids
        self.image = pygame.transform.scale(rock_img, (30 * random.randint(1, 3), 30 * random.randint(1, 3)))
        # get hurtbox from image
        self.rect = self.image.get_rect()
        # asteroid spawns at random x position at the top of the screen
        self.rect.x = random.randint(0, width)
        self.rect.y = random.randint(-120, -50)
        # y speed is random, and scales up with difficulty
        self.speedy = random.randrange(1 + difficulty, 9 + difficulty)
        # x speed is random
        self.speedx = random.randrange(-3, 3)

    def update(self):
        # move asteroid position based on speeds
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # check if asteroid moves past the screen
        if self.rect.y > 735 or self.rect.left < -30 or self.rect.right > width + 30:
            # move back to the top of the screen
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(-120, -50)
            self.speedy = random.randrange(1 + difficulty, 9 + difficulty)

# Laser sprite
class Laser(pygame.sprite.Sprite):
    def __init__(self, shipx, shipy, dir):
        pygame.sprite.Sprite.__init__(self)
        # define the image used
        self.image = laser_img
        # get hurtbox from image
        self.rect = self.image.get_rect()
        # set constant speed to the direction the laser is going to
        self.speedy = -15 * dir
        # set the position of the laser on the center of the ship
        self.rect.centerx = shipx
        self.rect.bottom = shipy

    def update(self):
        # update the laser by changing the y
        self.rect.y += self.speedy

# Boss Sprite
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # set boss image
        self.image = boss_img
        # set hurtbox by getting rectangle from boss image
        self.rect = self.image.get_rect()
        # set position
        self.rect.centerx = width / 2
        self.rect.centery = -80
        # initialize horizontal speed
        self.xspeed = 5

    def update(self):
        # makes the boss move from side to side. The conditional statement checks if the boss bas hits the sides of the screen.
        if self.rect.centerx > width - 80 or self.rect.centerx < 80:
            # changes x speed direction to move the the opposite way
            self.xspeed = self.xspeed * - 1
        # changes sprite x position
        self.rect.x += self.xspeed

    def spawn(self):
        # play sound when boss spawns
        boss_sound.play()
        # loop that moves boss in middle
        while True:
            self.rect.y += 1
            if self.rect.y == 175:
                # break loop when boss is in position
                break

    def despawn(self):
        # play sound when boss dies
        boss_death_sound.play()
        # loop that moves boss back to top of screen
        while True:
            self.rect.y -= 1
            if self.rect.y == -100:
                #loop breaks when boss is done
                break
    # function that draws the boss' health bar
    def healthbar(self):
        # draws the rectangle behind the full health in red
        pygame.draw.rect(screen, red, (self.rect.x - 40, self.rect.y - 15, 200, 10))
        # draws a rectangle that has a length according to the boss' current health
        pygame.draw.rect(screen, green, (self.rect.x - 40, self.rect.y - 15, boss_health // (score // 1000), 10))

    # function that makes boss shoot
    def shoot(self):
        # sound effect plays when function called
        laser_sound = pygame.mixer.Sound('laser.wav')
        laser_sound.set_volume(0.5)
        laser_sound.play()
        # make 3 laser sprites, position them, and add them to sprite groups
        laser1 = Laser(self.rect.centerx, self.rect.centery, -1)
        laser2 = Laser(self.rect.centerx - 30, self.rect.centery, -1)
        laser3 = Laser(self.rect.centerx + 30, self.rect.centery, -1)
        all_sprites.add(laser1, laser2, laser3)
        boss_lasers.add(laser1, laser2, laser3)

# sheild sprite
class Sheild(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # get image and rectangle from image
        self.image = sheild_img
        self.rect = self.image.get_rect()
        # spawn the powerup on a random x axis on the top of the screen
        self.rect.centerx = random.randrange(1, width)
        self.rect.centery = -30
        # set the y speed
        self.yspeed = 5
    # update function
    def update(self):
        # move the powerup down the screen by adding the yspeed
        self.rect.y += self.yspeed
        # kill the powerup when it is off screen
        if self.rect.top > height:
            self.kill()

# Shot gun sprite
# functions just the same as shield sprite, just has a different image
class Shotgun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = gun_img
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(1, width)
        self.rect.centery = -30
        self.yspeed = 5

    def update(self):
        self.rect.y += self.yspeed
        if self.rect.top > height:
            self.kill()

# starting screen function
def startScreen():
    # loop boolean
    running = True
    # main loop
    while running:
        # check events
        for event in pygame.event.get():
            # if the player clicks their mouse or the keyboard, the game starts
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                # making the main loop boolean false stops the loop
                running = False
        # draw the title screen
        # fill screen
        screen.fill(black)
        # title text
        titleText = Titlefont.render('ALEC', False, (51, 5, 235))
        # format title text
        titleText_rect = titleText.get_rect(center=(width / 2, 180))
        # draw title text
        screen.blit(titleText, titleText_rect)
        # highscore text
        highscoreTrack = font.render('Your Highscore is: ' + str(highscore), False, (200, 200, 200))
        # format highscore text
        highscoreTrack_rect = highscoreTrack.get_rect(center=(width / 2, (height / 2) + 50))
        # draw highscore text
        screen.blit(highscoreTrack, highscoreTrack_rect)
        # make sub text variable
        subText = font.render('Click or press a key to start', False, (200, 200, 200))
        # format and position sub text variable
        subText_rect = subText.get_rect(center=(width / 2, height / 2))
        # draw sub text
        screen.blit(subText, subText_rect)
        # make sub text variable
        subText = font.render('Use arrow keys to move', False, (200, 200, 200))
        # format and position sub text variable
        subText_rect = subText.get_rect(center=(width / 2, (height / 2) +120))
        # draw sub text
        screen.blit(subText, subText_rect)
        # make sub text variable
        subText = font.render('and spacebar to shoot', False, (200, 200, 200))
        # format and position sub text variable
        subText_rect = subText.get_rect(center=(width / 2, (height / 2) + 170))
        # draw sub text
        screen.blit(subText, subText_rect)
        # make sub text variable
        subText = font.render('Survive as long as possible', False, (200, 200, 200))
        # format and position sub text variable
        subText_rect = subText.get_rect(center=(width / 2, (height / 2) + 220))
        # draw sub text
        screen.blit(subText, subText_rect)
        # make sub text variable
        subText = font.render("Made By Nima Dehkordi", False, (200, 200, 200))
        # format and position sub text variable
        subText_rect = subText.get_rect(center=(width / 2, height -30))
        # draw sub text
        screen.blit(subText, subText_rect)
        # flip display
        pygame.display.flip()

# call start screen
startScreen()

# game over function
def gameOver():
    # get global variables to reset game
    global alive, score, health, boss_health, boss_spawned, frames, player, boss, shotgun_shot, difficulty
    # despawn boss
    if boss_spawned:
        boss.despawn()
    # make main loop boolean variable
    running = True
    # write the current highscore in a txt file to access later
    with open('highscores.txt', 'a') as highscores:
        highscores.write('\n' + str(highscore))
    # main loop
    while running:
        # draw losing screen
        screen.fill(black)
        # create and draw the title text
        titleText1 = Titlefont.render('GAME', False, (255, 0, 0))
        titleText_rect1 = titleText1.get_rect(center=(width / 2, 150))
        screen.blit(titleText1, titleText_rect1)
        # title text split in 2 sections
        titleText2 = Titlefont.render('Over', False, (255, 0, 0))
        titleText_rect2 = titleText2.get_rect(center=(width / 2, 350))
        screen.blit(titleText2, titleText_rect2)
        # create and draw highscore text
        highscoreTrack = font.render('Your Highscore is: ' + str(highscore), False, (200, 200, 200))
        highscoreTrack_rect = highscoreTrack.get_rect(center=(width / 2, 450))
        screen.blit(highscoreTrack, highscoreTrack_rect)
        # create and draw sub texxt
        subText = font.render('Click or press a key to play again', False, (200, 200, 200))
        subText_rect = subText.get_rect(center=(width / 2, 550))
        screen.blit(subText, subText_rect)
        subText1 = font.render('Press X to leave', False, (200, 200, 200))
        subText_rect1 = subText1.get_rect(center=(width / 2, 650))
        screen.blit(subText1, subText_rect1)
        # event loop
        for event in pygame.event.get():
            # wait 5 seconds before checking to check accidental clicks
            pygame.time.wait(1500)
            # checks if player clicks x
            if event.type == pygame.K_x:
                # stop running the main loop and game loop
                running = False
                alive = False
            # check if player clicks anything else
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                # reset game variables and sprite locations
                running = False
                alive = True
                player.rect.centerx = width / 2
                player.rect.centery = -80
                score = 0
                difficulty = 1
                health = 100
                boss_health = 200
                boss_spawned = False
                frames = 0
                shotgun_shot = False
                player.reset()
        # flip display
        pygame.display.flip()

# initialize sprite groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
lasers = pygame.sprite.Group()
boss_lasers = pygame.sprite.Group()
# initialize sprites
player = Player()
# add to sprite group
all_sprites.add(player)
boss = Boss()
# add to sprite group
all_sprites.add(boss)
# loop to make 10 asteroids
for _ in range(10):
    asteroid = Asteroid()
    # add to sprite groups
    all_sprites.add(asteroid)
    asteroids.add(asteroid)
sheilds = pygame.sprite.Group()
shotguns = pygame.sprite.Group()

# main game loop
while alive:
    # makes sure game doesn't drop below 30 frames
    clock.tick(FPS)
    # add frames passed to timer
    frames += FPS
    # increase score overtime, only if boss isn't spawned
    if not boss_spawned:
        score += 1
    # event loop
    for event in pygame.event.get():
        # checks if user quits
        if event.type == pygame.QUIT:
           alive = False
        # checks if user clicks space button to shoot
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # call shoot function
                player.shoot()
    # update sprite movement
    all_sprites.update()
    # check for laser collision with asteroids and kill both sprites
    shot = pygame.sprite.groupcollide(lasers, asteroids, True, True)
    # loop through each collision
    for _ in shot:
        # play explosion sound
        explo = pygame.mixer.Sound('explosion.wav')
        explo.play()
        # add a new asteroid to replace
        asteroid = Asteroid()
        # add to sprite groups
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
    # check for player crashing with asteroids, kill the asteroid sprite
    crash = pygame.sprite.spritecollide(player, asteroids, True)
    # loop through each collision
    for _ in crash:
        # play sound effect
        dmg.play()
        # reduce player health
        health -= 5
        # Create new asteroid to replace the one killed in the collision
        asteroid = Asteroid()
        # add to sprite group
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
        # check if player dies
        if health <= 0:
            gameOver()
    # check if player picks up sheild power up, kill the sheild sprite
    sheild_contact = pygame.sprite.spritecollide(player, sheilds, True, False)
    if sheild_contact:
        # play a sound effect
        powerUp.play()
        # add 20 health
        if health <= 80:
            health += 20
        else:
            # to prevent extra health, replenish all of the player's health
            health_add = 100 - health
            health += health_add
    # check if player picks up shotgun power up, kill the shotgun sprite
    shotgun_contact = pygame.sprite.spritecollide(player, shotguns, True, False)
    if shotgun_contact:
        # play power up sound effect
        powerUp.play()
        # define when the player get's the shotugn power up by getting the current frames that passed
        shotgun_timer = frames
        # make shotgun_shot true so the player can shoot shotgun shots
        shotgun_shot = True
    # check if shotgun runs out of time
    if shotgun_shot:
        # if the time is 3000 frames after the shotgun_timer, then it becomes False and the player no longer shoots shotgun_shots
        if frames == shotgun_timer + 3000:
            shotgun_shot = False
    # boss events and collisions
    if boss_spawned:
        # check if player collides with boss
        if pygame.sprite.collide_rect(player, boss):
            # player loses health
            health -= 5
            # play sound effect
            dmg.play()
            # check if player dies
            if health <= 0:
                # call game over function
                gameOver()
        # check if boss lasers hit player, kill the laser sprites that hit the player
        boss_hits = pygame.sprite.spritecollide(player, boss_lasers, True)
        # loop through each hit
        for _ in boss_hits:
            # play sound effect
            dmg.play()
            # remove player health. Laser damage scales with the score, so lasers do more damage as score gets higher
            health -= 10 * (score // 1000)
            # check if player dies
            if health <= 0:
                # call game over function
                gameOver()
        # check for collisions of the player's lasers and the boss, kill the laser sprites that collide
        player_shoots_boss = pygame.sprite.spritecollide(boss, lasers, True)
        for _ in player_shoots_boss:
            # decrease boss health
            boss_health -= 20
            # check if boss dies
            if boss_health <= 0:
                # increase boss health for next round
                boss_health = 200 * ((score // 1000) + 1)
                # go back to increasing score
                score += 1
                # play sound effect
                boss_death_sound.play()
                # call boss to despawn and go off screen
                boss.despawn()
                # set bool to false so loop doesn't check events again
                boss_spawned = False
        # if boss lasers and player lasers collide, kill both sprites
        bullet_collide = pygame.sprite.groupcollide(lasers, boss_lasers, True, True)
    # check if player meets a score interval to spawn a boss
    if score % 1000 == 0 and not boss_spawned and score != 0:
        # play sound effect
        boss_sound.play()
        # call boss to spawn
        boss.spawn()
        # make bool true
        boss_spawned = True
        # begin to draw boss healthbar
        boss.healthbar()
    # increase difficulty at 500 score intervals
    elif score % 500 == 0 and score != 0 and not boss_spawned:
        difficulty += 1
    # timer for boss to shoot
    if boss_spawned:
        # make the boss shoot at 450 frame intervals
        if frames % 450 == 0:
            boss.shoot()
    # draw screen background
    screen.blit(background, [0, 0])
    # to determine the probability of a powerup, I made a random number generator and said that a powerup will only
    # spawn if the random number is a predetermined number.
    pow_chance = random.randint(1, 100)
    if pow_chance == 9:
        # 1/2 chance for the powerup to be a shield or shotgun
        type_chance = random.randint(1, 2)
        if type_chance == 1:
            # make shield sprite
            shield = Sheild()
            # add to sprite groups
            sheilds.add(shield)
            all_sprites.add(shield)
        elif type_chance == 2:
            # add shotgun sprite
            shotgun = Shotgun()
            # add to sprite groups
            shotguns.add(shotgun)
            all_sprites.add(shotgun)
    # project boss healthbar if boss is spawned
    if boss_spawned:
        boss.healthbar()
    # draw back of player healthbar that reflects their total health, 100.
    pygame.draw.rect(screen, red, (50, 50, 100, 10))
    # draw the front portion which reflects their current health via the health var
    pygame.draw.rect(screen, green, (50, 50, health, 10))
    # draw all sprites
    all_sprites.draw(screen)
    # draw the score text at the top of the screen
    # make score to string to be able to write
    score = str(score)
    # render the text
    scoretext = font.render(score, False, (200, 200, 200))
    # draw the text
    screen.blit(scoretext, ((width / 2) - 50, 20))
    # convert back to integer
    score = int(score)
    # check if score is higher than highscore
    if score > highscore:
        # make highscore the score
        highscore = score
        # create and draw text alert to the top right of the screen
        highscore_text = font.render("New highscore!", False, (200, 200, 200))
        screen.blit(highscore_text, (width - 220, 20))
    # flip display
    pygame.display.flip()
# quit pygame when loop is complete
pygame.quit()
