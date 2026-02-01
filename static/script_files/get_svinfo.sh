#!/bin/bash

# Ensure generic locale for parsing
export LC_ALL=C

# Hostname
HOSTNAME=$(hostname)

# IP Addresses
# Try hostname -I first (GNU hostname)
if command -v hostname >/dev/null 2>&1 && hostname -I >/dev/null 2>&1; then
    IP_ALL=$(hostname -I)
else
    # Fallback to ip command
    IP_ALL=$(ip -4 addr show scope global | grep inet | awk '{print $2}' | cut -d/ -f1 | tr '\n' ' ')
fi
IP1=$(echo $IP_ALL | awk '{print $1}')
IP2=$(echo $IP_ALL | awk '{print $2}')

# OS Version
if [ -f /etc/os-release ]; then
    # Source the file to get variables
    . /etc/os-release
    OS_VERSION=$PRETTY_NAME
elif [ -f /etc/redhat-release ]; then
    OS_VERSION=$(cat /etc/redhat-release)
else
    OS_VERSION=$(uname -sr)
fi
# Remove quotes if any
OS_VERSION=$(echo "$OS_VERSION" | sed 's/"//g')

# Kernel Version
KERNEL_VERSION=$(uname -r)

# CPU Cores
if command -v nproc >/dev/null 2>&1; then
    CPU_CORES=$(nproc)
else
    CPU_CORES=$(grep -c ^processor /proc/cpuinfo)
fi

# CPU Usage (%) - using /proc/stat for 1 second interval
get_cpu_usage() {
    read cpu a b c idle rest < /proc/stat
    prev_total=$((a+b+c+idle))
    prev_idle=$idle
    sleep 1
    read cpu a b c idle rest < /proc/stat
    total=$((a+b+c+idle))
    let "diff_total=$total-$prev_total"
    let "diff_idle=$idle-$prev_idle"
    awk -v diff_total="$diff_total" -v diff_idle="$diff_idle" 'BEGIN { if(diff_total==0) print 0; else printf "%.1f", (diff_total-diff_idle)/diff_total*100 }'
}
CPU_USAGE=$(get_cpu_usage)

# Memory (GB)
# Get total memory in kB and convert to GB (rounding)
MEM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
MEMORY=$(awk -v mem="$MEM_KB" 'BEGIN {printf "%.0f", mem/1024/1024}')

# Total Disk (GB)
# Sum size of all disk-type block devices
if command -v lsblk >/dev/null 2>&1; then
    TOTAL_DISK=$(lsblk -d -n -o SIZE -b | awk '{sum+=$1} END {print int(sum/1024/1024/1024)}')
else
    # Fallback using df for root if lsblk not available
    TOTAL_DISK=$(df -B1G / | awk 'NR==2 {print $2}' | sed 's/G//')
fi

# Memory Usage (%)
MEM_TOTAL=$(grep MemTotal /proc/meminfo | awk '{print $2}')
MEM_AVAIL=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
if [ -z "$MEM_AVAIL" ]; then
    # Fallback for older kernels
    MEM_FREE=$(grep MemFree /proc/meminfo | awk '{print $2}')
    MEM_BUFF=$(grep Buffers /proc/meminfo | awk '{print $2}')
    MEM_CACHE=$(grep ^Cached /proc/meminfo | awk '{print $2}')
    MEM_AVAIL=$((MEM_FREE + MEM_BUFF + MEM_CACHE))
fi
MEM_USAGE=$(awk -v t="$MEM_TOTAL" -v a="$MEM_AVAIL" 'BEGIN {if(t==0) print 0; else printf "%.1f", (t-a)/t*100}')

# Disk Usage (%) - Root partition
DISK_USAGE=$(df -P / | awk 'NR==2 {print $5}' | tr -d '%')

# Uptime (days)
UPTIME_DAYS=$(awk '{print int($1/86400)}' /proc/uptime)

# Is Virtual
IS_VIRTUAL="false"
if command -v systemd-detect-virt >/dev/null 2>&1; then
    systemd-detect-virt >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        IS_VIRTUAL="true"
    fi
fi

# Current Time
DATA_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Save to CSV
CHECK_DATE=$(date +%Y%m%d)
CSV_FILE="/tmp/${HOSTNAME}_${IP1}_${CHECK_DATE}.csv"

echo "hostname,ip1,ip2,os_version,kernel_version,cpu_cores,memory,total_disk,uptime,data_time,is_virtual,cpu_usage,memory_usage,disk_usage" > "$CSV_FILE"
echo "$HOSTNAME,$IP1,$IP2,\"$OS_VERSION\",$KERNEL_VERSION,$CPU_CORES,$MEMORY,$TOTAL_DISK,$UPTIME_DAYS,\"$DATA_TIME\",$IS_VIRTUAL,$CPU_USAGE,$MEM_USAGE,$DISK_USAGE" >> "$CSV_FILE"

# Output JSON
cat <<EOF
{
    "hostname": "$HOSTNAME",
    "ip1": "$IP1",
    "ip2": "$IP2",
    "os_version": "$OS_VERSION",
    "kernel_version": "$KERNEL_VERSION",
    "cpu_cores": $CPU_CORES,
    "memory": $MEMORY,
    "total_disk": $TOTAL_DISK,
    "uptime": $UPTIME_DAYS,
    "data_time": "$DATA_TIME", 
    "is_virtual": $IS_VIRTUAL,
    "cpu_usage": $CPU_USAGE,
    "memory_usage": $MEM_USAGE,
    "disk_usage": $DISK_USAGE
}
EOF
