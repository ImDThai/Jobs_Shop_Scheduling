import tkinter as tk
from tkinter import Label, Entry, Button
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread
from AL import Read_Data
from AL import chromosome
import mutation as Mu
import crossover as Cr
import ortool as Or
import copy

S1 = 0
S2 = 0
S3 = 0
y = 0

class RealtimeGraph:
    def __init__(self, root):
        self.root = root
        self.root.title("Realtime Gantt Chart")

        self.figure, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Call the update method every 5000 milliseconds (5 seconds)
        self.root.after(1000, self.update_graph)

        # Add button to open Genetic Algorithm parameters window
        Button(root, text="Genetic Algorithm Parameters", command=self.open_genetic_algorithm_window).pack()

    def showGC(self, data, Makespans, Workloads):
        # ... (your existing code for displaying Gantt chart)
        # Clear previous data on the axis
        self.ax.clear()
        # Tạo Gantt chart
        # Tính toán thời gian bắt đầu và kết thúc
        for i, machine_data in enumerate(data):
            for task in machine_data:
                job, task_num, start, end = task
                color = plt.cm.viridis(job / max([t[0] for m in data for t in m]))
                self.ax.barh(i, end - start, left=start, color=color, edgecolor='black')

                # Thêm nhãn công việc vào thanh ngang
                self.ax.text((start + end) / 2, i, f'J{job}O{task_num}', color='black', va='center', ha='center', weight='bold')

        # Tạo legend cho các jobs
        unique_jobs = sorted(set(task[0] for machine_data in data for task in machine_data))
        legend_patches = [mpatches.Rectangle((0, 0), 1, 1, color=plt.cm.viridis(job / max([t[0] for m in data for t in m]))) for job in unique_jobs]
        
        # Tạo legend
        self.ax.legend(legend_patches, [f'Job {job}' for job in unique_jobs], loc='upper left', bbox_to_anchor=(1, 1))

        # Đặt nhãn và tiêu đề
        self.ax.set_yticks(range(len(data)))
        self.ax.set_yticklabels([f'Machine {i+1}' for i in range(len(data))])
        self.ax.set_xlabel(f'Makespans = {Makespans} | Workloads = {Workloads} | Generation = {y}')
        self.ax.xaxis.label.set_fontweight('bold')
        self.ax.set_title('GANTT CHART')

        # Redraw the canvas
        self.canvas.draw()

    def update_graph(self):
        if S2 != 0:
            self.showGC(S1, S2, S3)
            # Call the update method again after 5000 milliseconds (5 seconds)
            self.root.after(1000, self.update_graph)

    def open_genetic_algorithm_window(self):
        # Open Genetic Algorithm Parameters window
        GeneticAlgorithmParamsWindow(self.root)

class GeneticAlgorithmParamsWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Genetic Algorithms Parameters")

        # Create entry widgets for parameters
        self.data_entry = Entry(self.root, width=50)
        self.population_size_entry = Entry(self.root)
        self.generation_entry = Entry(self.root)
        self.crossover_prob_entry = Entry(self.root)
        self.mutation1_prob_entry = Entry(self.root)
        self.mutation2_prob_entry = Entry(self.root)

        # Set default values for parameters
        self.data_entry.insert(0, "kacem2002_1.txt")
        self.population_size_entry.insert(0, "10")
        self.generation_entry.insert(0, "50")
        self.crossover_prob_entry.insert(0, "0.8")
        self.mutation1_prob_entry.insert(0, "0.2")
        self.mutation2_prob_entry.insert(0, "0.2")

        # Create labels
        Label(self.root, text="Data File:").grid(row=0, column=0)
        Label(self.root, text="Population Size:").grid(row=1, column=0)
        Label(self.root, text="Generations:").grid(row=2, column=0)
        Label(self.root, text="Crossover Probability:").grid(row=3, column=0)
        Label(self.root, text="Mutation1 Probability:").grid(row=4, column=0)
        Label(self.root, text="Mutation2 Probability:").grid(row=5, column=0)

        # Place entry widgets
        self.data_entry.grid(row=0, column=1)
        self.population_size_entry.grid(row=1, column=1)
        self.generation_entry.grid(row=2, column=1)
        self.crossover_prob_entry.grid(row=3, column=1)
        self.mutation1_prob_entry.grid(row=4, column=1)
        self.mutation2_prob_entry.grid(row=5, column=1)

        # Create "Run GA" button
        Button(self.root, text="Run GA", command=self.run_genetic_algorithm).grid(row=6, columnspan=2)

    def run_genetic_algorithm(self):
        # Get parameter values from entry widgets
        data_file = self.data_entry.get()
        population_size = int(self.population_size_entry.get())
        generation = int(self.generation_entry.get())
        crossover_prob = float(self.crossover_prob_entry.get())
        mutation1_prob = float(self.mutation1_prob_entry.get())
        mutation2_prob = float(self.mutation2_prob_entry.get())

        # Run Genetic Algorithms with the specified parameters
        GA = Thread(target=Genetic_Algorithms, args=(data_file, population_size, generation, crossover_prob, mutation1_prob, mutation2_prob))
        GA.start()
        
def Genetic_Algorithms(Data_in,population_size,generation,crossover_probability,mutation1_probability,mutation2_probability):
    global S1, S2, S3, y
    D = Read_Data(Data_in)    #Đưa dữ liệu vào mảng D
    E = chromosome(D,1000,1000)    #Xây dựng quần thể (bộ nhiễm sắc thể choromosome(dữ liệu vào, số lượng gen mong muốn, số vòng lặp random))
    c = int(population_size*crossover_probability)
    m1 = int(population_size*mutation1_probability)
    m2 = int(population_size*mutation2_probability)
    Q = E
    x = 1
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
                S1 = Or.JSP_OR(Assf).scheduling()
                S2 = Or.JSP_OR(Assf).makespans()
                S3 = Or.JSP_OR(Assf).workloads()
                y  = x
        x += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimeGraph(root)
    root.mainloop()
