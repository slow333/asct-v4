Write-Host "Stopping ASCT Project Services..."

# 1. Redis 컨테이너 중지
Write-Host "Stopping Redis (Docker)..."
docker stop my-redis 2>$null

# 2. 관련 프로세스 종료 (Django, Celery Worker, Celery Beat 및 해당 창)
# start.ps1에서 실행된 명령어 패턴 정의
$targetPatterns = @(
    "manage.py runserver",
    "celery -A config worker",
    "celery -A config beat"
)

Write-Host "Searching for running processes..."

# 프로세스가 완전히 종료될 때까지 최대 5회 반복 확인
for ($i = 1; $i -le 5; $i++) {
    $foundAny = $false
    
    # 실행 중인 Python 및 PowerShell 프로세스 조회
    try {
        $processes = Get-CimInstance Win32_Process | Where-Object { $_.Name -match "python|powershell|pwsh" }
    } catch {
        $processes = Get-WmiObject Win32_Process | Where-Object { $_.Name -match "python|powershell|pwsh" }
    }

    foreach ($p in $processes) {
        # 현재 실행 중인 stop.ps1 프로세스는 종료 제외
        if ($p.ProcessId -eq $PID) { continue }

        if ($p.CommandLine) {
            foreach ($pattern in $targetPatterns) {
                if ($p.CommandLine -match [regex]::Escape($pattern)) {
                    Write-Host "Attempt ${i}: Terminating PID $($p.ProcessId) ($($p.Name))"
                    taskkill /PID $p.ProcessId /F /T 2>$null
                    $foundAny = $true
                    break 
                }
            }
        }
    }

    if (-not $foundAny) {
        break
    }
    Start-Sleep -Seconds 1
}

# 3. Docker Desktop 종료
Write-Host "Stopping Docker Desktop..."
taskkill /IM "Docker Desktop.exe" /F /T 2>$null

Write-Host "All services stopped."
