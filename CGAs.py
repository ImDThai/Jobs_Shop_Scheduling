import tkinter as tk
from tkinter import filedialog
import random
import copy
import AL
import ortool as Or
import crossover as Cr
import mutation as Mu
import numpy as np

#------------------------------[FUNCTION]------------------------------------
def Read_Data(filename='data.txt'):
    Structure_data = np.genfromtxt(filename, dtype=int, max_rows=1)
    Data = np.genfromtxt(filename, dtype = int, skip_header = 1)
    Data = Data.reshape(Structure_data[0], Structure_data[1], Structure_data[2])
    Data.tolist()
    return Data

def chromosome(Data_Input,loop,Gens_estimate):
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
        if len(nE) == Gens_estimate:
            n = loop
    while n2 < loop :
        EE = []
        EE = AL.gen2(Data_Input,99)
        if EE not in nE :
            nE.append(EE)
            n2 = 0
        else:
            n2 += 1
        if len(nE) == Gens_estimate:
            n2 = loop
    E_chromosome = [[0 for k in range(3)] for j in range(len(nE))]
    for i in range(len(nE)):
        E_chromosome[i][0] = nE[i]
        ec = Or.format_data(E_chromosome[i][0],Data_Input)
        a = Or.JSP_OR(ec)
        E_chromosome[i][1] = a.makespans()
        E_chromosome[i][2] = a.workloads()
    E_chromosome1 = sorted(E_chromosome, key=lambda sublist: (sublist[1], sublist[2]))
    return E_chromosome1

def Genetic_Algorithms(Data_in,population_size,generation,crossover_probability,mutation1_probability,mutation2_probability):
    D = Data_in    #Đưa dữ liệu vào mảng D
    E = chromosome(D,1000,1000)    #Xây dựng quần thể (bộ nhiễm sắc thể choromosome(dữ liệu vào, số lượng gen mong muốn, số vòng lặp random))
    
    c = int(population_size*crossover_probability)
    m1 = int(population_size*mutation1_probability)
    m2 = int(population_size*mutation2_probability)

    Q = E
    x = 1
    y = 0
    Cmax_find = 99999
    WL_find = 99999
    Assignment = [ 0 for i in range(100)]
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
        Q2 = [[0 for j in range(3)] for k in range(population_size)]
        for i3 in range(len(Q2)):
            Q2[i3][0] = C1[i3]
            q2f = Or.format_data(Q2[i3][0],D)
            Q2[i3][1] = Or.JSP_OR(q2f).makespans()
            Q2[i3][2] = Or.JSP_OR(q2f).workloads()
        # Gộp G2 vào tập quần thể ban đầu
        Q2.extend(QQ)
        # Sắp xếp các phần tử trong Q2 theo thứ tự tăng dần Cmax
        QQ2 = sorted(Q2, key=lambda sublist: (sublist[1], sublist[2]))
        # Loại bỏ các phần tử giống nhau trong QQ2 lưu vào QQ3
        QQ3 = []
        for element in QQ2:
            if element not in QQ3:
                QQ3.append(element)
        # Lấy n phần tử đầu của QQ3 thay vào Q
        Q = QQ3[:population_size]
        if Q[0][1] <= Cmax_find or Q[0][2] <= WL_find:
            Cmax_find = Q[0][1]
            WL_find = Q[0][2]
            Assf = Or.format_data(Q[0][0],D)
            WL = Or.JSP_OR(Assf).workloads_per_machine()
            if WL not in Assignment:
                Assignment.append(WL)
                Scheduling = Or.JSP_OR(Assf).scheduling()
                Makespans  =  Or.JSP_OR(Assf).makespans()
                Workloads = Or.JSP_OR(Assf).workloads()
                print(Scheduling)
                y += 1
        x += 1
#-----------------------------[MAIN]--------------------------------------------------------
class GeneticAlgorithmGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Genetic Algorithm Parameters")

        # Variables for input parameters
        self.filename = tk.StringVar()
        self.population_size = tk.IntVar(value=10)
        self.generations = tk.IntVar(value=100)
        self.crossover_probability = tk.DoubleVar(value=1.0)
        self.mutation1_probability = tk.DoubleVar(value=0.5)
        self.mutation2_probability = tk.DoubleVar(value=0.5)

        # Create and place widgets
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="File Name:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.master, textvariable=self.filename, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.master, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.master, text="Population Size:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.master, textvariable=self.population_size).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Generations:").grid(row=2, column=0, sticky="e")
        tk.Entry(self.master, textvariable=self.generations).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Crossover Probability:").grid(row=3, column=0, sticky="e")
        tk.Entry(self.master, textvariable=self.crossover_probability).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Mutation 1 Probability:").grid(row=4, column=0, sticky="e")
        tk.Entry(self.master, textvariable=self.mutation1_probability).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Mutation 2 Probability:").grid(row=5, column=0, sticky="e")
        tk.Entry(self.master, textvariable=self.mutation2_probability).grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self.master, text="Run Genetic Algorithm", command=self.run_genetic_algorithm).grid(row=6, column=1, pady=10)

    def place_widgets(self):
        for child in self.master.winfo_children():
            child.grid_configure(padx=10, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.filename.set(file_path)

    def run_genetic_algorithm(self):
        file_path = self.filename.get()
        if file_path:
            values = Read_Data(file_path)
            Genetic_Algorithms(
                values,
                self.population_size.get(),
                self.generations.get(),
                self.crossover_probability.get(),
                self.mutation1_probability.get(),
                self.mutation2_probability.get()
            )
if __name__ == "__main__":
    root = tk.Tk()
    app = GeneticAlgorithmGUI(root)
    root.mainloop()
#-----------------------------[END]---------------------------------------------------------