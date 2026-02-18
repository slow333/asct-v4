# 실행 순서
# 1. venv 실행 --> 이 상태에서 start.ps1을 실행
Write-Host "Starting ASCT Project Services..."

# 스크립트 실행 위치로 작업 디렉토리 설정 (모듈 경로 문제 해결)
Set-Location $PSScriptRoot

# 가상환경 활성화 스크립트 경로 (프로젝트 구조에 맞게 조정 필요)
$venvPath = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"

# 기존 로그 파일 백업 (logs_backup 폴더로 이동)
$backupDir = Join-Path $PSScriptRoot "logs_backup"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}
$logFiles = @("celery_worker.log", "celery_beat.log")
foreach ($file in $logFiles) {
    if (Test-Path $file) {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Move-Item -Path $file -Destination (Join-Path $backupDir "$file.$timestamp") -Force
        Write-Host "Backed up old log: $file" -ForegroundColor Gray
    }
}

# 1. Redis 컨테이너 실행 (Docker)
Write-Host "Checking Redis container..."
$redisContainer = docker ps -a -q -f "name=^my-redis$"
if (-not $redisContainer) {
    Write-Host "Creating and starting with protected-mode disabled..."
    # 외부 접속을 허용하기 위해 protected-mode를 비활성화합니다.
    docker run --name my-redis -p 6379:6379 -d redis redis-server --protected-mode no
} else {
    $redisStatus = docker ps -q -f "name=^my-redis$"
    if (-not $redisStatus) {
        Write-Host "Starting existing Redis container..."
        docker start my-redis
    } else {
        Write-Host "my-redis is already running."
    }
}

# Redis가 준비될 때까지 대기 (Celery 연결 오류 방지)
Write-Host "Waiting for Redis to be ready..."
$redisReady = $false
for ($i = 0; $i -lt 15; $i++) { # 최대 30초 대기
    # 2>$null을 사용하여 redis-cli를 찾을 수 없다는 오류 메시지 숨김
    $pingResult = docker exec my-redis redis-cli ping 2>$null
    if ($pingResult -like "*PONG*") {
        Write-Host "Redis is ready." -ForegroundColor Green
        $redisReady = $true
        break
    }
    Write-Host "Waiting for Redis... (attempt $($i+1))"
    Start-Sleep -Seconds 2
}
if (-not $redisReady) {
    Write-Warning "Could not confirm Redis is ready. Celery might fail to connect. Exiting."
    exit 1
}

# 프로세스 상태 확인을 위한 함수
function Check-ProcessStatus {
    param(
        [string]$logFile,
        [string]$processName,
        [string]$successString
    )
    
    Write-Host "Verifying $processName startup..."
    Start-Sleep -Seconds 7 # 프로세스가 시작되고 로그를 남길 시간을 줍니다.

    if (-not (Test-Path $logFile)) {
        Write-Error "$processName log file ('$logFile') not found. Startup failed."
        return $false
    }

    $logContent = Get-Content $logFile -Tail 20
    Write-Host "--- Last 10 lines of $processName log ---" -ForegroundColor Cyan
    $logContent | Select-Object -Last 10
    Write-Host "-------------------------------------------" -ForegroundColor Cyan

    if ($logContent -match $successString) {
        Write-Host "$processName appears to be running successfully." -ForegroundColor Green
        return $true
    }

    if ($logContent -match "ERROR") {
        Write-Error "$processName started with errors. Please check '$logFile' for details."
        return $false
    }

    Write-Warning "$processName might not have started correctly. Success message not found in log. Please check '$logFile'."
    return $false
}

# 2. Celery Worker (기존 창에서 실행)
Write-Host "Launching Celery Worker..."
$workerLog = "celery_worker.log"
Start-Process powershell -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "Set-Location '$PSScriptRoot'; . '$venvPath'; celery -A config worker -l info -P eventlet -f '$workerLog'" -WindowStyle Hidden -WorkingDirectory $PSScriptRoot
Check-ProcessStatus -logFile $workerLog -processName "Celery Worker" -successString "ready"

# 3. Celery Beat (기존 창에서 실행)
Write-Host "Launching Celery Beat..."
$beatLog = "celery_beat.log"
Start-Process powershell -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "Set-Location '$PSScriptRoot'; . '$venvPath'; celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler '$beatLog'" -WindowStyle Hidden -WorkingDirectory $PSScriptRoot
Check-ProcessStatus -logFile $beatLog -processName "Celery Beat" -successString "beat: Starting..."


# 4. Django Runserver (현재 창에서 실행)
Write-Host "All background services launched. Starting Django Runserver..."
Write-Host "If the following lines show the Django development server starting, the web service is running." -ForegroundColor Yellow
. $venvPath
python manage.py runserver 0.0.0.0:8000
