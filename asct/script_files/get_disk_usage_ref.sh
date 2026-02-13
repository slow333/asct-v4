#!/bin/bash

# ##################### CASE 1: df ###########################
# --- 스크립트 동작 설명 ---
# 이 스크립트는 df 명령어를 사용하여 /, /boot, /home 파티션의 용량을 합산하여 계산합니다.
# 중복된 파티션(예: /home이 /에 포함된 경우)은 한 번만 계산합니다.
export LC_ALL=C

HOSTNAME=$(hostname)
IP_ADDR=$(hostname -I | awk '{print $1}')
[ -z "$IP_ADDR" ] && IP_ADDR="127.0.0.1"
OUTPUT_FILE="/tmp/${HOSTNAME}_disk_usage_df_$(date +%Y%m%d).csv"
# CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")


# 1. 루트 디바이스의 스토리지 타입 확인 (기존 로직 재사용)
ROOT_PARTITION=$(df / | awk 'NR==2 {print $1}')
ROOT_DEVICE=$(lsblk -no pkname "$ROOT_PARTITION" 2>/dev/null)
if [ -z "$ROOT_DEVICE" ]; then
    ROOT_DEVICE=$(basename "$ROOT_PARTITION" | sed -e 's/[0-9]*$//' -e 's/p[0-9]*$//')
fi

STORAGE_TYPE="unknown"
if [ -n "$ROOT_DEVICE" ] && [ -f "/sys/block/$ROOT_DEVICE/queue/rotational" ]; then
    is_rotational=$(cat "/sys/block/$ROOT_DEVICE/queue/rotational")
    if [ "$is_rotational" -eq 1 ]; then
        STORAGE_TYPE="hdd"
    else
        STORAGE_TYPE="ssd"
    fi
fi

# 2. df를 이용하여 /, /boot, /home 용량 계산
# -P: POSIX output format (한 줄로 출력)
# -k: 1K-blocks (계산 정확도를 위해 KB 단위 사용)
# sort -u -k1,1: 파일시스템명($1) 기준으로 중복 제거 (예: /home이 /에 포함된 경우 중복 계산 방지)
read total_kb used_kb <<< $(df -kP / /boot /home 2>/dev/null | awk 'NR>1 {print $1, $2, $3}' | sort -u -k1,1 | awk '{sum_total+=$2; sum_used+=$3} END {print sum_total, sum_used}')

# 값이 없을 경우 0으로 처리
total_kb=${total_kb:-0}
used_kb=${used_kb:-0}

# 3. 단위 변환 및 퍼센트 계산
# local_total (GB 단위)
local_total=$((total_kb / 1024 / 1024))

# local_usage_p (%)
if [ "$total_kb" -gt 0 ]; then
    local_usage_p=$(awk "BEGIN {printf \"%.2f\", ($used_kb / $total_kb) * 100}")
else
    local_usage_p=0.00
fi

# 4. CSV 파일 생성
# echo "hostname,IP,storage_type,local_total,local_usage_p" > "$OUTPUT_FILE"
# echo "$HOSTNAME,$IP_ADDR,$STORAGE_TYPE,$local_total,$local_usage_p" >> "$OUTPUT_FILE"

# echo "Successfully generated CSV: $OUTPUT_FILE"

# Output JSON
cat <<EOF
{
    "hostname": "$HOSTNAME",
    "ip_addr": "$IP_ADDR",
    "storage_type": "$STORAGE_TYPE",
    "local_total": "$local_total",
    "local_usage_p": $local_usage_p,
}
EOF


# ##################### CASE 2: sadf ###########################
# --- 스크립트 동작 설명 ---
# 이 스크립트는 sysstat/sadf를 사용하여 디스크 사용량 정보를 수집합니다.
#
# --- 제약 사항 및 해결 ---
# 1. `sadf -d`는 파일 시스템의 용량 사용률(예: `df` 명령어)이 아닌, 디스크의 I/O 통계(tps, kB/s, %util 등)를 제공합니다.
#    요청된 'disk usage(%)'에 가장 근접한 값인 I/O 사용률(`%util`)을 `local_usage_p` 컬럼에 사용합니다.
#    **주의: 이 값은 디스크가 얼마나 찼는지를 나타내는 용량 사용률이 아니라, 디스크가 얼마나 활발하게 일했는지를 나타내는 I/O 사용률입니다.**
#
# 2. `sadf -d`는 시스템의 모든 블록 디바이스에 대한 데이터를 보고하지만, Django 모델은 호스트당 하나의 데이터만 저장하도록 설계되어 있습니다.
#    따라서, 스크립트는 시스템의 핵심인 루트('/') 파일시스템이 위치한 물리 디바이스의 정보만 수집합니다.
export LC_ALL=C

HOSTNAME=$(hostname)
IP_ADDR=$(hostname -I | awk '{print $1}')
[ -z "$IP_ADDR" ] && IP_ADDR="127.0.0.1"
OUTPUT_FILE="/tmp/${HOSTNAME}_disk_usage_$(date +%Y%m%d).csv"


# 1. 루트('/') 파일시스템이 위치한 블록 디바이스 찾기
ROOT_PARTITION=$(df / | awk 'NR==2 {print $1}')
# lsblk를 사용하여 파티션의 부모 디바이스 이름(예: /dev/sda1 -> sda)을 찾습니다.
ROOT_DEVICE=$(lsblk -no pkname "$ROOT_PARTITION" 2>/dev/null)

# lsblk를 사용할 수 없는 경우를 위한 대체 방법
if [ -z "$ROOT_DEVICE" ]; then
    # 파티션 이름에서 숫자 부분을 제거하여 부모 디바이스를 추정합니다. (예: sda1 -> sda, nvme0n1p1 -> nvme0n1)
    ROOT_DEVICE=$(basename "$ROOT_PARTITION" | sed -e 's/[0-9]*$//' -e 's/p[0-9]*$//')
fi

if [ -z "$ROOT_DEVICE" ]; then
    echo "Error: Could not determine the root block device."
    exit 1
fi

# 2. 루트 디바이스의 정보 수집 (storage_type, local_total)
STORAGE_TYPE="unknown"
if [ -f "/sys/block/$ROOT_DEVICE/queue/rotational" ]; then
    is_rotational=$(cat "/sys/block/$ROOT_DEVICE/queue/rotational")
    if [ "$is_rotational" -eq 1 ]; then
        STORAGE_TYPE="hdd"
    else
        STORAGE_TYPE="ssd"
    fi
fi

# 디바이스 전체의 총 용량을 GB 단위로 계산
TOTAL_GB=0
if [ -b "/dev/$ROOT_DEVICE" ]; then
    total_size_bytes=$(lsblk -b -d -n -o SIZE "/dev/$ROOT_DEVICE" 2>/dev/null | awk '{print $1}')
    if [[ "$total_size_bytes" -gt 0 ]]; then
        TOTAL_GB=$((total_size_bytes / 1024 / 1024 / 1024))
    fi
fi
# lsblk 실패 시, df 명령어로 루트 파티션의 용량을 대신 사용
if [ "$TOTAL_GB" -eq 0 ]; then
    TOTAL_GB=$(df -BG / | awk 'NR==2 {print $2}' | sed 's/G//')
fi


# 3. CSV 헤더 작성
echo "hostname,IP,Date,storage_type,local_total,local_usage_p" > "$OUTPUT_FILE"

# 4. /var/log/sa 로그 파일 처리
SA_DIR="/var/log/sa"
if [ -d "$SA_DIR" ]; then
    if ! command -v sadf >/dev/null 2>&1; then
        echo "Error: sysstat (sadf) is not installed."
        exit 1
    fi

    for file in $(ls $SA_DIR/sa[0-9][0-9] 2>/dev/null | sort); do
        # sadf로 디스크 통계를 읽고, 위에서 찾은 루트 디바이스 정보만 필터링
        if sadf -d "$file" -- -d >/dev/null 2>&1; then
            sadf -d -t "$file" -- -d | grep -v "^#" | grep ";$ROOT_DEVICE;" | awk -F';' \
            -v host="$HOSTNAME" \
            -v ip="$IP_ADDR" \
            -v type="$STORAGE_TYPE" \
            -v total="$TOTAL_GB" \
            '{
                # $3=timestamp, $NF=%util
                timestamp = $3
                if (timestamp ~ /^[0-9]+$/) { # RHEL6 같은 epoch timestamp 처리
                    timestamp = strftime("%Y-%m-%d %H:%M:%S", timestamp)
                }
                printf "%s,\"%s\",%s,%s,%s,%.2f\n", host, ip, timestamp, type, total, $NF
            }' >> "$OUTPUT_FILE"
        fi
    done
    echo "Successfully generated CSV: $OUTPUT_FILE"
else
    echo "Error: Directory $SA_DIR not found."
    exit 1
fi