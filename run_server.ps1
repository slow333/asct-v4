# 가상 환경 활성화 및 Django 개발 서버 실행 스크립트

# 가상 환경 활성화 스크립트 경로 (venv 폴더가 프로젝트 루트에 있다고 가정)
$venvPath = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."
    . $venvPath
}

Write-Host "Starting Django Server..."
py .\manage.py runserver
