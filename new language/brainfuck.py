import sys

def run(bf):
    stack = []
    link = {}
    for i,c in enumerate(bf):
        if c == '[':
            stack.append(i)
        elif c == ']':
            start, end = stack.pop(), i
            link[start] = end
            link[end] = start

    tape = [0 for _ in range(1000)]
    cell = 50
    instr = 0

    while instr < len(bf):
        code = bf[instr]

        if   code == '>': cell += 1
        elif code == '<': cell -= 1
        elif code == '+': tape[cell] += 1
        elif code == '-': tape[cell] -= 1
        elif code == ',': tape[cell] = ord(sys.stdin.read(1))
        elif code == '.': sys.stdout.write(chr(tape[cell]))
        elif code == ']['[not tape[cell]]:
            instr = link[instr]
        elif code == '!':
            print(tape[40:60])

        instr += 1



# run('++++++[>++++++++++++<-]>.>++++++++++[>++++++++++<-]>+.+++++++..+++.>++++[>+++++++++++<-]>.<+++[>----<-]>.<<<<<+++[>+++++<-]>.>>.+++.------.--------.>>+.')
run('--<-<<+[!+[!<+>--->->->-<<<]>]<<--.<++++++.<<-..<<.<+.>>.>>.<<<.+++.>>.>>-.<<<+.')

"""
link >> dict





"""


