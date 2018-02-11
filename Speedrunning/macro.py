from time import time, sleep
from Quartz import *
from keycodes import keys, reverse
import pickle

# =========== constants you can mess with ===========

RESET = keys.Space
GO = (keys.ANSI_D, keys.ANSI_A)
KEY_FOR_QUIT = keys.ANSI_P

# ===========

times = {
    0:(keys.ANSI_D, True),

}


etype_pressed = 10
etype_released = 11

class Eject(Exception):
    """i dunno how to break from i/o loop otherwise"""

class globals:
    current_run = None
    space_pressed = False
    running = False

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

    if keycode is RESET and etype is etype_pressed and not globals.space_pressed:
        globals.current_run.reset()
        globals.space_pressed = True
    if keycode is RESET and etype is etype_released:
        globals.space_pressed = False
    if keycode in GO and etype:
        globals.current_run.start_split()
    if keycode is KEY_FOR_QUIT and etype is etype_released:
        globals.current_run.save()

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




class Run:

    def begin(self):
        globals.current_run = self
        self.start = None
        self.splits = []
        print('begin!')
        try:
            enterWatchLoop()
        except Eject:
            pass


    def reset(self):
        if self.start is not None and globals.running:
            split = time() - self.start
            print(split)
            self.splits.append(split)
            globals.running = False

    def start_split(self):
        if not globals.running:
            self.start = time()
            globals.running = True

    def save(self):
        print(', '.join(map(str, self.splits)))
        exit()

def open_game(name):
    game = pickle.load(open(name, 'r'))
    print()
    Run().begin(game)


Run().begin()
