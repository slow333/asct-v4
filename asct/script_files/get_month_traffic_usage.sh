#!/bin/bash

SA_DIR="/var/log/sa"
OUTPUT_FILE="/tmp/${HOSTNAME}_traffic_usage_$(date +%Y%m%d).csv"
IP_ADDR=$(hostname -I | awk '{print $1}')
[ -z "$IP_ADDR" ] && IP_ADDR="127.0.0.1"

# 인터페이스 속도 수집 (Mbps 단위)
SPEED_MAP=""
for iface_path in /sys/class/net/*; do
    iface_name=$(basename "$iface_path")
    if [ -f "$iface_path/speed" ]; then
        speed=$(cat "$iface_path/speed" 2>/dev/null)
        if [[ "$speed" =~ ^[0-9]+$ ]]; then
            SPEED_MAP="${SPEED_MAP}${iface_name}:${speed},"
        fi
    fi
done

if [ -d "$SA_DIR" ]; then
    echo "hostname,IP,Date,IFACE,Speed,rxkB/s,txkB/s" > "$OUTPUT_FILE"
    for file in $(ls $SA_DIR/sa[0-9][0-9] 2>/dev/null | sort); do
        # 헤더(#으로 시작) 제외하고 추가
        sadf -d "$file" -- -n DEV | grep -v '^#' | awk -F';' -v ip="$IP_ADDR" -v speed_map="$SPEED_MAP" '
        BEGIN {
            OFS=","
            split(speed_map, arr, ",")
            for (i in arr) {
                split(arr[i], pair, ":")
                speeds[pair[1]] = pair[2]
            }
        }
        $4 != "lo" {
            timestamp = $3
            if (timestamp ~ /^[0-9]+$/) {
                timestamp = strftime("%Y-%m-%d %H:%M:%S", timestamp)
            }
            
            spd = speeds[$4]; if(spd=="") spd="-"; else if(spd>=1000) spd=(spd/1000)"G"; else spd=spd"M"
            print $1, ip, timestamp, $4, spd, $7, $8
        }' >> "$OUTPUT_FILE"
    done
    echo "Successfully generated CSV: $OUTPUT_FILE"
else
    echo "Directory $SA_DIR not found."
    exit 1
fi
