import random
#------------------------------[FUNCTION]------------------------------------
#Xây dựng hàm đọc dữ liệu - READ DATA
def Data(value):
    nj = len(value)         #số Job
    no = len(value[0])      #Số thao tác mỗi Job
    nm = len(value[0][0])   #Số máy
    D = [[[0 for k in range(nm)] for j in range(no)] for i in range(nj)]
    for i in range(nj):
        for j in range(no):
            for k in range(nm):
                D[i][j][k] = value[i][j][k]
    return D
#Xây dựng hàm tìm kiếm địa phương - APPROACH BY LOCALIZATION
def gen(Data):
    x = len(Data)
    y = len(Data[0])
    z = len(Data[0][0])
    D2 = [[[D[i][j][k] for k in range(z)] for j in range(y)] for i in range(x)]
    S = [[[0 for k in range(z)] for j in range(y)] for i in range(x)]
    for i in range(x):
        for j in range(y):
            if min(D2[i][j]) >= 99:
                continue
            Min = 99
            r = random.randint(0, z-1)
            position = 1
            for k in range(r, z):
                if D2[i][j][k] < Min:
                    Min = D2[i][j][k]
                    position = k
            for k in range(r):
                if D2[i][j][k] < Min:
                    Min = D2[i][j][k]
                    position = k
            S[i][j][position] = 1
            for q in range(j+1, y):
                D2[i][q][position] = D2[i][q][position] + D[i][j][position]
            for w in range(i+1, x):
                for q in range(y):
                    D2[w][q][position] = D2[w][q][position] + D[i][j][position]
    return S
class JSP:
    def __init__(self, gen):
        self.gen = gen
    #Xây dựng biểu đồ kế hoạch - ASSIGNMENT SCHEMATA
    def schemata(self):
        S = self.gen
        x = len(S)
        y = len(S[0])
        z = len(S[0][0])
        t = [0]*x
        m = [0]*z
        Wk = [0]*z
        S2 = [[[0 for k in range(z)] for j in range(y)] for i in range(x)]
        for j in range(y):
            for i in range(x):
                for k in range(z):
                    if S[i][j][k] == 1:
                        S2[i][j][k] = (max(t[i], m[k]), max(t[i], m[k]) + D[i][j][k])
                        t[i] = max(t[i], m[k]) + D[i][j][k]
                        m[k] = max(t[i], m[k])
                        Wk[k] = Wk[k] + D[i][j][k]
        for i in range(x):
            for j in range(y):
                print(f"J{[i+1]}{[j+1]}:", S2[i][j])
    #Xây dựng hàm đánh giá - EVALUATION
    def makespans(self):
        S = self.gen
        x = len(S)
        y = len(S[0])
        z = len(S[0][0])
        t = [0]*x
        m = [0]*z
        Wk = [0]*z
        S2 = [[[0 for k in range(z)] for j in range(y)] for i in range(x)]
        for j in range(y):
            for i in range(x):
                for k in range(z):
                    if S[i][j][k] == 1:
                        S2[i][j][k] = (max(t[i], m[k]), max(t[i], m[k]) + D[i][j][k])
                        t[i] = max(t[i], m[k]) + D[i][j][k]
                        m[k] = max(t[i], m[k])
                        Wk[k] = Wk[k] + D[i][j][k]
        return max(t)
    def processing_time(self):
        S = self.gen
        x = len(S)
        y = len(S[0])
        z = len(S[0][0])
        t = [0]*x
        m = [0]*z
        Wk = [0]*z
        S2 = [[[0 for k in range(z)] for j in range(y)] for i in range(x)]
        for j in range(y):
            for i in range(x):
                for k in range(z):
                    if S[i][j][k] == 1:
                        S2[i][j][k] = (max(t[i], m[k]), max(t[i], m[k]) + D[i][j][k])
                        t[i] = max(t[i], m[k]) + D[i][j][k]
                        m[k] = max(t[i], m[k])
                        Wk[k] = Wk[k] + D[i][j][k]
        return t
    def workloads(self):
        S = self.gen
        x = len(self.Data)
        y = len(self.Data[0])
        z = len(self.Data[0][0])
        t = [0]*x
        m = [0]*z
        Wk = [0]*z
        S2 = [[[0 for k in range(z)] for j in range(y)] for i in range(x)]
        for j in range(y):
            for i in range(x):
                for k in range(z):
                    if S[i][j][k] == 1:
                        S2[i][j][k] = (max(t[i], m[k]), max(t[i], m[k]) + D[i][j][k])
                        t[i] = max(t[i], m[k]) + D[i][j][k]
                        m[k] = max(t[i], m[k])
                        Wk[k] = Wk[k] + D[i][j][k]
            for i in range(x):
                W = W + Wk[i]
        return W
# Xay dung quan the
def chromosome(Data_Input,target,loop):
    nE = [[0 for k in range(2)] for j in range(target)]
    x = len(Data_Input)
    y = len(Data_Input[0])
    z = len(Data_Input[0][0])
    n = 0
    n_while = 0
    while n< target:
        if n == 0:
            nE[n][0] = gen(Data_Input)
            n = n+1
        else:
            size = 0
            compare = 0
            value = gen(Data_Input)
            for l in range(0,n):
                for i in range(x):
                    for j in range(y):
                        for k in range(z):
                            if value[i][j][k] == nE[l][0][i][j][k]:
                                size = size + 1
                if size == x*y*z:
                    compare = compare +1
                else:
                    size = 0
            if compare == 0:
                nE[n][0] = value
                n = n+1
            else:
                n_while = n_while + 1
        if n_while == loop:
            break
    E = [[0 for k in range(2)] for j in range(n)]
    for i in range(n):
        E[i][0] = nE[i][0]
    for i in range(n):
        a = JSP(E[i][0])
        E[i][1] = a.makespans()
    E1 = sorted(E, key=lambda tup: tup[1])
    return E1

#Xay dung ham Crossover
def crossover(D,E):
    a = random.randint(0,len(E)-1)
    b = random.randint(0,len(E)-1)
    while a == b:
        b = random.randint(0,len(E)-1)
    S1 = E[a][0]
    S2 = E[b][0]
    # Lựa chọn vị trí lai ghép
    i1 = i2 = j1 = j2 = 0
    while i1 >= i2:
        i1 = random.randint(0,len(D)-1)
        i2 = random.randint(0,len(D)-1)
        j1 = random.randint(0,len(D[0])-1)
        j2 = random.randint(0,len(D[0])-1)
        while i1 == i2 and j1 > j2:
            j1 = random.randint(0,len(D[0])-1)
            j2 = random.randint(0,len(D[0])-1)
    C1 = [[[0 for k in range(len(D[0][0]))] for j in range(len(D[0]))] for i in range(len(D))]
    C2 = [[[0 for k in range(len(D[0][0]))] for j in range(len(D[0]))] for i in range(len(D))]
    for a in range(0, i1):
        C1[a] = S2[a]
        C2[a] = S1[a]
    for a in range(i1+1, i2):
        C1[a] = S1[a]
        C2[a] = S2[a]
    for a in range(i2+1, len(D)):
        C2[a] = S1[a]
        C1[a] = S2[a]
    if i1 < i2:
        for b in range(0,j1):
            C1[i1][b] = S2[i1][b]
            C2[i1][b] = S1[i1][b]
        for b in range(j1,len(D[0])):
            C1[i1][b] = S1[i1][b]
            C2[i1][b] = S2[i1][b]
        for b in range(0,j2+1):
            C1[i2][b] = S1[i2][b]
            C2[i2][b] = S2[i2][b]
        for b in range(j2+1,len(D[0])):
            C1[i2][b] = S2[i2][b]
        C2[i2][b] = S1[i2][b]
    return [C1,C2]
# Xây dựng hàm đột biến
def mutation1(E):
    a = random.randint(0,len(E)-1)
    S = E[a][0]
    value_S = JSP(S)
    t = value_S.processing_time()
    print("Processing Time per Jobs:", t)
    max_pt = max(t)
    i = t.index(max_pt)
    print("jobs have processing time max:", i+1)
#-----------------------------[MAIN]--------------------------------------------------------
values = [
        [   # Layer 0
            [1, 3, 4, 1],
            [3, 8, 2, 1],
            [3, 5, 4, 7]
        ],
        [   # Layer 1
            [4, 1, 1, 4],
            [2, 3, 9, 3],
            [9, 1, 2, 2]
        ],
        [   # Layer 2
            [8, 6, 3, 5],
            [4, 5, 8, 1],
            [99, 99, 99, 99]
        ]
    ]
n = 10
D = Data(values)    #Đưa dữ liệu vào mảng D
E = chromosome(D,100,1000)    #Xây dựng quần thể (bộ nhiễm sắc thể choromosome(dữ liệu vào, số lượng gen mong muốn, số vòng lặp random))
P1 = E[:n]
C = [0 for k in range(n)]
for i in range(0,n,2):
    F = crossover(D,P1)
    C[i] = F[0]
    C[i+1] = F[1]
mutation1(P1)
#-----------------------------[END]---------------------------------------------------------