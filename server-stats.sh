#!/bin/bash

LOGFILE="server-stats.log"

{
echo -e "\n=== REPORT $(date '+%Y-%m-%d %H:%M:%S') ==="

echo "===TOTAL CPU USAGE==="
mpstat 1 1 | awk '/Average:/ {print 100-$NF"%used"}'

echo -e "\n===TOTAL MEMORY USAGE==="
free --mebi | awk '/Mem:/ {
    used=$3; total=$2; free=$4; available=$7;

    used_perc = used/total * 100;
    free_perc = free/total * 100;
    avail_perc = available/total * 100;
    
    used_gib = used/1024;
    total_gib = total/1024;
    free_gib = free/1024;
    avail_gib = available/1024;

    printf " Used: %d Mib(%.2f Gib) / %d Mib(%.2f Gib) (%.2f%%)\n",\
           used, used_gib, total, total_gib, used_perc;

    printf " Free: %d Mib(%.2f Gib) / %d Mib(%.2f Gib) (%.2f%%)\n",\
           free, free_gib, total, free_gib, free_perc;

    printf " Available: %d Mib(%.2f Gib) / %d Mib(%.2f Gib) (%.2f%%)\n",\
           available, avail_gib, total, avail_gib, avail_perc;
}'	   


echo -e "\n===TOTAL DISK USAGE==="
df -B1M --total | awk '/^total/ {
    used=$3; total=$2; available=$4;

    used_perc = used/total * 100;
    avail_perc = available/total * 100;

    sub("M","",used); sub("M","",total); sub("M","",available);

    used_gib = used/1024;
    total_gib = total/1024;
    avail_gib = available/1024;

    printf " Used: %d Mib(%.2f Gib) / %d Mib(%.2f Gib) (%.2f%%)\n",\
           used, used_gib, total, total_gib, used_perc;

    printf " Available: %d Mib(%.2f Gib) / %d Mib(%.2f Gib) (%.2f%%)\n",\
           available, avail_gib, total, avail_gib, avail_perc;

}'


echo -e "\n===TOP 5 CPU PROCESSES==="
ps -eo pid,ppid,user,cmd,%cpu,%mem --sort=-%cpu | head -n 6


echo -e "\n===TOP 5 MEMORY PROCESSES==="
ps -eo pid,ppid,user,cmd,%cpu,%mem --sort=-%mem | head -n 6

} | tee -a "$LOGFILE"
