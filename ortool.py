import collections
from ortools.sat.python import cp_model



#Chuyển đổi kiểu dữ liệu từ Assignment Schdeduling -> OR-Tools Data
def format_data(gen,data_in):
    Assignment_Scheduling = gen
    x = len(Assignment_Scheduling)
    y = len(Assignment_Scheduling[0])
    z = len(Assignment_Scheduling[0][0])
    Assignment_Scheduling2 = [[0 for k in range(y)] for j in range(x)]
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if Assignment_Scheduling[i][j][k] == 1:
                    Assignment_Scheduling2[i][j] = (k,data_in[i][j][k])
    for i in range(x):
        for j in range(y):
            if Assignment_Scheduling2[i][j] == 0:
                del Assignment_Scheduling2[i][j]
    return Assignment_Scheduling2

#Xây dựng thư viện các thuộc tính
class JSP_OR():
    def __init__(self, jobs_data):
        self.jobs_data = jobs_data
        
        machines_count = 1 + max(task[0] for job in jobs_data for task in job)
        # Tinh W/Wk
        Data = self.jobs_data
        W = [0 for i in range(machines_count)]
        T = [0 for i in range(len(Data))]
        for i in range(len(Data)):
            for j in range(len(Data[i])):
                W[Data[i][j][0]] = W[Data[i][j][0]] + Data[i][j][1]
                T[i] = T[i] + Data[i][j][1]

        self.time_per_jobs = T
        self.total_workloads = sum(W)
        self.WLs = W

        self.all_machines = range(machines_count)  # Make it a class member
        horizon = sum(task[1] for job in jobs_data for task in job)

        # Create the model.
        model = cp_model.CpModel()

        # Named tuple to store information about created variables.
        task_type = collections.namedtuple("task_type", "start end interval")
        # Named tuple to manipulate solution information.
        assigned_task_type = collections.namedtuple(
            "assigned_task_type", "start job index duration"
        )

        # Creates job intervals and add to the corresponding machine lists.
        all_tasks = {}
        machine_to_intervals = collections.defaultdict(list)

        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine, duration = task
                suffix = f"_{job_id}_{task_id}"
                start_var = model.NewIntVar(0, horizon, "start" + suffix)
                end_var = model.NewIntVar(0, horizon, "end" + suffix)
                interval_var = model.NewIntervalVar(
                    start_var, duration, end_var, "interval" + suffix
                )
                all_tasks[job_id, task_id] = task_type(
                    start=start_var, end=end_var, interval=interval_var
                )
                machine_to_intervals[machine].append(interval_var)

        # Create and add disjunctive constraints.
        for machine in self.all_machines:
            model.AddNoOverlap(machine_to_intervals[machine])

        # Precedences inside a job.
        for job_id, job in enumerate(jobs_data):
            for task_id in range(len(job) - 1):
                model.Add(
                    all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end
                )

        # Makespan objective.
        obj_var = model.NewIntVar(0, horizon, "makespan")
        model.AddMaxEquality(
            obj_var,
            [all_tasks[job_id, len(job) - 1].end for job_id, job in enumerate(jobs_data)],
        )
        model.Minimize(obj_var)

        # Creates the solver and solve.
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # Create one list of assigned tasks per machine.
            assigned_jobs = collections.defaultdict(list)
            for job_id, job in enumerate(jobs_data):
                for task_id, task in enumerate(job):
                    machine = task[0]
                    assigned_jobs[machine].append(
                        assigned_task_type(
                            start=solver.Value(all_tasks[job_id, task_id].start),
                            job=job_id,
                            index=task_id,
                            duration=task[1],
                        )
                    )
            Cmax = solver.ObjectiveValue()  # Get the makespan value
            self.Makespans = Cmax
            self.assigned_jobs = assigned_jobs

    def makespans(self):
        Cmax = self.Makespans
        return Cmax

    def scheduling(self):
        output = ""
        for machine in self.all_machines:  # Access all_machines from the class
            # Sort by starting time.
            self.assigned_jobs[machine].sort()
            sol_line_tasks = "Machine " + str(machine + 1) + ": "
            sol_line = "           "
            for assigned_task in self.assigned_jobs[machine]:  # Access assigned_jobs from the class
                name = f"job_{assigned_task.job + 1}_task_{assigned_task.index + 1}"
                # Add spaces to output to align columns.
                sol_line_tasks += f"{name:15}"

                start = assigned_task.start
                duration = assigned_task.duration
                sol_tmp = f"[{start},{start + duration}]"
                # Add spaces to output to align columns.
                sol_line += f"{sol_tmp:15}"
            sol_line += "\n"
            sol_line_tasks += "\n"
            output += sol_line_tasks
            output += sol_line
        print(output)

    def workloads_per_machine(self):
        wpm = self.WLs
        return wpm
    
    def workloads(self):
        Wk = self.total_workloads
        return Wk
    
    def processing_time(self):
        Tk = self.time_per_jobs
        return Tk
