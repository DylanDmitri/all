from mido import MidiFile
from collections import defaultdict

infile = 'gladiators.mid'
outfile = '.'.join(infile.split('.')[:-1]) + '.txt'

mid = MidiFile(infile)
commands = defaultdict(lambda:[])
for i, track in enumerate(mid.tracks):
    print()
    print('Track {}: {}'.format(i, track.name))
    current_time = 0
    for message in track:
        print(message)
        if message.time:
            current_time += message.time

        if message.type=='note_on' and message.velocity:  #if ur hitting
            commands['full'].append(str(message.note)+':'+str(current_time))

for note, times in commands.items():
    print(note, times)

patterns = [commands[key] for key in sorted(commands.keys())]

open(outfile, 'w').write('\n'.join(', '.join(map(str, pattern)) for pattern in patterns))
