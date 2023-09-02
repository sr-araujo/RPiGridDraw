# 8x8grid-sense.py
# Animation and single frame creation append
# for SenseHAT LED matrix
import pygame, sys, math, time, png, os
from sense_hat import SenseHat
from pygame.locals import *

from buttons import Button
from led import LED
from colors import *

GRIDANIMATIONPY = '8x8grid-animation.py'
GRIDIMAGEPNG = '8x8grid-image.png'

saved = True
warning = False
pygame.init()
pygame.font.init()

sh = SenseHat()
screen = pygame.display.set_mode((530, 395), 0, 32)
pygame.display.set_caption('Sense HAT Grid Editor')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)
colour = RED # Initial LED color
rotation = 0
# Actual number frame
frame_number = 0
fps = 4

# Make an 8x8 array of LED (actual frame)
leds = []
for yi in range(8):
    for xi in range(8):
        leds.append( LED(xi, yi , 20) )
        
buttons = []
buttons_warn = []
# Dictionary of 8x8 array LED for animation
animation={}

def setColourRed():
    global colour
    colour = RED

def setColourBlue():
    global colour
    colour = BLUE

def setColourGreen():
    global colour
    colour = GREEN

def setColourPurple():
    global colour
    colour = PURPLE

def setColourPink():
    global colour
    colour = PINK

def setColourYellow():
    global colour
    colour = YELLOW

def setColourOrange():
    global colour
    colour = ORANGE

def setColourWhite():
    global colour
    colour = WHITE

def setColourCyan():
    global colour
    colour = CYAN

# Clears the pygame LED grid and sets all the leds.lit back to False
def clearGrid():
    global sh
    sh.clear()
    for ld in leds:
        #ld.color = WHITE
        ld.color = EMPTY
        ld.lit = False

# The grid is an 1d array, then convert coordinates (x,y) to (index)
def getIndex( x, y ):
    return x + (y * 8)

# Takes a grid and builds version for exporting to Text
def buildGrid():
    global leds
    #grid = [ leds[i].color if leds[i].lit else EMPTY for i in range(64)]
    grid = [ tuple(leds[i].color) for i in range(64)]
        
#    for ld in leds:
#        if ld.lit:
#            grid[ getIndex( ld.pos ) ] = ld.color
        
    return grid

# Takes a grid and builds version for exporting to PNG
def buildGridPNG():
    gridPNG = [ (), (), (), (), (), (), (), () ] # list of 8 empty tuples 
    
    for ld in leds:
        gridPNG[ld.y] += ld.color if ld.lit else EMPTY
        #gridPNG[ld.y] += ld.color
    
    return gridPNG

# Loads image onto SenseHAT matrix
def piLoad():
    sh.set_pixels( buildGrid() )

# Writes grid to PNG file
def exportGridToPNG():
    global saved
    with open(GRIDIMAGEPNG,'wb') as f:
        w = png.Writer(8, 8, greyscale = False)
        w.write(f, buildGridPNG())
        f.close()
        saved = True
        
def importGridFromPNG():
    global sh
    global leds
    global frame_number
    frame_number = 0
    
    grid = sh.load_image(file_path = GRIDIMAGEPNG)
    
    for ld in leds:
        ld.color = grid[ getIndex(ld.x, ld.y) ]
        ld.lit = ld.color != EMPTY
    
    drawEverything()
    animation[frame_number] = leds.copy() # animation.update({str(frame_number): leds.copy()})

# Writes Grid to console
def exportToConsole():
    print(buildGrid())

#Rotates image on SenseHAT LED matrix
def rotate():
    global rotation
    rotation = (rotation + 90) % 360
    sh.set_rotation(rotation)

def handleClick():
    global saved
    global warning
    pos = pygame.mouse.get_pos()
    isLed = findLED(pos, leds)
    if isLed:
        isLed.clicked(colour)
        saved = False
    for butt in buttons:
        if butt.rect.collidepoint(pos):
            butt.click()
    if warning:
        for butt in buttons_warn:
            if butt.rect.collidepoint(pos):
                butt.click()

# reads leds and checks if clicked position is in one of them
def findLED(clicked_pos, LEDs):
    xPosition = clicked_pos[0]
    yPosition = clicked_pos[1]
    for ld in LEDs:
        if math.hypot(ld.pos_x - xPosition, ld.pos_y - yPosition) <= ld.radius:
            return ld
    return None

def drawEverything():
    global warning
    screen.blit(background, (0, 0))
    
    # Draw leds
    for ld in leds:
        ld.draw()
    # Draw buttons
    for bt in buttons:
        bt.draw(screen)
        
    font = pygame.font.Font(None,16)
    screen.blit(font.render('Frame ', 1, WHITE), (5, 5))
    screen.blit(font.render( str(frame_number), 1, WHITE ), (18, 18))
    screen.blit(font.render('Frame rate= ' + str(fps) +' fps', 1, WHITE), (175, 10))
    
    font = pygame.font.Font(None, 18)
    screen.blit(font.render('Animation', 1, WHITE), (445, 15))
    screen.blit(font.render('Single Frame', 1, WHITE), (435, 120))
    pygame.draw.circle(screen,colour, (390, 345), 20, 0)
    
    if warning:
        for bt in buttons_warn:
            bt.draw(screen)
            
    # Flip the screen        
    pygame.display.flip()

def load_leds_to_animation():
    global frame_number
    global leds
    for saved_led in animation[frame_number]:
        if saved_led.lit:
            for ld in leds:
                if (ld.x, ld.y) == (saved_led.x, saved_led.y):
                    ld.color = saved_led.color
                    ld.lit = True

def nextFrame():
    global frame_number
    global leds
    animation[frame_number] = leds.copy()
    frame_number += 1
    if frame_number in animation:
        leds =[]
        for xi in range(8):
            for yi in range(8):
                leds.append( LED(xi, yi, 20) )
        load_leds_to_animation()

def prevFrame():
    global frame_number
    global leds
    animation[frame_number] = leds.copy()
    clearGrid()
    
    if frame_number != 1:
        frame_number -= 1
    if frame_number in animation:
        leds =[]
        for xi in range(8):
            for yi in range(8): 
                leds.append( LED(xi, yi, 20) )
        load_leds_to_animation()

def delFrame():
    global frame_number
    if len(animation) > 1:
        print(animation)
        print('length =' + str(len(animation)))
        animation[frame_number] = leds.copy()
        print('deleting ' + str(frame_number))
        del animation[frame_number]
        print('length now =' + str(len(animation)))
        prevFrame()
        for shuffle_frame in range(frame_number + 1, len(animation)):
            print('shifting ' + str(shuffle_frame+1) + ' to  be ' + str(shuffle_frame))
            animation[shuffle_frame] = animation[shuffle_frame + 1].copy()
        print('deleting ' + str(len(animation)))
        del animation[len(animation)]

#def getLitLEDs():
#    points = []
#    for ld in leds:
#        if ld.lit:
#            points.append(ld.pos)
#    return points

# ***************** Main program body - set up leds and buttons ************
def play():
    global leds
    global frame_number
    animation[frame_number] = leds.copy()
    
    for playframe in range(len(animation)):
        leds =[]
        for xi in range(8):
            for yi in range(8):
                leds.append( LED(xi, yi, 20) )
            for saved_led in animation[playframe]:
                if saved_led.lit:
                    for ledTmp in leds:
                        if (ledTmp.x, ledTmp.y) == (saved_led.x, saved_led.y):
                            ledTmp.color = saved_led.color
                            ledTmp.lit = True
        piLoad()
        time.sleep(1.0/fps)
    frame_number = len(animation)

def faster():
    global fps
    fps += 1

def slower():
    global fps
    if fps > 1:
        fps -= 1

def gridToSTRpy(gridRAW):
    string = '    [\n'
    for iy in range(8):
        string += '    '
        for ix in range(8):
            i = ix + (iy * 8)
            if   gridRAW[i] == E: string += 'E'
            elif gridRAW[i] == R: string += 'R'
            elif gridRAW[i] == O: string += 'O'
            elif gridRAW[i] == Y: string += 'Y'
            elif gridRAW[i] == G: string += 'G'
            elif gridRAW[i] == C: string += 'C'
            elif gridRAW[i] == B: string += 'B'
            elif gridRAW[i] == P: string += 'P'
            elif gridRAW[i] == K: string += 'K'
            elif gridRAW[i] == W: string += 'W'
            else: string += str(gridRAW[i]) # Unknow color
            if ix == 7 and iy == 7:
                string += '\n    ]'
                continue
            string +=','
        if iy == 7:
            continue
        string += '\n'
    return string

def exportAnimation():
    global saved
    FILE=open(GRIDANIMATIONPY,'w')
    FILE.write('# Python program created with '+ os.path.basename(__file__) +'\n')
    FILE.write('from sense_hat import SenseHat\n')
    FILE.write('import time\n\n')
    FILE.write('# Color Tuples\n')
    FILE.write('E  = (  0,   0,   0) # Empty (Black or LED off)\n')
    FILE.write('R  = (255,   0,   0) # Red\n')
    FILE.write('O  = (255, 128,   0) # Orange\n')
    FILE.write('Y  = (255, 255,   0) # Yellow\n')
    FILE.write('G  = (  0, 128,   0) # Green\n')
    FILE.write('C  = (  0, 255, 255) # Cyan\n')
    FILE.write('B  = (  0,   0, 255) # Blue\n')
    FILE.write('P  = (102,   0, 204) # Purple\n')
    FILE.write('K  = (255,   0, 255) # Pink\n')
    FILE.write('W  = (255, 255, 255) # White\n')
    FILE.write('\nsh = SenseHat()\n')
    FILE.write('frames = [\n')
    global leds
    global frame_number    
    animation[frame_number] = leds.copy()
    
    for playframe in range(len(animation)):
        leds =[]
        for yi in range(8):
            for xi in range(8):
                leds.append( LED(xi, yi, 20) )
            for saved_led in animation[playframe]:
                if saved_led.lit:
                    for ld in leds:
                        if (ld.x, ld.y) == (saved_led.x, saved_led.y):
                            ld.color = saved_led.color
                            ld.lit = True
        grid = buildGrid()

        FILE.write(gridToSTRpy(grid))
        if playframe == (len(animation) - 1):
            FILE.write('\n')
            continue
        FILE.write(',\n')
    FILE.write(']\n\n')
    FILE.write('for x in frames:\n')
    FILE.write('    sh.set_pixels(x)\n')
    FILE.write('    time.sleep('+ str(1.0/fps) + ')\n')
    FILE.write('\ninput(\'Press ENTER to continue. .  .\')\n')
    FILE.write('sh.clear()')
    FILE.close()
    saved = True

def prog_exit():
    print('exit clicked')
    global warning
    warning = False
    clearGrid()
    pygame.quit()
    sys.exit()

def save_it():
    print('save clicked')
    global warning
    exportAnimation()
    warning = False

def quit():
    global saved
    if not saved:
        nosave_warn()
    else:
        prog_exit()

def importGridFromFilePY():
    global leds
    global frame_number
    frame_number = 0
    file = open(GRIDANIMATIONPY)
    
    l = 0
    while l < 19:
        file.readline()
        l += 1
    
    counter = 0
    leds = []
    line = 0
    while line < 8:
        buff = file.readline().replace(',\n','').strip()
        load_frame = buff.split(',')
                
        for f in load_frame:
            ledTmp = LED(counter % 8, int(counter / 8), 20)
            
            ledTmp.lit = True
            if   f == 'E':
                ledTmp.lit = False
                ledTmp.color = E
            elif f == 'R': ledTmp.color = R
            elif f == 'O': ledTmp.color = O
            elif f == 'Y': ledTmp.color = Y
            elif f == 'G': ledTmp.color = G
            elif f == 'C': ledTmp.color = C
            elif f == 'B': ledTmp.color = B
            elif f == 'P': ledTmp.color = P
            elif f == 'K': ledTmp.color = K
            elif f == 'W': ledTmp.color = W
            
            leds.append(ledTmp)
            counter += 1
        line += 1
    
    animation[frame_number] = leds.copy()
    file.close()

buttons.append(Button('<-', action = prevFrame,                         size = ( 25, 30), pos = ( 50,   5), color =   LIGHTBROWN))
buttons.append(Button('->', action = nextFrame,                         size = ( 25, 30), pos = ( 80,   5), color =   LIGHTBROWN))
buttons.append(Button('Delete', action = delFrame,                      size = ( 50, 30), pos = (115,   5), color =   LIGHTBROWN))
buttons.append(Button('+', action = faster,                             size = ( 25, 30), pos = (300,   5), color =   LIGHTBROWN))
buttons.append(Button('-', action = slower,                             size = ( 25, 30), pos = (330,   5), color =   LIGHTBROWN))
buttons.append(Button('', action = setColourRed,                        size = ( 50, 30), pos = (365,  10), hilight = DARKCYAN, color = RED))
buttons.append(Button('', action = setColourOrange,                     size = ( 50, 30), pos = (365,  45), hilight = DARKCYAN, color = ORANGE))
buttons.append(Button('', action = setColourYellow,                     size = ( 50, 30), pos = (365,  80), hilight = DARKCYAN, color = YELLOW))
buttons.append(Button('', action = setColourGreen,                      size = ( 50, 30), pos = (365, 115), hilight = DARKCYAN, color = GREEN))
buttons.append(Button('', action = setColourCyan,                       size = ( 50, 30), pos = (365, 150), hilight = DARKCYAN, color = CYAN))
buttons.append(Button('', action = setColourBlue,                       size = ( 50, 30), pos = (365, 185), hilight = DARKCYAN, color = BLUE))
buttons.append(Button('', action = setColourPurple,                     size = ( 50, 30), pos = (365, 220), hilight = DARKCYAN, color = PURPLE))
buttons.append(Button('', action = setColourPink,                       size = ( 50, 30), pos = (365, 255), hilight = DARKCYAN, color = PINK))
buttons.append(Button('', action = setColourWhite,                      size = ( 50, 30), pos = (365, 290), hilight = DARKCYAN, color = WHITE))
buttons.append(Button('Export to py', action = exportAnimation,         size = (100, 30), pos = (425,  45), color =   DARKBRICK))
buttons.append(Button('Import from file', action = importGridFromFilePY,size = (100, 30), pos = (425,  80), color =   DARKBRICK))
buttons.append(Button('Export to console', action = exportToConsole,    size = (100, 30), pos = (425, 150), color =   GREY))
buttons.append(Button('Export to PNG', action = exportGridToPNG,        size = (100, 30), pos = (425, 185), color =   GREY))
buttons.append(Button('Import from PNG', action = importGridFromPNG,    size = (100, 30), pos = (425, 220), color =   GREY))
buttons.append(Button('Clear Grid', action = clearGrid,                 size = (100, 30), pos = (425, 255), color =   LIGHTCYAN, fontColor = BLACK))
buttons.append(Button('Rotate LEDs', action = rotate,                   size = (100, 30), pos = (425, 290), color =   LIGHTCYAN, fontColor = BLACK))
buttons.append(Button('Play on LEDs', action = play,                    size = (100, 30), pos = (425, 325), color =   LIGHTBROWN))
buttons.append(Button('Quit', action = quit,                            size = (100, 30), pos = (425, 360), color =   DARKGREY))

# Buttons over windows
buttons_warn.append(Button('Save', action = save_it,                 size = ( 60, 50), pos = (150, 250), hilight = BRICK,color=YELLOW,fontColor = BLACK))
buttons_warn.append(Button('Quit', action = prog_exit,               size = ( 60, 50), pos = (260, 250), hilight = BRICK,color=YELLOW,fontColor = BLACK))


def nosave_warn():
    global warning
    warning = True
    font = pygame.font.Font(None,48)
    frame_text = 'Unsaved Frames '
    d = 0
    while d < 5:
        text = font.render(frame_text,1,RED)
        screen.blit(text, (100,100))
        pygame.display.flip()
        time.sleep(0.1)
        text = font.render(frame_text,1,GREEN)
        screen.blit(text, (100,100))
        pygame.display.flip()
        time.sleep(0.1)
        d += 1
    drawEverything()
    
################ Main prog loop ################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not saved:
                nosave_warn()
            else:
                prog_exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            handleClick()

    #update the display
    drawEverything()