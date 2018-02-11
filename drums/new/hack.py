import random

drumNum = {
        36: 0,
        38: 1,
        42: 2,
        51: 3,

        55: 0,
        57: 0,
        59: 0,
        60: 1,
        62: 2,
        64: 3,

        65: 2,
        67: 0,
        68: 0,
        69: 2,
        70: 2,
        71: 3,
        72: 3,
        73: 3,
        74: 0,
        75: 0,
        76: 1,
        77: 0,
        78: 1,
        79: 1,
        80: 1,
        81: 2,
        82: 2,
        83: 2,
        84: 2,
        85: 2,
        86: 2

    }

prev = 2000

class tumpo:
    def __init__(self):
        self.next_up = [None,None,None,None,None,None,None,None]
        self.sticks = [0, 0, 0, 0]
        self.note = None

    @property
    def next(self):
        return self.next_up[self.port]

    @property
    def port(self):
        return drumNum[self.note]*2 + self.stick

    @property
    def stick(self):
        return self.sticks[drumNum[self.note]]


def makeHeader(inputFile,outputFile='patterns.txt'):
    drums = 'cymbal','snare','tom1','tom2','tom_floor','bass','hi_hat'

    default = 70
    longer = 80
    delays = [59] * 20

    fin = open(inputFile,'r')
    fout = open(outputFile,'w')

    fout.writelines(r'//all patterns' + '\n')

    outputLengths = []
    output = []

    for pattern in fin:

        foo = tumpo()

        def extend_output(port,direction,time):
            global prev
            diff = time - prev
            prev = time
            port = {
                0: 2,
                1: 3,
                2: 4,
                3: 4,
                4: 6,
                5: 7,
                6: 8,
                7: 8,

            }[port]
            output.append("delay({});\ndigitalWrite({}, {});".format(diff, port, direction))

        for group in pattern.split(', '):
            note, timestamp = group.split(':')
            timestamp = (1*int(timestamp)) + 2000  # trim trailing comma
            foo.note = int(note)

            for i,potential in enumerate(foo.next_up):
                if potential is not None:
                    if potential[2] < timestamp:
                        extend_output(*potential)
                        foo.next_up[i] = None

            extend_output(foo.port, 'HIGH', timestamp)

            if foo.next is not None:
                raise Exception('stick already down, cannot make it go down again')

            try:
                foo.next_up[foo.port] = (foo.port,'LOW', timestamp + delays[foo.port])
            except:
                print('zoinks')

            foo.sticks[drumNum[foo.note]] = 0 if foo.sticks[drumNum[foo.note]] else 1

    fout.writelines('\n'.join(output))

makeHeader('gladiators.txt')
