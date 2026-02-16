#!/bin/bash

# JSON 형식으로 서버 정보를 출력하는 스크립트
export LC_ALL=C

HOSTNAME=$(hostname)
IP1=$(hostname -I | awk '{print $1}')
IP2=$(hostname -I | awk '{print $2}')

# OS Version
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_VERSION=$PRETTY_NAME
elif [ -f /etc/redhat-release ]; then
    OS_VERSION=$(cat /etc/redhat-release)
else
    OS_VERSION="Unknown"
fi

KERNEL=$(uname -r)
CPU_CORES=$(nproc)

# Memory (GB)
MEM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
MEMORY=$((MEM_KB / 1024 / 1024))

# Total Disk (GB) - 물리 디스크 합계 (loop, ram 제외)
TOTAL_DISK=$(lsblk -d -n -o SIZE,TYPE | grep -v "loop\|rom" | awk '{print $1}' | sed 's/G//' | awk '{s+=$1} END {print int(s)}')

# Uptime (days)
UPTIME_SEC=$(cat /proc/uptime | awk '{print $1}' | cut -d. -f1)
UPTIME=$((UPTIME_SEC / 86400))

# Virtual Machine Check
if systemd-detect-virt >/dev/null 2>&1; then
    IS_VIRTUAL="true"
else
    IS_VIRTUAL="false"
fi

# Resource Usage (Simple snapshot)
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
MEM_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}')

# Disk Usage (Aggregate / and /home)
read total_kb used_kb <<< $(df -kP / /home 2>/dev/null | awk 'NR>1 {print $1, $2, $3}' | sort -u -k1,1 | awk '{sum_total+=$2; sum_used+=$3} END {print sum_total+0, sum_used+0}')
if [ "${total_kb:-0}" -gt 0 ]; then
    DISK_USAGE=$(awk "BEGIN {printf \"%.0f\", ($used_kb / $total_kb) * 100}")
else
    DISK_USAGE=0
fi

# Current Time
DATA_TIME=$(date +"%Y-%m-%d %H:%M:%S")

# JSON Output
cat <<EOF
{
    "hostname": "$HOSTNAME",
    "ip1": "$IP1",
    "ip2": "$IP2",
    "os_version": "$OS_VERSION",
    "kernel_version": "$KERNEL",
    "cpu_cores": $CPU_CORES,
    "memory": $MEMORY,
    "total_disk": ${TOTAL_DISK:-0},
    "uptime": $UPTIME,
    "is_virtual": $IS_VIRTUAL,
    "cpu_usage": ${CPU_USAGE:-0},
    "memory_usage": ${MEM_USAGE:-0},
    "disk_usage": ${DISK_USAGE:-0},
    "data_time": "$DATA_TIME"
}
EOF
