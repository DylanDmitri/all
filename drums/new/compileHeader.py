inputFile = "midi_pattern.txt"
outputFile = "patterns.txt"

drums = 'cymbal','snare','tom1','tom2','tom_floor','bass','hi_hat'

delays = dict(
    cymbal=(65,),
    snare=(65,65),
    tom1=(65,65),
    tom2=(65,65),
    tom_floor=(65,65),
    bass=(65,),
    hi_hat=(65,65),
)

fin = open(inputFile,'r')
fout = open(outputFile,'w')

fout.writelines(r'//all patterns' + '\n')

outputLengths = []
outputs = []

