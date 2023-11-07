import random
# The algorithm uses data from the beginning of the lesson to select operations on machines.
# The output data marks the machines selected for each operation
# The following two algorithms are mentioned in the article: Imed Kacem, Slim Hammadi
# "Approach by Localization and Multiobjective Evolutionary Optimization for Flexible Job-Shop Scheduling Problems", 2002
# Assignment_Procedure 1
def gen1(gen1_data,limited_value1):
    x = len(gen1_data)
    y = len(gen1_data[0])
    z = len(gen1_data[0][0])
    D1 = [[[gen1_data[i][j][k] for k in range(z)] for j in range(y)] for i in range(x)]
    S1 = [[[0 for k in range(z)] for j in range(y)] for i in range(x)]
    for i in range(x):
        for j in range(y):
            if min(D1[i][j]) >= limited_value1:
                continue
            Min = limited_value1
            r = random.randint(0, z-1)
            position = 1
            for k in range(r, z):
                if D1[i][j][k] < Min:
                    Min = D1[i][j][k]
                    position = k
            for k in range(r):
                if D1[i][j][k] < Min:
                    Min = D1[i][j][k]
                    position = k
            S1[i][j][position] = 1
            for q in range(j+1, y):
                D1[i][q][position] = D1[i][q][position] + gen1_data[i][j][position]
            for w in range(i+1, x):
                for q in range(y):
                    D1[w][q][position] = D1[w][q][position] + gen1_data[i][j][position]
    return S1
# Assignment_Procedure 2
def gen2(gen2_data,limited_value2):
    x = len(gen2_data)
    y = len(gen2_data[0])
    z = len(gen2_data[0][0])
    D2 = [[[gen2_data[i][j][k] for k in range(z)] for j in range(y)] for i in range(x)]
    S2 = [[[0 for k in range(z)] for j in range(y)] for i in range(x)]
    w = 1
    while w <= x*y:
        min = limited_value2
        r = random.randint(0,z-1)
        PositionK = r
        for i in range(len(D2)):
            for j in range(len(D2[i])):
                for k in range(r, z):
                    if D2[i][j][k] < min and D2[i][j][k] != 0:
                        min = D2[i][j][k]
                        PositionK = k
                        PositionI = i
                        PositionJ = j
                for k in range(0,r):
                    if D2[i][j][k] < min and D2[i][j][k] != 0:
                        min = D2[i][j][k]
                        PositionK = k
                        PositionI = i
                        PositionJ = j
        if min < limited_value2:
            S2[PositionI][PositionJ][PositionK] = 1
        D2[PositionI][PositionJ] = [0 for i in range(len(D2[0][0]))]
        for i in range(len(D2)):
            for j in range(len(D2[i])):
                if D2[i][j][PositionK] != 0:
                    D2[i][j][PositionK] = D2[i][j][PositionK] + gen2_data[PositionI][PositionJ][PositionK]
        w += 1
    return S2