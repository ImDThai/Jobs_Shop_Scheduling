import random
import ortool

def mutation1(gen_input1,Data_input_mu):
    a = random.randint(0,len(gen_input1)-1)
    S_mutation1 = gen_input1[a]
    sm = ortool.format_data(S_mutation1,Data_input_mu)
    value_S = ortool.JSP_OR(sm)
    t = value_S.processing_time()
    max_pt = max(t)
    i = t.index(max_pt)
    r = 0
    j = 0
    while j < len(S_mutation1[0]) and r == 0:
        position = 0
        for k1 in range(len(S_mutation1[0][0])):
            if S_mutation1[i][j][k1] == 1:
                position = k1
        for k2 in range(len(S_mutation1[0][0])):
            if Data_input_mu[i][j][k2] < Data_input_mu[i][j][position]:
                S_mutation1[i][j][position] = 0
                S_mutation1[i][j][k2] = 1
                r = 1
        j += 1
    return S_mutation1
# Xây dựng hàm đột biến 2
def mutation2(gen_input2,Data_input_m2):
    a = random.randint(0,len(gen_input2)-1)
    S_mutation2 = gen_input2[a]
    sm2 = ortool.format_data(S_mutation2,Data_input_m2)
    value_S = ortool.JSP_OR(sm2)
    w = value_S.workloads_per_machine()
    max_wl = max(w)
    indices_of_max = [o for o, x in enumerate(w) if x == max_wl]
    min_wl = min(w)
    indices_of_min = [o for o, x in enumerate(w) if x == min_wl]
    k1 = random.choice(indices_of_max)
    k2 = random.choice(indices_of_min)
    r = 0
    while r == 0:
        i = random.randint(0,len(S_mutation2)-1)
        position = random.randint(0,len(S_mutation2[0])-1)
        for j in range(position,len(S_mutation2[0])):
            if S_mutation2[i][j][k1] == 1:
                r = 1
                positioni = i
                positionj = j
            else:
                r = 0
        if r == 0:
            for j in range(0, position):
                if S_mutation2[i][j][k1] == 1:
                    r = 1
                    positioni = i
                    positionj = j
                else:
                    r = 0
    S_mutation2[positioni][positionj][k1] = 0
    S_mutation2[positioni][positionj][k2] = 1
    return S_mutation2