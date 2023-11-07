import random
# The algorithm selects any two parents and crosses them together
def cross(data_cross,E_cross):
    a = random.randint(0,len(E_cross)-1)
    b = random.randint(0,len(E_cross)-1)
    while a == b:
        b = random.randint(0,len(E_cross)-1)
    S1 = E_cross[a][0]
    S2 = E_cross[b][0]
    # Select the point to crossover
    i1 = i2 = j1 = j2 = 0
    while i1 > i2:
        i1 = random.randint(0,len(data_cross)-1)
        i2 = random.randint(0,len(data_cross)-1)
        j1 = random.randint(0,len(data_cross[0])-1)
        j2 = random.randint(0,len(data_cross[0])-1)
        while i1 == i2 and j1 > j2:
            j1 = random.randint(0,len(data_cross[0])-1)
            j2 = random.randint(0,len(data_cross[0])-1)
    crossover1 = [[[0 for k in range(len(data_cross[0][0]))] for j in range(len(data_cross[0]))] for i in range(len(data_cross))]
    crossover2 = [[[0 for k in range(len(data_cross[0][0]))] for j in range(len(data_cross[0]))] for i in range(len(data_cross))]
    for a in range(0, i1):
        crossover1[a] = S2[a]
        crossover2[a] = S1[a]
    for a in range(i1+1, i2):
        crossover1[a] = S1[a]
        crossover2[a] = S2[a]
    for a in range(i2+1, len(data_cross)):
        crossover2[a] = S1[a]
        crossover1[a] = S2[a]
    if i1 < i2:
        for b in range(0,j1):
            crossover1[i1][b] = S2[i1][b]
            crossover2[i1][b] = S1[i1][b]
        for b in range(j1,len(data_cross[0])):
            crossover1[i1][b] = S1[i1][b]
            crossover2[i1][b] = S2[i1][b]
        for b in range(0,j2+1):
            crossover1[i2][b] = S1[i2][b]
            crossover2[i2][b] = S2[i2][b]
        for b in range(j2+1,len(data_cross[0])):
            crossover1[i2][b] = S2[i2][b]
            crossover2[i2][b] = S1[i2][b]
    if i1 == i2:
        for b in range(0,j1):
            crossover1[i1][b] = S2[i1][b]
            crossover2[i1][b] = S1[i1][b]
        for b in range(j1,j2+1):
            crossover1[i1][b] = S1[i1][b]
            crossover2[i1][b] = S2[i1][b]
        for b in range(j2+1,len(data_cross[0])):
            crossover1[i2][b] = S2[i2][b]
            crossover2[i2][b] = S1[i2][b]
    return [crossover1,crossover2]