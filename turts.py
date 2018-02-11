data = list("""
0000	00	0	1	0	1
0000	01	0	0	1	0
0000	10	0	0	0	1
0000	11	0	0	0	0
0001	00	0	1	1	0
0001	01	0	0	1	1
0001	10	0	0	1	0
0001	11	0	0	0	0
0010	00	0	1	1	1
0010	01	0	1	0	0
0010	10	0	0	1	1
0010	11	0	0	0	0
0011	00	1	0	0	0	1	0	0
0011	01	0	1	0	1
0011	10	0	1	0	0
0011	11	0	0	0	0
0100	00	1	0	0	1
0100	01	0	1	1	0
0100	10	0	1	0	1
0100	11	0	0	0	0
0101	00	1	0	1	0
0101	01	0	1	1	1
0101	10	0	1	1	0
0101	11	0	0	0	0
0110	00	1	0	1	1	0	1	0
0110	01	1	0	0	0	1	0	0
0110	10	0	1	1	1
0110	11	0	0	0	0
0111	00	1	1	0	0
0111	01	1	0	0	1
0111	10	1	0	0	0	1	0	0
0111	11	0	0	0	0
1000	00	1	0	0	0	1	0	0
1000	01	1	0	0	0	1	0	0
1000	10	1	0	0	0	1	0	0
1000	11	0	0	0	0
1001	00	1	1	1	0
1001	01	1	0	1	1	0	1	0
1001	10	1	0	1	0
1001	11	0	0	0	0
1010	00	1	1	1	1	0	0	1
1010	01	1	1	0	0
1010	10	1	0	1	1	0	1	0
1010	11	0	0	0	0
1011	00	1	0	1	1	0	1	0
1011	01	1	0	1	1	0	1	0
1011	10	1	0	1	1	0	1	0
1011	11	0	0	0	0
1100	00	1	1	1	1	0	0	1
1100	01	1	1	1	0
1100	10	1	1	0	1
1100	11	0	0	0	0
1101	00	1	1	1	1	0	0	1
1101	01	1	1	1	1	0	0	1
1101	10	1	1	1	0
1101	11	0	0	0	0
1110	00	1	1	1	1	0	0	1
1110	01	1	1	1	1	0	0	1
1110	10	1	1	1	1	0	0	1
1110	11	0	0	0	0
1111	00	1	1	1	1
1111	01	1	1	1	1
1111	10	1	1	1	1
1111	11	0	0	0	0""".strip().split('\n'))


gap = 41.15
dotsize = 12

import turtle

turtle._CFG['width'] = 1152
turtle._CFG['height'] = 2000

jeb = turtle.Turtle()

jeb.pensize(20)
jeb.penup()
jeb.speed(0)

def badot():
    pass
    jeb.dot(dotsize,'red')

def show(rows):

    gy = 440

    for row in rows:

        jeb.setpos(-440,gy)

        args = row.split('\t')
        while len(args) < 9:
            args.append('0')

        firstbit = args[0]+args[1]
        secondbit = ''.join(args[2:])

        for c in firstbit:
            if int(c):
                jeb.dot(dotsize,'black')
            else:
                badot()
            jeb.forward(gap)
            if not int(c):
                jeb.dot(dotsize,'black')
            else:
                badot()
            jeb.forward(gap)


        jeb.forward(14+gap*3)

        for c in secondbit:
            if int(c):
                jeb.dot(dotsize,'black')
            else:
                badot()
            jeb.forward(gap)

        gy -= 39+14.65

for group in range(4):
    show(data[group*16:(group+1)*16])
    input()
    jeb.clear()

turtle.done()

