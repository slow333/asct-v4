#!/bin/bash

export LC_ALL=C

IP_ADDR=$(hostname -I | awk '{print $1}')
[ -z "$IP_ADDR" ] && IP_ADDR="127.0.0.1"
# Total Memory in MB
TOTAL_MEM=$(free -m | awk '/^Mem:/{print $2}')
OUTPUT_FILE="/tmp/${HOSTNAME}_memory_usage_$(date +%Y%m%d).csv"
HEADER_WRITTEN=false

echo "hostname,IP,Date,Total_Mem,Usage(%)" > "$OUTPUT_FILE"

SA_DIR="/var/log/sa"

if [ -d "$SA_DIR" ]; then
    for file in $(ls $SA_DIR/sa[0-9][0-9] 2>/dev/null | sort); do
        if sadf -d "$file" -- -r >/dev/null 2>&1; then
            # sadf -d output header starts with #
            # We need to find which field number is %memused or %mem.
            sadf -d -t "$file" -- -r | awk -F';' -v  ip="$IP_ADDR" -v tot_mem="$TOTAL_MEM" '
            BEGIN { mem_idx = 0 }
            /^#/ {
                for (i=1; i<=NF; i++) {
                    if ($i == "%memused" || $i == "%mem") {
                        mem_idx = i
                        break
                    }
                }
            }
            !/^#/ {
                if (mem_idx > 0) {
                    timestamp = $3
                    if (timestamp ~ /^[0-9]+$/) {
                        timestamp = strftime("%Y-%m-%d %H:%M:%S", timestamp)
                    }
                    usage = $mem_idx
                    printf "%s,\"%s\",%s,%s,%.2f\n", $1, ip, timestamp, tot_mem, usage
                }
            }' >> "$OUTPUT_FILE"
        fi
    done
    echo "Successfully generated CSV: $OUTPUT_FILE"
else
    echo "Error: Directory $SA_DIR not found."
fi

# sadf -d 명령어의 출력 형식 때문에 헤더(Header)와 실제 데이터(Data)를 구분하여 처리하기 위함입니다.

# sadf -d -- -r  출력
# # hostname;interval;timestamp;kbmemfree;kbavail;kbmemused;%memused;kbbuffers;kbcached;kbcommit;%commit;kbactive;kbinact;kbdirty
# rhel9;268;2026-02-06 23:00:35 UTC;103612;26864;140552;37.59;0;47036;288092;9.57;22292;30668;0
# rhel9;600;2026-02-06 23:10:35 UTC;112516;30008;143104;38.27;0;35640;288476;9.58;27676;14320;0
# rhel9;600;2026-02-06 23:20:35 UTC;110708;28288;144852;38.74;0;35700;288476;9.58;28008;14364;0
# rhel9;600;2026-02-06 23:30:35 UTC;109472;27052;146088;39.07;0;35700;288476;9.58;28008;14364;0
# rhel9;600;2026-02-06 23:40:35 UTC;108212;25816;147280;39.39;0;35772;288092;9.57;27808;14388;0

# /^#/ (헤더 처리)
# ^는 줄의 시작, #은 해시 문자를 의미합니다. 즉, #으로 시작하는 줄을 찾습니다.
# sadf -d 명령어를 실행하면 첫 번째 줄(헤더)이 # hostname;interval;timestamp... 형태로 출력됩니다.

# 이 블록에서는 헤더의 각 컬럼을 순회하며 %memused 또는 %mem이 몇 번째 컬럼(인덱스)에 있는지(mem_idx)를 찾아냅니다. sysstat 버전에 따라 컬럼 순서가 다를 수 있기 때문에 동적으로 위치를 파악하는 것입니다.

# !/^#/ (데이터 처리)
# !는 부정(Not)을 의미합니다. 즉, #으로 시작하지 않는 줄을 찾습니다.
# 실제 CPU나 메모리 사용률 데이터가 담긴 줄들은 # 없이 바로 데이터로 시작합니다.
# 이 블록에서는 앞서 헤더에서 찾아낸 인덱스(mem_idx)를 사용하여, 실제 데이터 줄에서 정확한 메모리 사용률 값을 추출하고 CSV 형태로 출력합니다.
# 요약하자면, 헤더에서 컬럼 위치를 먼저 파악하고, 그 위치 정보를 이용해 실제 데이터 줄에서 값을 꺼내기 위해 두 패턴으로 나누어 처리하는 것입니다.