import pygame
from pygame import *

pygame.init()

win = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Llama Game!')
clock = pygame.time.Clock()
# ======================================================================================================================
# Loading images to use for the game.
icon = pygame.image.load('assets/SS_R_Icon.png')
pygame.display.set_icon(icon)

Machu_Picchu = pygame.image.load('assets/Machu_Picchu.gif')
Play_button = pygame.image.load('assets/Play_button.png')

llama_left = pygame.image.load('assets/llama_left.png') # Size is 110x110
llama_right = pygame.image.load('assets/llama_right.png') # Size is 110x110
llama_mid = pygame.image.load('assets/llama_mid.png') # Size is 110x110

spit_right = pygame.image.load('assets/spit_right.png') # Size is 62x56
spit_left = pygame.image.load('assets/spit_left.png') # Size is 62x56

spit_sound = pygame.mixer.Sound('assets/spit_3.wav')
slap_sound = pygame.mixer.Sound('assets/slap.wav')
llama_sound = pygame.mixer.Sound('assets/oorgle.wav')

# Link to song: https://musiclab.chromeexperiments.com/Song-Maker/song/6752443683569664
# pygame.mixer.music.load('assets/Piano_Conga.wav')
# pygame.mixer.music.load('assets/Strings_Conga.wav')
# pygame.mixer.music.load('assets/Synth_Conga.wav')
pygame.mixer.music.load('assets/Marimba_Conga.wav')
pygame.mixer.music.play(-1)

Sasan_R = pygame.image.load('assets/SS_R.png') # Size is 131x134
Sasan_L = pygame.image.load('assets/SS_L.png') # Size is 131x134
A_Sasan_R = pygame.image.load('assets/SS_A_R.png') # Size is 131x134
A_Sasan_L = pygame.image.load('assets/SS_A_L.png') # Size is 131x134
#=======================================================================================================================
class PLAYER():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 40
        self.is_jump = False
        self.jump_count = 80
        self.left = False
        self.right = False
        self.standing = True
        self.life = 1
        self.alive = True
        self.score = 0

    def draw(self, win):
        if self.life != 0 and self.alive:
            if not(self.standing):
                if self.left:
                    win.blit(llama_left, (self.x, self.y))
                elif self.right:
                    win.blit(llama_right, (self.x, self.y))
            else:
                if self.right:
                    win.blit(llama_right, (self.x, self.y))
                else:
                    win.blit(llama_left, (self.x, self.y))
            # else:
            #     win.blit(llama_mid, (self.x, self.y))


class PROJECTILE(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.right = False
        self.left = False
        self.velocity = 50
        self.is_tof = False

    def draw(self, win):
        if self.right == True:
            win.blit(spit_right, (self.x, self.y))
        elif self.left == True:
            win.blit(spit_left, (self.x, self.y))


class ENEMY():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 8
        self.left = False
        self.right = False

    def draw(self, win):
        if self.right:
            win.blit(Sasan_R, (self.x, self.y))
        elif self.left:
            win.blit(Sasan_L, (self.x, self.y))

def Score(score):
    font = pygame.font.SysFont('Courier', 24, True)
    text = font.render("Sasan's life:" + str(score), 1, (245, 25, 0))
    win.blit(text, (375, 15))


llama = PLAYER(450, 450, 120, 120) # Creating the llama character.
Sasan = ENEMY(0, 0, 135, 135)
tof = PROJECTILE(llama.x, llama.y)
# left, top, right, bottom = -30, -10, -105, -125

# ======================================================================================================================
# Drawing out the game dynamics.
def redraw_game_windew():
    win.blit(Machu_Picchu, (0, 0))
    Score(llama.score)
    Sasan.draw(win)
    llama.draw(win)
    tof.draw(win)
    pygame.display.update()
    # if llama.alive == False or llama.life == 1:
# ======================================================================================================================
# Intro to the game.
def Menu(run_game):
    intro = True
    while intro == True:
        win.blit(Machu_Picchu, (0, 0))
        win.blit(llama_mid, (300-68, 164))
        win.blit(Play_button, (300-225, 300-75))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            intro = False
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                intro = False
                run_game = False

        clock.tick(15)
    return run_game
# ======================================================================================================================
# Code to display the clue to solve the puzzle.
# def Clue():

# ======================================================================================================================
# Code for the actual game dynamics.
def Game_Loop(run_game):
    run = True
    llama.life = 1
    llama.alive = True
    llama.score = 15
    Sasan.velocity = 8
    Sasan.x = 0
    Sasan.y = 0
    while run:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                run_game = False
                return run_game

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and llama.x > 15:
            llama.x -= llama.velocity
            llama.left = True
            llama.right = False
            llama.standing = False
        elif keys[pygame.K_RIGHT] and llama.x < 475:
            llama.x += llama.velocity
            llama.left = False
            llama.right = True
            llama.standing = False
        else:
            llama.standing = True
        # else:
        #     llama.right = False
        #     llama.left = False

        if not(llama.is_jump):
            if keys[pygame.K_UP]:
                llama.is_jump = True
        else:
            llama.y += -1 * llama.jump_count
            llama.jump_count -= 10
            if llama.jump_count < -80:
                llama.jump_count = 80
                llama.is_jump = False

        if keys[pygame.K_SPACE] and llama.right == True:
            spit_sound.play()
            tof.is_tof = True
            tof.right = True
            tof.left = False
            tof.y = llama.y +5
            tof.x = llama.x + 20
        elif keys[pygame.K_SPACE] and llama.left == True:
            spit_sound.play()
            tof.is_tof = True
            tof.right = False
            tof.left = True
            tof.y = llama.y +5
            tof.x = llama.x + 25

        if tof.is_tof and tof.right:
            if tof.x < 600:
                tof.x += 30
            else:
                tof.is_tof = False
                tof.right = False
        elif tof.is_tof and tof.left:
            if tof.x > -50:
                tof.x -= 30
            else:
                tof.is_tof = False
                tof.left = False

        if llama.x - Sasan.x >= 0:
            Sasan.x += Sasan.velocity
            Sasan.right = True
            Sasan.left = False
        else:
            Sasan.x -= Sasan.velocity
            Sasan.left = True
            Sasan.right = False

        if llama.y - Sasan.y >= 0:
            Sasan.y += Sasan.velocity
        else:
            Sasan.y -= Sasan.velocity

        if tof.x > Sasan.x and tof.x < Sasan.x+65 and tof.y < Sasan.y+85 and tof.y > Sasan.y-25:
            llama.score -= 1
            slap_sound.play()
            tof.is_tof = False
            tof.right = False
            tof.left = False
            tof.x = llama.x + 22
            tof.y = llama.y + 5
            if llama.score == 5:
                Sasan.velocity += 5
            if llama.score == 0:
                run = False

        if Sasan.x < llama.x < Sasan.x+65 and Sasan.y-25 < llama.y < Sasan.y+65:
            llama.life -= 1
            llama.x = 450
            llama.y = 450
            Sasan.x = 0
            Sasan.y = 0
            llama.jump_count = 80
            llama.is_jump = False
            if llama.life == 0:
                llama.alive = False
            pygame.mixer.music.pause()
            llama_sound.play()
            pygame.time.delay(3500)
            pygame.mixer.music.unpause()
            run = False

        redraw_game_windew()
    return run_game

run_game = True
while run_game:
    run_game = Menu(run_game)
    if run_game == True:
        run_game = Game_Loop(run_game)
    # if llama.score >= 20:
    #     Clue()