import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def showGC(data, Makespans, Workloads, save_path='gantt_chart.png'):
    # Tạo Gantt chart
    fig, ax = plt.subplots(figsize=(12, 6))

    # Tính toán thời gian bắt đầu và kết thúc
    for i, machine_data in enumerate(data):
        for task in machine_data:
            job, task_num, start, end = task
            color = plt.cm.viridis(job / max([t[0] for m in data for t in m]))
            ax.barh(i, end - start, left=start, color=color, edgecolor='black')

            # Thêm nhãn công việc vào thanh ngang
            ax.text((start + end) / 2, i, f'J{job}O{task_num}', color='white', va='center', ha='center')

    # Tạo legend cho các jobs
    unique_jobs = sorted(set(task[0] for machine_data in data for task in machine_data))
    legend_patches = [mpatches.Rectangle((0, 0), 1, 1, color=plt.cm.viridis(job / max([t[0] for m in data for t in m]))) for job in unique_jobs]
    
    # Tạo legend
    ax.legend(legend_patches, [f'Job {job}' for job in unique_jobs], loc='upper left', bbox_to_anchor=(1, 1))

    # Đặt nhãn và tiêu đề
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([f'Machine {i+1}' for i in range(len(data))])
    ax.set_xlabel(f'Makespans = {Makespans} , Workloads = {Workloads}')
    ax.set_title('GANTT CHART')

    # Lưu đồ thị dưới dạng hình ảnh
    plt.savefig(save_path, bbox_inches='tight')
