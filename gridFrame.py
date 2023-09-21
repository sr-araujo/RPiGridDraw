from gridColors import *
from led import LED
import png, math

# Class to manage an Array of 8x8 gridLeds
class gridFrame():
    def __init__(self, width = 8, height = 8, radius = 20, rotation = 0):
        self.width = width # Width / Max X
        self.height = height # Height / Max Y
        self.size = width * height # Size / Max Elements
        self.rotation = rotation # 0, 90, 180, 270
        self.led = [ LED(x, y, radius) for y in range(height) for x in range(width) ]
        ledMap0 = self.getLedMap() # Get Led Map
        ledMap270 = self.rotate90(ledMap0) # Rotate 90º
        ledMap180 = self.rotate90(ledMap270)
        ledMap90 = self.rotate90(ledMap180)
        self.ledMap = { # LED map orientation
              0: ledMap0,
             90: ledMap90,
            180: ledMap180,
            270: ledMap270
        }
    
    # Get 1D index of an 2D array/matrix
    def getLedIndex(self, _x, _y):
       return _x + (self.width * _y)
    
    # Draw all 64 led grid
    def Draw(self):
        for _i in range(self.size):
            self.led[_i].draw()
    
    # Set LED map orientation of the image being shown (0, 90, 180, 270)
    def setLedMap(self, ledMap):
        for _i in range(self.size):
            self.led[_i].pos_x, self.led[_i].pos_y = ledMap[_i]
    
    # Get LED map orientation of the image being shown (0, 90, 180, 270)
    def getLedMap(self):
        return [ (self.led[_i].pos_x, self.led[_i].pos_y) for _i in range(self.size) ]
        
    # Change the orientation of the image being shown (0, 90, 180, 270)
    def set_rotation(self, _rotation = 0):
        if _rotation in self.ledMap.keys():
            self.rotation = _rotation
            self.setLedMap(self.ledMap[_rotation])
    
    # Rotate LED map
    def rotate90(self, ledMap):
        _i = 0
        _x = self.width
        _newLedMap = [ (_, _) for _ in range(self.size)]
        while _x > 0:
            _x -= 1
            for _y in range(self.height):
                _newLedMap[self.getLedIndex(_x, _y)] = ledMap[_i]
                _i += 1
                
        return _newLedMap
    
    # Clear gridFrame
    def clear(self):
        for _i in range(self.size):
            self.led[_i].color =  EMPTY
            self.led[_i].lit = False
    
    # Return a [list of 64 (tuple RGB color)]
    def getLedList(self):
        return [ self.led[_i].color for _i in range(self.size) ]
    
    # Return a [list of 8 (tuple of 24 int values (24 / 3 = 8 RGB colours) )]
    def getLedListPng(self):
        _listColor = [ () for _y in range(self.height) ] # list of 8 empty tuples
        
        for _i in range(self.size): # Fill tuples
            _listColor[self.led[_i].y] += self.led[_i].color
                    
        return _listColor
    
    # Load an image from a PNG file
    def loadImage(self, _fileName = 'gridImage.png'):
        _f = open(_fileName, 'rb') # binary read mode is important
        _, _, _c, _m = png.Reader(_f).read_flat()
        _f.close()
        _t = _m['planes'] # Tuple size
        _a = _t - 3 # Adjust if tuple > 3
        for _i in range(self.size):
            self.led[_i].color = tuple(_c[(_i * _t) : ((_i + 1) * _t) - _a])
            self.led[_i].lit = self.led[_i].color != EMPTY
    
    # Save image to a PNG file
    def saveImage(self, _fileName = 'gridFrameImage.png'):
        _f = open(_fileName, 'wb') # binary read mode is important
        png.Writer(8, 8, greyscale = False).write(_f, self.getLedListPng())
        _f.close()

    # Return a string of 64 (tuple RGB color)
    #def getLedListStr(self):
    #    return str(self.getLedList())
    
    # self =  str [list of 64 (tuple RGB color)]
    def setLedListStr(self, l):
        _j = 0 # str index
        for _i in range(self.size): # index of gridFrame
            while l[_j] != '(': _j +=1 # search tuple RGB
            # Extract R G B str values
            _j += 1 # ignore '('
            
            # Get red str value
            _r = ''
            while l[_j] != ',':
                _r += l[_j]
                _j += 1
            _j += 1 # ignore ','
            
            # Get green str value
            _g = ''
            while l[_j] != ',':
                _g += l[_j]
                _j += 1
            _j += 1 # ignore ','
            
            # Get blue str value
            _b = ''
            while l[_j] != ')':
                _b += l[_j]
                _j += 1
                
            # Convert, tuple(R,G,B) = str(r,g,b)
            self.led[_i].color = (int(_r), int(_g), int(_b))
            self.led[_i].lit = self.led[_i].color != EMPTY
            
    # Reads leds and checks if clicked position is in one of them
    def findLed(self, xPos, yPos):
        for _i in range(self.size):
            if math.hypot(self.led[_i].pos_x - xPos, self.led[_i].pos_y - yPos) <= self.led[_i].radius:
                return self.led[_i]
        return None
    
    # Return a gridFrame usefull information
    def __str__(self):
        _s = '['
        _width = self.width - 1
        _height = self.height - 1
        for _y in range(self.height):
            _s += '('
            _yindx = _y * self.width
            for _x in range(self.width):
                if _x > 0: _s += ' '
                _i = _x + _yindx
                _s += f'<{(self.led[_i].x,self.led[_i].y)} {self.led[_i].lit} {self.led[_i].color}>'
                if _x < _width: _s += ','
            _s += ')'
            if _y < _height: _s += ',\n'
        _s += ']'
        return _s