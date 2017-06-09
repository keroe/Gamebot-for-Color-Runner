#!/usr/bin/env python3

import pyautogui, time, os, logging, sys, random, copy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')

LEVEL_WIN_MESSAGE = 'win'

LEVEL = 1 # current level being played

GAME_REGION = () # (left, top, width, height) values coordinates of the game window



def main():
    """Runs the bot. It should be started in the beginning menu. It will select mode Fast 50."""
    logging.debug('Program Started. Press Ctrl-C to abort at any time.')
    getGameRegion()
    navigateStartGameMenu()
    setupCoordinates()
    startPlaying()
    #debugClickAllField()


def shortPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)



def getGameRegion():
    """Obtains the region that the game is played in."""
    global GAME_REGION

    # identify the top-left corner
    logging.debug('Finding game region...')

    region = pyautogui.locateOnScreen(shortPath('start_menu.png'))
    if region is None:
      raise Exception('Could not find game on screen. Is the game visible?')

    # calculate the region of the entire game
    topLeftX = region[0] # left
    topLeftY = region[1] - 220 # top - cropped of rest 220 px
    GAME_REGION = (topLeftX, topLeftY, 640, 480) # the game screen is always 640 x 480
    logging.debug('Game region found: %s' % (GAME_REGION,))


def navigateStartGameMenu():
    """Performs the clicks to navigate form the start screen to the beginning of the first level."""


    # click on Fast 50
    logging.debug('Clicking on the Fast 50 game mode...')
    pos_x = GAME_REGION[0] + 430 # 430 x in the starting menu
    pos_y = GAME_REGION[1] + 320 # 320 y in the starting menu
    pyautogui.moveTo(pos_x, pos_y, duration=1) # one click seems not to work
    while True:
        checkSucces = pyautogui.locateOnScreen(shortPath('start_menu_cropped.png'), region = GAME_REGION)
        if checkSucces is None:
            break
        pyautogui.click()
        logging.debug('Trying to click menu')

    logging.debug('Clicked on the right game mode.')

    # click on Continue
    pos_x = GAME_REGION[0] + 310 # 310 x in the starting menu
    pos_y = GAME_REGION[1] + 370 # 380 y in the starting menu
    pyautogui.moveTo(pos_x, pos_y, duration=1)
    while True:
        checkSucces = pyautogui.locateOnScreen(shortPath('ready.png'),region = GAME_REGION)
        if checkSucces is None:
            break
        pyautogui.click()
        logging.debug('Trying to click Begin')

    logging.debug('Clicked on Begin button.')

def setupCoordinates():
    """Setup the game field. It looks like this

    X|X|X|X
    -------
    X|X|X|X
    -------
    X|X|X|X
    -------
    X|X|X|X

    """
    FieldSizeX = 77 # the size of the fields x
    FieldSizeY = 118 # the size of the fields y
    FieldMidX = int(FieldSizeX/2) # the middle of the fields x
    FieldMidY = int(FieldSizeY/2) # the middle of the fields y
    #black_bar_size_x = 3 #
    #black_bar_size_y = 2 # maybe needed
    StartGameAreaX = GAME_REGION[0] + 162 # StartGameAreaX=Gameregion_x+blackbar_lef
    StartGameAreaY = GAME_REGION[1] + 1 # StartGameAreaY=Gameregion_y+blackbar_top
    StartGameAreaXRel = 162 # relative starting point in the screenshot
    StartGameAreaYRel = 1  # relative starting point in the screenshot
    global FIELDS
    # pos_abs is the absolute position of the field on your screen
    # pos_rel is the relative position of the field in the screenshot
    FIELDS = {'f11': {'pos_abs': (StartGameAreaX + FieldMidX, StartGameAreaY + FieldMidY), 'pos_rel': (StartGameAreaXRel + FieldMidX, StartGameAreaYRel + FieldMidY),'color': None}, #
              'f12': {'pos_abs': (StartGameAreaX + FieldSizeX + FieldMidX, StartGameAreaY + FieldMidY), 'pos_rel': (StartGameAreaXRel + FieldSizeX + FieldMidX, StartGameAreaYRel + FieldMidY), 'color': None},  ## Row 1
              'f13': {'pos_abs': (StartGameAreaX + 2*FieldSizeX + FieldMidX, StartGameAreaY + FieldMidY), 'pos_rel': (StartGameAreaXRel + 2*FieldSizeX + FieldMidX, StartGameAreaYRel + FieldMidY), 'color': None},  ##
              'f14': {'pos_abs': (StartGameAreaX + 3*FieldSizeX + FieldMidX, StartGameAreaY + FieldMidY), 'pos_rel': (StartGameAreaXRel + 3*FieldMidX, StartGameAreaYRel + FieldMidY),'color': None},
              #
              'f21': {'pos_abs': (StartGameAreaX + FieldMidX, StartGameAreaY + FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + FieldMidX, StartGameAreaYRel + FieldMidY),'color': None},
              'f22': {'pos_abs': (StartGameAreaX + FieldSizeX + FieldMidX, StartGameAreaY + FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + FieldSizeX + FieldMidX, StartGameAreaYRel + FieldSizeY + FieldMidY),'color': None},  ## Row 2
              'f23': {'pos_abs': (StartGameAreaX + 2*FieldSizeX + FieldMidX, StartGameAreaY + FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + 2*FieldSizeX + FieldMidX, StartGameAreaYRel + FieldSizeY + FieldMidY),'color': None},
              'f24': {'pos_abs': (StartGameAreaX + 3*FieldSizeX + FieldMidX, StartGameAreaY + FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + 3*FieldSizeX + FieldMidX, StartGameAreaYRel + FieldSizeY + FieldMidY),'color': None},

              'f31': {'pos_abs': (StartGameAreaX + FieldMidX, StartGameAreaY + 2*FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + FieldMidX, StartGameAreaYRel + 2*FieldSizeY + FieldMidY),'color': None},
              'f32': {'pos_abs': (StartGameAreaX + FieldSizeX + FieldMidX, StartGameAreaY + 2*FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + FieldSizeX + FieldMidX, StartGameAreaYRel + 2*FieldSizeY + FieldMidY),'color': None}, ## Row 3
              'f33': {'pos_abs': (StartGameAreaX + 2*FieldSizeX + FieldMidX, StartGameAreaY + 2*FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + 2*FieldSizeX + FieldMidX, StartGameAreaYRel + 2*FieldSizeY + FieldMidY),'color': None},
              'f34': {'pos_abs': (StartGameAreaX + 3*FieldSizeX + FieldMidX, StartGameAreaY + 2*FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + 3*FieldSizeX + FieldMidX, StartGameAreaYRel + 2*FieldSizeY + FieldMidY),'color': None},

              'f41': {'pos_abs': (StartGameAreaX + FieldMidX, StartGameAreaY + 3*FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + FieldMidX, StartGameAreaYRel + 3*FieldSizeY + FieldMidY),'color': None},
              'f42': {'pos_abs': (StartGameAreaX + FieldSizeX + FieldMidX, StartGameAreaY + 3*FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + FieldSizeX + FieldMidX, StartGameAreaYRel + 3*FieldSizeY + FieldMidY),'color': None}, ## Row 4
              'f43': {'pos_abs': (StartGameAreaX + 2*FieldSizeX + FieldMidX, StartGameAreaY + 3*FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + 2*FieldSizeX + FieldMidX, StartGameAreaYRel + 3*FieldSizeY + FieldMidY),'color': None},
              'f44': {'pos_abs': (StartGameAreaX + 3*FieldSizeX + FieldMidX, StartGameAreaY + 3*FieldSizeY + FieldMidY), 'pos_rel': (StartGameAreaXRel + 3*FieldSizeX + FieldMidX, StartGameAreaYRel + 3*FieldSizeY + FieldMidY),'color': None},}


    LEVEL = 1

def debugClickAllField():
  for key, value in FIELDS.items(): # go through all entries in the dict
      pos = value
      pyautogui.moveTo(pos)
      time.sleep(1)

def startPlaying():
  getFieldColor()
  findSingleField()
  #clickField()

def getFieldColor():
  im = pyautogui.screenshot(region=GAME_REGION)
  colorList = []
  for key, value in FIELDS.items():
      value['color'] = im.getpixel(value['pos_rel'])
      logging.debug('Got the color for the field' )
      logging.debug(value['color'])
  logging.debug(colorList)

def findSingleField():
    for key, value in FIELDS.items():
        n = su

def clickField(pos):
    pyautogui.click(pos)


if __name__ == '__main__':
    main()
