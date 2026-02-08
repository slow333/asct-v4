#!/bin/bash

export LC_ALL=C

HOSTNAME=$(hostname)
IP_ADDR=$(hostname -I | awk '{print $1}')
[ -z "$IP_ADDR" ] && IP_ADDR="127.0.0.1"
CPU_CORES=$(nproc --all)
OUTPUT_FILE="/tmp/${HOSTNAME}_cpu_usage_$(date +%Y%m%d).csv"

echo "hostname,IP,Date,Cpu_cores,Total_Usage(%)" > "$OUTPUT_FILE"

SA_DIR="/var/log/sa"

if [ -d "$SA_DIR" ]; then
    # Check if sysstat is installed
    if ! command -v sadf >/dev/null 2>&1; then
        echo "Error: sysstat (sadf) is not installed."
        exit 1
    fi

    # 파일 수집 및 정렬
    for file in $(ls $SA_DIR/sa[0-9][0-9] 2>/dev/null | sort); do
        # sadf로 파일을 읽을 수 있는지 확인
        if sadf -d "$file" -- -u >/dev/null 2>&1; then
            # -d: Database friendly (semicolon separated)
            # -t: Local timestamp
            # -- -u: CPU stats
            sadf -d -t "$file" -- -u | grep -v "^#" | awk -F';' -v host="$HOSTNAME" -v ip="$IP_ADDR" -v cores="$CPU_CORES" '
            {
                # Handle RHEL 6 epoch timestamp (all digits)
                timestamp = $3
                if (timestamp ~ /^[0-9]+$/) {
                    timestamp = strftime("%Y-%m-%d %H:%M:%S", timestamp)
                }

                if ($4 == "all" || $4 == "-1") {
                    usage = 100 - $NF
                    printf "%s,\"%s\",%s,%s,%.2f\n", host, ip, timestamp, cores, usage
                }
            }' >> "$OUTPUT_FILE"
        fi
    done

    echo "Successfully generated CSV: $OUTPUT_FILE"
    # cat "$OUTPUT_FILE"
else
    echo "Error: Directory $SA_DIR not found."
fi

# awk -F';'는 입력받은 텍스트의 각 줄을 나눌 때, 구분자(Field Separator)로 세미콜론(;)을 사용하겠다는 의미입니다.

# 기본 동작: awk는 아무 옵션이 없으면 **공백(스페이스나 탭)**을 기준으로 데이터를 나눕니다.
# -F 옵션: Field Separator의 약자로, 구분자를 직접 지정할 때 사용합니다.
# 스크립트 내 역할:
# 앞선 명령어 sadf -d는 데이터를 **세미콜론(;)**으로 구분된 형식(CSV와 유사)으로 출력합니다.
# 예: hostname;interval;timestamp;CPU;%user;...
# 따라서 awk가 이 데이터를 올바르게 읽어서 $3(시간), $4(CPU 종류), $NF(Idle 값) 등을 추출하려면, 공백이 아닌 세미콜론을 기준으로 잘라야 합니다.
# 즉, **"데이터가 세미콜론으로 구분되어 있으니, 거기에 맞춰서 잘라 읽어라"**라고 awk에게 알려주는 옵션입니다.

# NF (Number of Fields): 현재 처리 중인 줄(Line)에 있는 필드(열)의 총 개수를 나타냅니다.
# $NF: 필드의 총 개수(NF)를 인덱스로 사용하여, 가장 마지막 필드의 값을 가져옵니다.
# 예시 상황
# sadf -d 명령어의 출력이 다음과 같다고 가정해 보겠습니다 (세미콜론 ;으로 구분):

# text
# hostname;interval;timestamp;CPU;%user;%nice;%system;%iowait;%steal;%idle
# 이 줄에는 총 10개의 필드가 있습니다. 따라서:

# NF = 10
# $1 = hostname
# $2 = interval
# ...
# $10 (즉, $NF) = %idle (마지막 값)
# 작성하신 스크립트에서 sadf ... -- -u 옵션은 CPU 사용률을 출력하며, 이 포맷에서 가장 마지막 컬럼이 항상 Idle(유휴) 상태의 비율이기 때문에 $NF를 사용하여 그 값을 가져오는 것입니다.
