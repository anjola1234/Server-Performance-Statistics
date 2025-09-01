#!/usr/bin/env python3

import psutil
import platform 

def cpu_usage():
    print("===TOTAL CPU USAGE===")
    usage =  psutil.cpu_percent(interval=1)
    print(f"{usage}% used")


def memory_usage():
    print("\n===TOTAL MEMORY USAGE===")
    mem = psutil.virtual_memory()

    total = mem.total / (1024**2)
    used = mem.used / (1024**2)
    free = mem.free / (1024**2)
    available = mem.available / (1024**2)

    used_perc = used/total * 100
    free_perc = free/total * 100
    avail_perc = available/total * 100

    print(f"Used: {used:.2f}Mib({used/1024:.2f}Gib) / {total:.2f}Mib({total/1024:.2f}Gib)  {used_perc:.2f}%")
    print(f"free: {free:.2f}Mib({free/1024:.2f}Gib) / {free:.2f}Mib({total/1024:.2f}Gib)  {free_perc:.2f}%")
    print(f": {available:.2f}Mib({available/1024:.2f}Gib) / {available:.2f}Mib({total/1024:.2f}Gib)  {avail_perc:.2f}%")


def disk_usage():
    print("\n===TOTAL DISK USAGE===")
    disk = psutil.disk_usage("/")

    total = disk.total / (1024**2)
    used = disk.used / (1024**2)
    free = disk.free / (1024**2)

    used_perc = used/total * 100
    free_perc = free/total * 100

    print(f"Used: {used:.2f}Mib({used/1024:.2f}Gib) / {total:.2f}Mib({total/1024:.2f}Gib)  {used_perc:.2f}%")
    print(f"free: {free:.2f}Mib({free/1024:.2f}Gib) / {free:.2f}Mib({total/1024:.2f}Gib)  {free_perc:.2f}%")



def top_processes():
    print("\n===TOP 5 CPU PROCESSES===")
    processes = []
    for p in psutil.process_iter(["pid", "ppid", "username", "exe", "cpu_percent","memory_percent"]):

        pid = p.info.get("pid", 0)
        ppid = p.info.get("ppid", 0)
        user = p.info.get("username")
        exe = str(p.info.get("exe", ""))
        cpu_percent =  p.info.get("cpu_percent", 0.0)
        mem_percent =  p.info.get("memory_percent", 0.0)

        processes.append((pid, ppid, user, exe, cpu_percent, mem_percent))

    cpu_sorted = sorted(processes, key=lambda x: x[4], reverse=True)

    for pid, ppid, user, exe, cpu, mem in cpu_sorted[:5]:
        print(f" PID {pid:<6} | PPID {ppid:<6} | USER {user:<15} | EXE {str(exe):<30} | CPU {cpu:>5.1f}% | MEM {mem:>5.1f}%") 

    print("\n===TOP 5 MEMORY PROCESSES===")
    mem_sorted = sorted(processes, key=lambda x: x[5], reverse=True)

    for pid, ppid, user, exe, cpu, mem in mem_sorted[:5]:
        print(f" PID {pid:<6} | PPID {ppid:<6} | USER {user:<15} | EXE {str(exe):<30} | CPU {cpu:>5.1f}% | MEM {mem:>5.1f}%")


if __name__ == "__main__":
    print(f"System: {platform.system()} {platform.release()}")
    cpu_usage()
    memory_usage()
    disk_usage()
    top_processes()

