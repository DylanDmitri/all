from time import time
from Quartz import *
from keycodes import keys, reverse
import pickle

# =========== constants you can mess with ===========

KEY_FOR_SPLITS = keys.Space
KEY_FOR_RESET = keys.ANSI_R
KEY_FOR_QUIT = keys.ANSI_P
KEY_FOR_LV = keys.ANSI_L

START = 1 

# ===========



etype_pressed = 10
etype_released = 11

class Eject(Exception):
    """i dunno how to break from i/o loop otherwise"""

class globals:
    current_run = None
    space_pressed = False

def mean(nums):
    if len(nums) == 0: return float('inf')
    return sum(nums) / len(nums)

def dev(nums):
    m = mean(nums)
    return sum((a-m)**2 for a in nums)**.5

# This callback will be invoked every a key is pressed.
def eventCallBack(proxy, etype, event, refcon):
    # The incoming keycode.
    keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)

    # print reverse[keycode],
    # if etype is etype_pressed:
    #     print 'pressed'
    # elif etype is etype_released:
    #     print 'released'

    if keycode is KEY_FOR_SPLITS and etype is etype_pressed and not globals.space_pressed:
        globals.current_run.take_split()
        globals.space_pressed = True
    if keycode is KEY_FOR_SPLITS and etype is etype_released:
        globals.space_pressed = False
    if keycode is KEY_FOR_RESET and etype is etype_released:
        globals.current_run.reset()
    if keycode is KEY_FOR_QUIT and etype is etype_released:
        globals.current_run.save()
    if keycode is KEY_FOR_LV and etype is etype_released:
        globals.current_run.lv()

    return event

def enterWatchLoop():
    eventMask = (1 << kCGEventKeyDown) | (1 << kCGEventKeyUp)
    eventTap = CGEventTapCreate(kCGSessionEventTap,
                                kCGHeadInsertEventTap,
                                0,
                                eventMask,
                                eventCallBack,
                                None)

    if eventTap is None:
        raise Exception("hey maybe you wanna do this in sudo mode")

    runLoopSource = CFMachPortCreateRunLoopSource(kCFAllocatorDefault,
                                                  eventTap, 0)
    CFRunLoopAddSource(CFRunLoopGetCurrent(),
                       runLoopSource,
                       kCFRunLoopCommonModes)
    CGEventTapEnable(eventTap, True)
    CFRunLoopRun()



class Game:
    def __init__(self, name, levels, expected=None):
        self.name = name
        self.levels = levels + 1  # bad code
        self.expected = expected
        assert len(expected) == levels

        self.runs = []

    def savetimes(self, times):
        self.runs.append(times)

    def level_data(self, level):
        if not self.runs: return []
        return [run[level-1] for run in self.runs]




class Run:

    def begin(self, game, start_level=None, end_level=None):
        globals.current_run = self
        self.game = game

        self.p = 0
        self.dist = [[]]

        if start_level is None: start_level = START
        if end_level is None: end_level = game.levels

        self.start_level = start_level
        self.end_level = end_level
        self.reset()

        try:
            enterWatchLoop()
        except Eject:
            pass

    def take_split(self):
        newtime = time()

        if self.level == self.start_level:
            print('begin!')
            self.timestamp = time()

        else:
            split = newtime - self.splitstamp

            # to avoid double-tap space breaking stuff
            if split < 5: return

            if trialmode:
                print(split)
            else:

                target = self.game.expected[self.level-2] - (0 if self.start_level==1 else self.game.expected[self.start_level-2])

                print target,
                netdif = (newtime - self.timestamp) - target
                print "%.2f, %+.2f, %+.2f" % (
                      split, netdif, netdif - self.p)
                self.dist[-1].append(split)
                self.p = netdif

        self.level += 1
        self.splitstamp = newtime

        if self.level > self.end_level:
            print 'run complete - final time %.1f secs' % (self.timestamp-newtime)
            self.reset()

    def reset(self):
        print '\ninitializing to start\npress space to begin'
        self.level = self.start_level
        self.p = 0

        if self.dist[-1]:
            self.dist.append([])

    def lv(self):

        while True:
            try:
                self.start_level = int(input(': '))
                break
            except ValueError:
                print('not a number?')

        self.reset()


    def save(self):
        for row in self.dist:
            print('\t'.join('%.2f'%f for f in row))
        pickle.dump(self.game, open(self.game.name, 'w'))
        exit()

def open_game(name):
    game = pickle.load(open(name, 'r'))
    print()
    Run().begin(game)


def new_game(*args, **kwargs):
    Run().begin(Game(*args, **kwargs), start_level=START)


trialmode = False
real_splits = (
    16.75, 33.85, 47.30, 57.90, 76.52,
    94.15, 109.2, 135.2, 159.1, 173.2,
    193.2, 215.6, 235.2, 266.2, 289.7,
    318.8, 370.8, 395.0, 457.9, 476.7
)
my_splits = (
 15.75,32.85,46.3,56.9,75.52,93.15,106.2,132.2,156.1,170.2,
 186.7,209.1,225.7,256.7,280.2,309.3,361.3,385.5,448.4,467.2
)

new_game('final ninja', 20, expected = my_splits) 
# new_game('factorio demo', 3, expected = (100, 100, 100))
