# gridSense.py
# Animation and single frame creation append for SenseHAT LED matrix
# Add Message, Error and Warning Windows
# Add explore file window to save and load PNG and PY
import pygame, sys, time
from sense_hat import SenseHat
from pygame.locals import *

from gridAnimation import gridAnimation # List Management
from gridColors import * # Constant colors
from buttons import Button # Button Management

# Inicialize Window
saved = True # Actual Frame Saved?
warning = False # Something to worry?
buttons = []
buttons_warn = []
WINDOWSIZE = (530, 395)
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(WINDOWSIZE, 0, 32)
pygame.display.set_caption('Sense HAT Grid Editor') # Window title
pygame.mouse.set_visible(1)
background = pygame.Surface( screen.get_size() ).convert()
background.fill(BLACK)

# Initialize Grid Frame Animation
GRIDFRAMECODEPY = 'gridFrameCode.py'
GRIDFRAMEIMAGEPNG = 'gridFrameImage.png'
color = RED # Initial LED color
rotation = 0 # Actual Frame Rotation, it can be 0º, 90º, 180º, 270º
frame_number = 0 # Show actual number frame
fps = 4 # Frames per second
sensehat = SenseHat() # Inicialize Sense HAT
frame = gridAnimation() # Inicialize animation data structure

def setColourRed():
    global color
    color = RED

def setColourBlue():
    global color
    color = BLUE

def setColourGreen():
    global color
    color = GREEN

def setColourPurple():
    global color
    color = PURPLE

def setColourPink():
    global color
    color = PINK

def setColourYellow():
    global color
    color = YELLOW

def setColourOrange():
    global color
    color = ORANGE

def setColourWhite():
    global color
    color = WHITE

def setColourCyan():
    global color
    color = CYAN

# Clears the actual frame led grid and sets all the frame.lit back to False
def clearGrid():
    global sensehat
    global frame
    sensehat.clear()
    frame.Clear()
    
# Writes grid to PNG file
def exportGridToPNG():
    global saved
    global frame
    frame.saveImage(GRIDFRAMEIMAGEPNG)
    saved = True

# Load PNG to actual frame
def importGridFromPNG():
    global frame
    global rotation
    global sensehat
    frame.set_rotation(rotation)
    sensehat.set_rotation(rotation)
    frame.loadImage(GRIDFRAMEIMAGEPNG)
    sensehat.set_pixels( frame.getLedList() )
    drawEverything()

# Writes Grid to console
def exportToConsole():
    global frame
    print( frame.getLedList() )

#Rotates image on SenseHAT LED matrix
def rotate():
    global rotation
    global frame
    rotation = (rotation + 90) % 360
    sensehat.set_rotation( rotation )
    frame.set_rotation( rotation )
    drawEverything()

def handleClick():
    global saved
    global color
    global frame
    global warning
    _position = pygame.mouse.get_pos()
    _isLed = frame.findLed(_position[0], _position[1])
    if _isLed:
        global sensehat
        sensehat.set_pixel(_isLed.x, _isLed.y, _isLed.clicked(color))
        saved = False
    for _button in buttons:
        if _button.rect.collidepoint(_position):
            _button.click()
    if warning:
        for _button in buttons_warn:
            if _button.rect.collidepoint(_position):
                _button.click()

def drawEverything():
    global warning
    global frame
    
    screen.blit(background, (0, 0))
    
    # Draw actual frame
    frame.Draw()
    
    # Draw buttons
    for _button in buttons:
        _button.draw(screen)
        
    _font = pygame.font.Font(None,16)
    screen.blit(_font.render('Frame', 1, WHITE), (5, 5))
    screen.blit(_font.render( str(frame_number), 1, WHITE ), (18, 18))
    screen.blit(_font.render('Frame rate =' + str(fps) +' fps', 1, WHITE), (175, 10))
    
    _font = pygame.font.Font(None, 18)
    screen.blit(_font.render('Animation', 1, WHITE), (445, 15))
    screen.blit(_font.render('Single Frame', 1, WHITE), (435, 120))
    pygame.draw.circle(screen, color, (390, 345), 20, 0)
    
    if warning:
        for _button in buttons_warn:
            _button.draw(screen)
            
    # Flip the screen        
    pygame.display.flip()

def nextFrame():
    global frame
    frame.Next()
    global frame_number
    frame_number = frame.Index()
    global rotation
    rotation = frame.get_rotation()
    global sensehat
    sensehat.set_rotation(rotation)
    sensehat.set_pixels( frame.getLedList() )
    frame.Draw()

def prevFrame():
    global frame
    frame.Previous()
    global frame_number
    frame_number = frame.Index()
    global rotation
    rotation = frame.get_rotation()
    global sensehat
    sensehat.set_rotation(rotation)
    sensehat.set_pixels( frame.getLedList() )
    frame.Draw()

def delFrame():
    global frame
    frame.Delete()
    global frame_number
    frame_number = frame.Index()
    global rotation
    rotation = frame.get_rotation()
    global sensehat
    sensehat.set_rotation(rotation)
    sensehat.set_pixels( frame.getLedList() )
    frame.Draw()

def play():
    global frame
    global sensehat
    global rotation
    global frame_number
    _frameNumber = frame.Index()
    
    _size = frame.Size() + 1
    _fps = frame.Fps()
    frame.setIndex( 0 )
    for _playFrame in range(_size):
        frame_number = frame.Index()
        rotation = frame.get_rotation()
        sensehat.set_rotation(rotation)
        sensehat.set_pixels( frame.getLedList() )
        drawEverything()
        time.sleep(1.0/_fps)
        frame.Next()
    
    frame.setIndex( _frameNumber )
    frame_number = frame.Index()
    rotation = frame.get_rotation()
    sensehat.set_rotation(rotation)
    sensehat.set_pixels( frame.getLedList() )
    drawEverything()

def faster():
    global fps
    global frame
    fps = frame.Faster()

def slower():
    global fps
    global frame
    fps = frame.Slower()

# Create an Animation Python application
def exportAnimation():
    global saved
    global frame
    _file = open( GRIDFRAMECODEPY, 'w' )
    _file.write( frame.getLedListPy() )
    _file.close()
    saved = True

def prog_exit():
    clearGrid()
    pygame.quit()
    sys.exit()

def saveAndExit():
    exportAnimation()
    prog_exit()

def importGridFromFilePY():
    global frame
    _file = open( GRIDFRAMECODEPY )
    frame.setLedListPy( _file.read() )
    _file.close()
    global sensehat
    sensehat.set_pixels( frame.getLedList() )

# No Save warning window
def nosave_warning():
    global warning
    global screen
    warning = True
    _font = pygame.font.Font(None,48)
    _frame_text = 'Unsaved Frames'
    for _ in range(5):
        _text = _font.render(_frame_text,1,RED)
        screen.blit( _text, ( 100, 100 ) )
        pygame.display.flip()
        time.sleep( 0.1 )
        _text = _font.render(_frame_text,1,GREEN)
        screen.blit( _text, ( 100, 100 ) )
        pygame.display.flip()
        time.sleep( 0.1 )
    drawEverything()

def check_exit():
    global saved
    if not saved:
        nosave_warning()
    else:
        prog_exit()

# ***************** Main program body - Set up leds and buttons ************
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
buttons.append(Button('Export to PY', action = exportAnimation,         size = (100, 30), pos = (425,  45), color =   DARKBRICK))
buttons.append(Button('Import from PY', action = importGridFromFilePY,size = (100, 30), pos = (425,  80), color =   DARKBRICK))
buttons.append(Button('Export to console', action = exportToConsole,    size = (100, 30), pos = (425, 150), color =   GREY))
buttons.append(Button('Export to PNG', action = exportGridToPNG,        size = (100, 30), pos = (425, 185), color =   GREY))
buttons.append(Button('Import from PNG', action = importGridFromPNG,    size = (100, 30), pos = (425, 220), color =   GREY))
buttons.append(Button('Clear Grid', action = clearGrid,                 size = (100, 30), pos = (425, 255), color =   LIGHTCYAN, fontColor = BLACK))
buttons.append(Button('Rotate LEDs', action = rotate,                   size = (100, 30), pos = (425, 290), color =   LIGHTCYAN, fontColor = BLACK))
buttons.append(Button('Play on LEDs', action = play,                    size = (100, 30), pos = (425, 325), color =   LIGHTBROWN))
buttons.append(Button('Quit', action = check_exit,                       size = (100, 30), pos = (425, 360), color =   DARKGREY))

# Buttons over windows
buttons_warn.append(Button('Save', action = saveAndExit,                 size = ( 60, 50), pos = (150, 250), hilight = BRICK,color=YELLOW,fontColor = BLACK))
buttons_warn.append(Button('Quit', action = prog_exit,               size = ( 60, 50), pos = (260, 250), hilight = BRICK,color=YELLOW,fontColor = BLACK))
    
################ Main prog loop ################
while True:
    drawEverything()
    for _event in pygame.event.get():
        if _event.type == pygame.QUIT:
            check_exit()
        if _event.type == pygame.MOUSEBUTTONDOWN:
            handleClick()