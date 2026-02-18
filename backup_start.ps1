Write-Host "Starting ASCT Project Services..."

# 스크립트 실행 위치로 작업 디렉토리 설정 (모듈 경로 문제 해결)
Set-Location $PSScriptRoot

# 0. Docker Desktop 실행 확인 및 자동 실행
if (-not (Get-Process "Docker Desktop" -ErrorAction SilentlyContinue)) {
    Write-Host "Docker Desktop is not running. Starting..."
    $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if (Test-Path $dockerPath) {
        Start-Process $dockerPath
    } else {
        Write-Warning "Docker Desktop path not found. Please ensure Docker is running."
    }
}

# Docker 데몬 준비 대기 (Redis 실행 전 필수)
Write-Host "Waiting for Docker Daemon to be ready..."
while ($true) {
    docker info | Out-Null 2>&1
    if ($?) { break }
    Write-Host "Waiting for Docker..."
    Start-Sleep -Seconds 3
}

# 가상환경 활성화 스크립트 경로 (프로젝트 구조에 맞게 조정 필요)
$venvPath = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"

# 1. Redis 실행 (Docker 컨테이너 이름이 'my-redis'라고 가정 - 문서 참조)
Write-Host "Checking Redis (Docker)..."
# my-redis 컨테이너 존재 여부 확인 (없으면 생성 및 실행, 있으면 시작)
$redisContainer = docker ps -a -q -f "name=^my-redis$"
if (-not $redisContainer) {
    Write-Host "Container 'my-redis' not found. Creating and starting..."
    docker run --name my-redis -p 6379:6379 -d redis redis-server --protected-mode no
    # docker run --name my-redis -p 6379:6379 -d redis redis-server --bind 0.0.0.0 --protected-mode no
} else {
    Write-Host "Starting Redis (Docker)..."
    docker start my-redis
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
    Write-Warning "Could not confirm Redis is ready. Continuing, but Celery might fail to connect."
}

# 3. Celery Worker (새 창에서 실행 - Windows 환경을 위한 eventlet 옵션 포함)
Write-Host "Launching Celery Worker (Hidden)..."
Start-Process powershell -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "Set-Location '$PSScriptRoot'; $env:SERVICE_TYPE='worker'; . '$venvPath'; celery -A config worker -l info -P eventlet -f 'celery_worker.log'" -WindowStyle Hidden -WorkingDirectory $PSScriptRoot

# 로그 확인을 위한 대기
Write-Host "Waiting for Celery Worker to initialize..."
Start-Sleep -Seconds 5

if (Test-Path "celery_worker.log") {
    Write-Host "--- Celery Worker Log (Last 10 lines) ---" -ForegroundColor Cyan
    Get-Content "celery_worker.log" -Tail 10
    Write-Host "-----------------------------------------" -ForegroundColor Cyan
}

# 4. Celery Beat (새 창에서 실행)
Write-Host "Launching Celery Beat (Hidden)..."
Start-Process powershell -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "Set-Location '$PSScriptRoot'; $env:SERVICE_TYPE='beat'; . '$venvPath'; celery -A config beat -l info -f 'celery_beat.log'" -WindowStyle Hidden -WorkingDirectory $PSScriptRoot

# 로그 확인을 위한 대기
Write-Host "Waiting for Celery Beat to initialize..."
Start-Sleep -Seconds 5

if (Test-Path "celery_beat.log") {
    Write-Host "--- Celery Beat Log (Last 10 lines) ---" -ForegroundColor Cyan
    Get-Content "celery_beat.log" -Tail 10
    Write-Host "---------------------------------------" -ForegroundColor Cyan
}

# 2. Django Runserver (현재 창에서 실행)
Write-Host "Launching Django Runserver..."
Write-Host "All background services started. Running Django..."
. $venvPath
$env:SERVICE_TYPE='web'
python manage.py runserver 0.0.0.0:8000
