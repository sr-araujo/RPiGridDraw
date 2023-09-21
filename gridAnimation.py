from gridColors import *
from gridFrame import gridFrame
import os

class gridAnimation(): # Never empty list, almost have 1 element
    def __init__(self):
        self.index = 0 # Index (Always actual frame)
        self.size = 0 # Size of list ( Empty list = -1 ) Size > -1
        self.fps = 4 # FPS
        self.frame = [
            gridFrame() # First element
        ]
    
    # Return actual frame fps
    def Fps(self):
        return self.fps
        
    # Faster FPS (Max 30 FPS)
    def Faster(self):
        if self.fps < 31:
            self.fps += 1
        return self.fps
        
    # Slow FPS (Min 1 FPS)
    def Slower(self):
        if self.fps > 1:
            self.fps -= 1
        return self.fps
    
    # Animation size. Frame number
    def Size(self):
        return self.size
    
    # Return actual frame index
    def Index(self):
        return self.index
    
    # Change the actual frame index
    def setIndex(self, _index = 0):
        if _index > -1 and _index <= self.size:
            self.index = _index
    
    # Next frame
    def Next(self):
        if self.index < self.size:
            self.index += 1
    
    # Previous frame
    def Previous(self):
        if self.index > 0:
            self.index -= 1
    
    # Delete frame
    def Delete(self):
        if self.size > 0: # Never empty list
            self.frame.pop(self.index)
            self.size -= 1
            if self.index > self.size:
                self.index = self.size
        elif self.size == 0: # If only one frame
            self.Clear() # Just clear but not delete
    
    # Push new frame
    def Push(self, _newFrame):
        if self.index < 0:
            self.index = 0
        self.size += 1
        self.frame.append(_newFrame)
    
    # Draw actual frame
    def Draw(self):
        self.frame[ self.index ].Draw()
    
    # Clear actual frame
    def Clear(self):
        self.frame[ self.index ].clear()
    
        # Return actual RGB tuples list
    def getLedList(self):
        return self.frame[ self.index ].getLedList()
    
    # Save actual frame to PNG file
    def saveImage(self, _fileName):
        self.frame[ self.index ].saveImage(_fileName)
    
    # Load PNG file to actual frame
    def loadImage(self, _fileName):
        self.frame[ self.index ].loadImage(_fileName)
    
    # Rotate actual frame
    def set_rotation(self, _rotation):
        self.frame[ self.index ].set_rotation(_rotation)
    
    # Rotate actual frame
    def get_rotation(self):
        return self.frame[ self.index ].rotation
    
    # Return True if click on a LED
    def findLed(self, x, y):
        return self.frame[ self.index ].findLed(x, y)
        
    # Return String of a Animation Python Aplication
    def getLedListPy(self): # Dictionary
        _strPyCode =  '# Python program created by '
        _strPyCode += os.path.basename(__file__)
        _strPyCode += '\nfrom sense_hat import SenseHat'
        _strPyCode += '\nfrom time import sleep'
       
        _strPyCode += '\n\nsensehat = SenseHat()'
        
        _strPyCode += '\n\nframe = {'
        _lenDictionary = len(self.frame) # Size of dictionary
        for _keyNumber in range(_lenDictionary): # While lists on dictionary
            _strPyCode += '\n    '
            _strPyCode += str(_keyNumber) # Set Key Number
            _strPyCode += ': [\n'
           
            _indexTuples = 0 # Index of tuples list [64 * (R,G,B)]
            for _iy in range(8):
                _strPyCode += '    '
                for _ix in range(8):
                    _strPyCode += '({:3},{:3},{:3})'.format(self.frame[_keyNumber].led[_indexTuples].color[0], self.frame[_keyNumber].led[_indexTuples].color[1], self.frame[_keyNumber].led[_indexTuples].color[2]) # Colour
                    _indexTuples += 1
                    if _ix == 7 and _iy == 7:
                        _strPyCode += '\n    ]'
                        continue
                    _strPyCode +=','
                if _iy == 7:
                    continue
                _strPyCode += '\n'
            if _keyNumber < (_lenDictionary - 1):
                _strPyCode += ','
                
        _strPyCode += '\n}' # End of dictionary
       
        _strPyCode += '\n\nfor _r in range(10): # Repeat 10 times the animation'
        _strPyCode += '\n    for _i in frame.keys(): # Run animation'
        _strPyCode += '\n        sensehat.set_pixels(frame[_i])'
        _strPyCode += '\n        sleep('
        _strPyCode += str(1.0 / self.fps)
        _strPyCode += ')'

        _strPyCode += '\n\ninput(\'Press ENTER to continue. .  .\')'
        _strPyCode += '\nsensehat.clear() # Clear Sense HAT'
        
        return _strPyCode
    
    # Get Lists of RGB tuples from an String with Python Aplication
    def setLedListPy(self, _strPyCode):
        _strIndex = 0 # String index
        while _strPyCode[_strIndex] != '{': # Search the dictionary on python code
            _strIndex += 1
            
        while True:
            while not _strPyCode[_strIndex].isdigit(): # Search a key of the dictionary
                _strIndex += 1
            
            _key = ''
            while _strPyCode[_strIndex].isdigit(): # Extract the key of the dictionary
                _key += _strPyCode[_strIndex]
                _strIndex += 1
            
            while _strPyCode[_strIndex] != '[': # Search list
                _strIndex += 1
            
            # Extact the list
            _list = ''
            while _strPyCode[_strIndex] != ']':
                _list += _strPyCode[_strIndex]
                _strIndex += 1
            _list += _strPyCode[_strIndex] # ']'
            _strIndex += 1
            
            _keyIndex = int(_key)
            
            if _keyIndex > self.size: # if
                self.Push( gridFrame() )
                
            self.frame[ _keyIndex ].setLedListStr( _list ) # Add [64 * (R,G,B)] to dicctionary
            
            while _strPyCode[_strIndex].isspace(): # Ignore spaces
                _strIndex += 1
            if _strPyCode[_strIndex] == '}' or _strIndex >= len(_strPyCode): # The end of dictionary, no more lists
                break