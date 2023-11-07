import random
import copy
import AL
import ortool as Or
import crossover as Cr
import mutation as Mu

#------------------------------[FUNCTION]------------------------------------

def Data(input_value):
    nj = len(input_value)         #số Job
    no = len(input_value[0])      #Số thao tác mỗi Job
    nm = len(input_value[0][0])   #Số máy
    RD = [[[0 for k in range(nm)] for j in range(no)] for i in range(nj)]
    for i in range(nj):
        for j in range(no):
            for k in range(nm):
                RD[i][j][k] = input_value[i][j][k]
    return RD

def chromosome(Data_Input,loop):
    nE = []
    n = 0
    n2 = 0
    while n < loop:
        EE = []
        EE = AL.gen1(Data_Input,99)
        if EE not in nE :
            nE.append(EE)
            n = 0
        else:
            n += 1
    while n2 < loop:
        EE = []
        EE = AL.gen2(Data_Input,99)
        if EE not in nE :
            nE.append(EE)
            n2 = 0
        else:
            n2 += 1
    E_chromosome = [[0 for k in range(2)] for j in range(len(nE))]
    for i in range(len(nE)):
        E_chromosome[i][0] = nE[i]
        ec = Or.format_data(E_chromosome[i][0],Data_Input)
        a = Or.JSP_OR(ec)
        E_chromosome[i][1] = a.makespans()
    E_chromosome1 = sorted(E_chromosome, key=lambda tup: tup[1])
    return E_chromosome1

def Genetic_Algorithms(Data_in,population_size,generation,crossover_probability,mutation1_probability,mutation2_probability):
    D = Data(Data_in)    #Đưa dữ liệu vào mảng D
    E = chromosome(D,1000)    #Xây dựng quần thể (bộ nhiễm sắc thể choromosome(dữ liệu vào, số lượng gen mong muốn, số vòng lặp random))
    
    c = int(population_size*crossover_probability)
    m1 = int(population_size*mutation1_probability)
    m2 = int(population_size*mutation2_probability)

    Q = E
    x = 1
    while x <= generation:
        QQ = copy.deepcopy(Q)

        #Lai ghép
        C1 = [0 for j in range(c)]
        for i in range(0,c,2):
            F = Cr.cross(D,Q)
            C1[i] = F[0]
            C1[i+1] = F[1]

        #Đột biến kiểu 1
        M1 = [0 for j in range(m1)]
        for i in range(m1):
            M1[i] = Mu.mutation1(C1,D)

        #Đột biến kiểu 2
        M2 = [0 for j in range(m2)]
        for i in range(m2):
            M2[i] = Mu.mutation2(C1,D)

        #Gộp các tổ hợp
        C1.extend(M1)
        C1.extend(M2)
        # Tạo mảng Q2 bao gồm cả chỉ số đánh giá Makespans
        Q2 = [[0 for j in range(2)] for k in range(population_size)]
        for i3 in range(len(Q2)):
            Q2[i3][0] = C1[i3]
            q2f = Or.format_data(Q2[i3][0],D)
            Q2[i3][1] = Or.JSP_OR(q2f).makespans()
        # Gộp G2 vào tập quần thể ban đầu
        Q2.extend(QQ)
        # Sắp xếp các phần tử tỏng Q2 theo thứ tự tăng dần Cmax
        QQ2 = sorted(Q2, key=lambda tup: tup[1])
        # Loại bỏ các phần tử giống nhau trong QQ2 lưu vào QQ3
        QQ3 = []
        for element in QQ2:
            if element not in QQ3:
                QQ3.append(element)
        # Lấy n phần tử đầu của QQ3 thay vào Q
        Q = QQ3[:population_size]
        x += 1
    Assignment = Q[0][0]
    Assf = Or.format_data(Assignment,D)
    print("________________________BEST SOLUTION_____________________")
    for i in range(len(Assf)):
        print(Assf[i])
    Or.JSP_OR(Assf).scheduling()
    print("Makespans : = ", Or.JSP_OR(Assf).makespans())
    print("Workloads : = ", Or.JSP_OR(Assf).workloads())
    print("Workloads per Machines : = ", Or.JSP_OR(Assf).workloads_per_machine())
    print("Time per Jobs : = ", Or.JSP_OR(Assf).processing_time())
#-----------------------------[MAIN]--------------------------------------------------------
values = [
    [   # Job 1
        [1,4,6,9,3,5,2,8,9,5],
        [4,1,1,3,4,8,10,4,11,4],
        [3,2,5,1,5,6,9,5,10,3]
    ],
    [   # Job 2
        [2,10,4,5,9,8,4,15,8,4],
        [4,8,7,1,9,6,1,10,7,1],
        [6,11,2,7,5,3,5,14,9,2]
    ],
    [   # Job 3
        [8,5,8,9,4,3,5,3,8,1],
        [9,3,6,1,2,6,4,1,7,2],
        [7,1,8,5,4,9,1,2,3,4]
    ],
    [   # Job 4
        [5,10,6,4,9,5,1,7,1,6],
        [4,2,3,8,7,4,6,9,8,4],
        [7,3,12,1,6,5,8,3,5,2]
    ],
    [   # Job 5
        [7,10,4,5,6,3,5,15,2,6],
        [5,6,3,9,8,2,8,6,1,7],
        [6,1,4,1,10,4,3,11,13,9]
    ],
    [   # Job 6
        [8,9,10,8,4,2,7,8,3,10],
        [7,3,12,5,4,3,6,9,2,15],
        [4,7,3,6,3,4,1,5,1,11]
    ],
    [   # Job 7
        [1,7,8,3,4,9,4,13,10,7],
        [3,8,1,2,3,6,11,2,13,3],
        [5,4,2,1,2,1,8,14,5,7]
    ],
    [   # Job 8
        [5,7,11,3,2,9,8,5,12,8],
        [8,3,10,7,5,13,4,6,8,4],
        [6,2,13,5,4,3,5,7,9,5]
    ],
    [   # Job 9
        [3,9,1,3,8,1,6,7,5,4],
        [4,6,2,5,7,3,1,9,6,7],
        [8,5,4,8,6,1,2,3,10,12]
    ],
    [   # Job 10
        [4,3,1,6,7,1,2,6,20,6],
        [3,1,8,1,9,4,1,4,17,15],
        [9,2,4,2,3,5,2,4,10,23]
    ]
]

Genetic_Algorithms(values,100,100,0.8,0.1,0.1)
#-----------------------------[END]---------------------------------------------------------