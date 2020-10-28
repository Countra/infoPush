# import subprocess
import os
# import time
# import socket
import psutil  # 监控数据读取
import sys
import multiprocessing
from multiprocessing import Process, Manager
"""
 * Copyright by 2020 Countra. All rights reserved.
 * @author: Countra
 * @date: 2020-10-02
"""
Cpu_dict = {}
cpus = ""
version = "1.0"


# CPU使用率
def get_cpu_per():
    cpu_p = psutil.cpu_percent(interval=1, percpu=True)  # 读取CPU使用率
    return cpu_p


# 内存信息
# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM


def getRAMinfo():
    p = os.popen('free')
    i = 0
    while True:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:4])


# 内存使用情况
def get_mem():
    # 读取内存使用率
    mem_p = psutil.virtual_memory().percent
    return mem_p


# 硬盘信息
# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used


def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while True:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:5])


# 网络信息
# 获取ip地址
# def get_ip():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#     return ip

# 获取公网ip地址
# def get_public_ip():
#     os.system('curl myip.ipip.net')


# 网络使用情况
def net_info():
    net_in = psutil.net_io_counters().bytes_recv / 1024 / 1024 / 1024
    net_in = round(net_in, 2)
    net_out = psutil.net_io_counters().bytes_sent / 1024 / 1024 / 1024
    net_out = round(net_out, 2)
    net = "Receive Data: " + str(net_in) + "GB / " + "Transmit Data: " + str(
        net_out) + "GB"
    return net


# 网速
# def net_speed():
#     s1 = psutil.net_io_counters().bytes_recv
#     time.sleep(1)
#     s2 = psutil.net_io_counters().bytes_sent
#     result = s2 - s1
#     # 结果保留两位小数
#     return str('%.2f' % (result / 1024 / 8 / 1024)) + 'MB/s'

###################################################################3


def CPU_Utilization(P):
    try:
        p1 = psutil.Process(int(P))
        if sys.argv[0] not in " ".join(p1.cmdline()):
            Cpu_dict[P] = str(p1.cpu_percent(interval=1)) + "%"  #等8秒
    except:
        pass


###################################################################3


def main():
    # CPU信息
    CPU_usage = get_cpu_per()

    # 内存信息
    # Output is in kb,here I convert it in Mb for readability
    RAM_stats = getRAMinfo()
    # RAM_total = round(int(RAM_stats[0]) / 1000, 1)
    RAM_used = round(int(RAM_stats[1]) / 1000, 1)
    RAM_free = round(int(RAM_stats[2]) / 1000, 1)
    RAM_per = get_mem()

    # Disk information
    DISK_stats = getDiskSpace()
    # DISK_total = DISK_stats[0]
    # DISK_used = DISK_stats[1]
    DISK_perc = DISK_stats[3]

    strs = " -------------------------------------------------------------\n|\t\thardware information\n" \
        + '|  CPU Use :  ' + str(CPU_usage) \
         + '\n|  RAM Used : ' + str(RAM_used) + " MB\n" \
           + '|  RAM Free : ' + str(RAM_free) + " MB\n" + '|  RAM Usage rate : ' \
             + str(RAM_per) + "%\n" \
              + '|  Disk Used Percentage : ' + str(DISK_perc) + "\n" \
                + '|  ' + net_info()

    os.system(
        "ls /var/countra/data/ >> /dev/null || mkdir -p /var/countra/data/")

    with open('/var/countra/data/sysinfos', 'wt') as f:
        f.write(strs + '\n|  ')

    os.system(
        "cat /proc/uptime| awk -F. '{run_days=$1 / 86400;run_hour=($1 % 86400)/3600;run_minute=($1 % 3600)/60;run_second=$1 % 60;printf(\"System is running: %d days %d:%d:%d\",run_days,run_hour,run_minute,run_second)}' >> /var/countra/data/sysinfos"
    )


if __name__ == "__main__":
    main()
    p_list = []
    with Manager() as manager:
        Cpu_dict = manager.dict()
        for i in psutil.pids():
            p = multiprocessing.Process(target=CPU_Utilization, args=(i, ))
            p.daemon = True
            p_list.append(p)
        for p in p_list:
            p.start()
        for p in p_list:
            p.join()
        for Mem_max in (sorted(Cpu_dict.items(),
                               key=lambda kv: (kv[1], kv[0]),
                               reverse=True))[0:1]:
            M_p = psutil.Process(Mem_max[0])
            cpus ="\n|\n|  < The process with the highest CPU usage >""\n|PID\tCPU use\t\tName\n|" \
                + str(Mem_max[0]) + "\t  " + str(Mem_max[1]) + "\t" \
                + " ".join(M_p.cmdline())
    with open('/var/countra/data/sysinfos', 'a+') as f:
        f.write(cpus)

    with open('/var/countra/data/sysinfos', 'a+') as f:
        f.write("\n -------------------------------------------------------------\n" +
                '\n')
