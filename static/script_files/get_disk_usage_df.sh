#!/bin/bash

export LC_ALL=C

HOSTNAME=$(hostname)
IP_ADDR=$(hostname -I | awk '{print $1}')
[ -z "$IP_ADDR" ] && IP_ADDR="127.0.0.1"
OUTPUT_FILE="/tmp/${HOSTNAME}_disk_usage_df_$(date +%Y%m%d).csv"
# CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

# --- 스크립트 동작 설명 ---
# 이 스크립트는 df 명령어를 사용하여 /, /boot, /home 파티션의 용량을 합산하여 계산합니다.
# 중복된 파티션(예: /home이 /에 포함된 경우)은 한 번만 계산합니다.

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
