from time import time
from Quartz import *
from keycodes import keys, reverse
import sys

# =========== constants you can mess with ===========

LEFT_STICK = keys.ANSI_F
RIGHT_STICK = keys.ANSI_J
END = keys.Return

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

    if keycode in (LEFT_STICK, RIGHT_STICK) and etype is etype_pressed:
        record()

    if keycode == END and etype is etype_pressed:
        raise Eject()

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



times = []
prev = None

def record():
    global prev

    if prev is None:
        prev = time()
        return

    split = time()
    sys.stdout.write('%.3f'%(split-prev) + ', ')
    sys.stdout.flush()
    prev = split


try:
    enterWatchLoop()
except Eject:
    print