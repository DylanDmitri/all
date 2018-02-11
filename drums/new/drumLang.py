
def port(note, stick):
    num = {
        36: 0,
        38: 0,
        42: 1,
        51: 2,
    }
    return num[note]+stick

def makeHeader(inputFile,outputFile='patterns.h'):
    drums = 'cymbal','snare','tom1','tom2','tom_floor','bass','hi_hat'

    default = 65
    longer = 100
    delays = dict(
        cymbal=(default,),
        snare=(default,default),
        tom1=(longer,longer),
        tom2=(longer,longer),
        tom_floor=(default,default),
        bass=(default,),
        hi_hat=(default,default),
    )

    fin = open(inputFile,'r')
    fout = open(outputFile,'w')

    fout.writelines(r'//all patterns' + '\n')

    outputLengths = []
    outputs = []

    for drumNum,pattern in enumerate(fin):
        drum = drums[drumNum]
        print(drum)

        output = []
        def extend_output(stick,direction,time):
            output.append("delay({});\ndigitalWrite({}, {})".format(time, port(note, stick), direction))

        next_up_stack = [None,None,None,None,None,None]
        stick = [0, 0, 0]

        for group in pattern.split(', '):
            note, timestamp = group.split(':')
            timestamp = int(timestamp) + 2000  # trim trailing comma

            for i,potential in enumerate(next_up_stack):
                if potential is not None:
                    if potential[2] < timestamp:
                        extend_output(*potential)
                        next_up_stack[i] = None

            extend_output(stick[note], 'LOW', timestamp)

            if next_up_stack[stick - 1] is not None:
                raise Exception('stick already down, cannot make it go down again')
            next_up_stack[port(note, stick[note])] = (stick,'HIGH',timestamp + delays[drum][stick[note] - 1])

            if port(note, stick) == 1:
                pass
            else:
                stick[note] = {0:1,1:0}[stick[note]]

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
    fout.writelines('const int lengths[numOfPatterns] = ' + lenArr + ';\n')

    fout.writelines('const unsigned long patterns[numOfPatterns][maxLength] PROGMEM = {\n')
    fout.writelines(',\n'.join(outputs))
    fout.writelines('\n};\n')

makeHeader('Jazz12.txt')