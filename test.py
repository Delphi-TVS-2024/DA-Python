
from datetime import datetime
import psutil


def get_pc_diag_info():
    pc_info = {
        "Free_space(GB)":'x',
        "CPU %":''
    }
    input_date_string = str(datetime.now()).split('.')[0]
    input_datetime = datetime.strptime(input_date_string, "%Y-%m-%d %H:%M:%S")
    output_date_string = input_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    disk_partitions = psutil.disk_partitions()
    e_drive_partition = None
    for partition in disk_partitions:
        if partition.device.startswith('E:'):
            drive_usage = psutil.disk_usage(partition.mountpoint)
            free_space = drive_usage.total / (1024 * 1024 * 1024)
            rounded = round(free_space, 4)
            pc_info["Free_space(GB)"] = rounded
    cpu_percent = psutil.cpu_percent(
        interval=1)  # Interval is in seconds, it waits for 1 second to get CPU utilization
    # print("CPU Utilization:", cpu_percent, "%")
    pc_info["CPU %"] = cpu_percent
    return pc_info , output_date_string

print()


dict , time = get_pc_diag_info()


print(dict)
print(time)