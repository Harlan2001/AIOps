[CmdletBinding()]
param(
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($BackendOnly -and $FrontendOnly) {
    throw '-BackendOnly 和 -FrontendOnly 不能同时使用。'
}

$projectRoot = $PSScriptRoot
$frontendDir = Join-Path $projectRoot 'frontend'
$startBackend = -not $FrontendOnly
$startFrontend = -not $BackendOnly
$powerShellExe = (Get-Process -Id $PID).Path

function Assert-Command {
    param(
        [string]$Name,
        [string]$InstallHint
    )

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "未找到 $Name。$InstallHint"
    }
}

if ($startBackend) {
    Assert-Command 'uv' '请先安装 uv：https://docs.astral.sh/uv/getting-started/installation/'
}

if ($startFrontend) {
    $npmCommand = Get-Command 'npm' -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($null -eq $npmCommand) {
        throw '未找到 npm。请先安装 Node.js（包含 npm）。'
    }
    $npmPath = $npmCommand.Path

    if (-not (Test-Path (Join-Path $frontendDir 'node_modules'))) {
        Write-Host '首次启动：正在安装前端依赖...' -ForegroundColor Cyan
        & $npmPath ci --prefix $frontendDir
        if ($LASTEXITCODE -ne 0) {
            throw "前端依赖安装失败，npm 退出码：$LASTEXITCODE"
        }
    }
}

$env:PYTHONIOENCODING = 'utf-8'

if ($startBackend) {
    Write-Host '正在启动 FastAPI 后端...' -ForegroundColor Cyan
    $backendCommand = "`$Host.UI.RawUI.WindowTitle = 'AIOps Backend'; uv run --extra api uvicorn ai_ops.api:app --host 127.0.0.1 --port 8000 --reload"
    Start-Process -FilePath $powerShellExe `
        -WorkingDirectory $projectRoot `
        -ArgumentList '-NoExit', '-Command', $backendCommand
}

if ($startFrontend) {
    Write-Host '正在启动 Vue 前端...' -ForegroundColor Cyan
    $escapedNpmPath = $npmPath.Replace("'", "''")
    $frontendCommand = "`$Host.UI.RawUI.WindowTitle = 'AIOps Frontend'; & '$escapedNpmPath' run dev -- --host 127.0.0.1"
    Start-Process -FilePath $powerShellExe `
        -WorkingDirectory $frontendDir `
        -ArgumentList '-NoExit', '-Command', $frontendCommand
}

Write-Host ''
if ($startBackend) {
    Write-Host '后端 API：http://127.0.0.1:8000/docs' -ForegroundColor Green
}
if ($startFrontend) {
    Write-Host '前端页面：http://127.0.0.1:5173' -ForegroundColor Green
}
Write-Host '请在对应服务窗口按 Ctrl+C 停止服务。' -ForegroundColor Yellow
