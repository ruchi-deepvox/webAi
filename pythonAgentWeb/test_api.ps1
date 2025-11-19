# PowerShell script to test Unified Voice Agent API

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Testing Unified Voice Agent API" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Health Check:" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get
    $response | ConvertTo-Json -Depth 10
    Write-Host "✓ Health check passed" -ForegroundColor Green
} catch {
    Write-Host "✗ Health check failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Get Config
Write-Host "2. API Configuration:" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/config" -Method Get
    $response | ConvertTo-Json -Depth 10
    Write-Host "✓ Config retrieved" -ForegroundColor Green
} catch {
    Write-Host "✗ Config failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Connect to Agent
Write-Host "3. Connect to Agent (Main Test):" -ForegroundColor Yellow
try {
    $body = @{
        user_name = "Test User"
        user_id = "test-123"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/connect" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    $response | ConvertTo-Json -Depth 10
    Write-Host "✓ Connection successful" -ForegroundColor Green
    Write-Host "  Token: $($response.token.Substring(0,20))..." -ForegroundColor Gray
    Write-Host "  Room: $($response.room)" -ForegroundColor Gray
    Write-Host "  URL: $($response.url)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Connection failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 4: List Rooms
Write-Host "4. List Active Rooms:" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/rooms" -Method Get
    $response | ConvertTo-Json -Depth 10
    Write-Host "✓ Rooms listed" -ForegroundColor Green
} catch {
    Write-Host "✗ List rooms failed: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "All tests completed!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

