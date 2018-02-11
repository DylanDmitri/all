
exam = False
hw = False
a = None

exams = []
hws = []

for line in open('grades', 'r'):
    if line.startswith('HW'):
        hw = True

    if line.startswith('Ex'):
        exam = True

    try:
        a = float(line.strip())
    except:
        pass

    if line.startswith('/'):
        if exam:
            exams.append(a / float(line[1:].strip()))
            exam = False
        elif hw:
            hws.append(a / float(line[1:].strip()))
            hw = False

for x in exams:
    print(x)


