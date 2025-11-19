# Add Windows Firewall Rule for Voice Agent API Server
# Run this script as Administrator

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Voice Agent - Firewall Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "Then run this script again." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "Adding firewall rule for port 8000..." -ForegroundColor Yellow

# Remove existing rule if present
netsh advfirewall firewall delete rule name="Python API Server" 2>$null

# Add new rule
$result = netsh advfirewall firewall add rule name="Python API Server" dir=in action=allow protocol=TCP localport=8000

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Firewall rule added." -ForegroundColor Green
    Write-Host ""
    Write-Host "Your API server is now accessible from other devices at:" -ForegroundColor Cyan
    Write-Host "http://192.168.0.102:8000" -ForegroundColor White
    Write-Host ""
    Write-Host "You can now use the voice agent from any device on your network!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "ERROR: Failed to add firewall rule." -ForegroundColor Red
    Write-Host "Please add it manually through Windows Firewall settings." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

