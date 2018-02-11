inputFile = "patterns/Jazz12.txt"
outputFile = '../Master/patterns.h'

drums = 'cymbal','snare','tom1','tom2','tom_floor','bass','hi_hat'

default = 5
delays = dict(
    cymbal =    (default, ),
    snare =     (default, default),
    tom1 =      (default, default),
    tom2 =      (default, default),
    tom_floor = (default, default),
    bass =      (default, ),
    hi_hat =    (default, default),
)

fin = open(inputFile,'r')
fout = open(outputFile,'w')

fout.writelines(r'//all patterns' + '\n')

outputLengths = []
outputs = []

for drumNum,pattern in enumerate(fin):
    drum = drums[drumNum]

    input = pattern.split(',')
    beats = list(map(lambda x:int(x),input))

    stick = 1
    def switchStick():
        global stick

        if drum in ('cymbal','bass'):
            stick = 1
        else:
            stick = 2 if stick == 1 else 1


    output = []
    next_up_stack = [None, None]

    for timestamp in pattern.split(', '):
        timestamp = int(timestamp)  # trim trailing comma

        for i, potential in enumerate(next_up_stack):
            if potential is not None:
                if potential[2] < timestamp:
                    output.extend(potential)
                    print(potential)
                    next_up_stack[i] = None

        output.extend((stick, 0, timestamp))
        # print((stick, 0, timestamp))
        if next_up_stack[stick-1] is not None:
            raise Exception('stick already down, cannot make it go down again')
        next_up_stack[stick-1] = (stick, 1, timestamp+delays[drum][stick-1])

        switchStick()

    length = len(output)
    output = list(map(lambda x:str(x),output))
    output = ', '.join(output)
    output = '{' + output + '}'

    outputLengths.append(length)
    outputs.append('\t' + output)

fout.writelines('const int numOfPatterns = ' + str(len(outputs)) + ';\n')
fout.writelines('const int maxLength = ' + str(max(outputLengths)) + ';\n\n')

lenArr = list(map(lambda x:str(x),outputLengths))
lenArr = ', '.join(lenArr)
lenArr = '{' + lenArr + '}'
fout.writelines('const int lengths[numOfPatterns] PROGMEM = ' + lenArr + ';\n')

fout.writelines('const unsigned long patterns[numOfPatterns][maxLength] PROGMEM = {\n')
fout.writelines(',\n'.join(outputs))
fout.writelines('\n};\n')
