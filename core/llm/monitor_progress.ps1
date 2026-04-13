# Live OBLITERATUS Progress Monitor
# Run this in a NEW PowerShell window

$obliteratedDir = "./obliterated"
$hfCacheDir = "$env:USERPROFILE\.cache\huggingface\hub"

Write-Host "`n🔴 LIVE OBLITERATION PROGRESS MONITOR" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to exit`n" -ForegroundColor Gray

$lastSizes = @{}

while($true) {
    Clear-Host
    Write-Host "`n🔴 LIVE OBLITERATION PROGRESS" -ForegroundColor Cyan
    Write-Host "   $(Get-Date -Format 'HH:mm:ss')`n" -ForegroundColor Gray
    
    # Check completed models
    if (Test-Path $obliteratedDir) {
        $completed = Get-ChildItem $obliteratedDir -Directory -ErrorAction SilentlyContinue | Where-Object { 
            (Get-ChildItem $_.FullName -Filter "*.safetensors" -ErrorAction SilentlyContinue).Count -gt 0 
        }
        $zipped = Get-ChildItem $obliteratedDir -Filter "*.zip" -ErrorAction SilentlyContinue
        
        Write-Host "✅ COMPLETED MODELS:" -ForegroundColor Green
        foreach ($model in $completed) {
            $size = (Get-ChildItem $model.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1GB
            $zipStatus = if (Test-Path "$obliteratedDir/$($model.Name).zip") { "📦 Zipped" } else { "" }
            Write-Host "   ✅ $($model.Name) ($([math]::Round($size, 2)) GB) $zipStatus" -ForegroundColor Green
        }
    }
    
    # Check downloading models
    Write-Host "`n📥 DOWNLOADING MODELS:" -ForegroundColor Yellow
    $downloading = Get-ChildItem $hfCacheDir -Directory -ErrorAction SilentlyContinue | Where-Object { 
        $_.Name -like "models--*" -and (Get-ChildItem $_.FullName -Filter "*.lock" -ErrorAction SilentlyContinue).Count -gt 0 
    }
    
    if ($downloading) {
        foreach ($model in $downloading) {
            $name = $model.Name -replace "models--", "" -replace "--", "/"
            $currentSize = (Get-ChildItem $model.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
            
            if (-not $lastSizes.ContainsKey($name)) {
                $lastSizes[$name] = $currentSize
                $speed = 0
            } else {
                $speed = ($currentSize - $lastSizes[$name]) * 1000 / 5  # MB/s over 5 sec refresh
                $lastSizes[$name] = $currentSize
            }
            
            Write-Host "   📥 $name" -ForegroundColor Yellow
            Write-Host "      Downloaded: $([math]::Round($currentSize * 1000, 0)) MB | Speed: $([math]::Round($speed, 2)) MB/s" -ForegroundColor Gray
        }
    } else {
        Write-Host "   (No active downloads)" -ForegroundColor Gray
    }
    
    # Check Python processes
    $pythonProcs = Get-Process -Name python* -ErrorAction SilentlyContinue
    if ($pythonProcs) {
        Write-Host "`n🐍 PYTHON PROCESSES:" -ForegroundColor Magenta
        foreach ($proc in $pythonProcs) {
            $mem = [math]::Round($proc.WorkingSet / 1GB, 2)
            $cpu = [math]::Round($proc.CPU, 1)
            Write-Host "   PID: $($proc.Id) | CPU: ${cpu}s | RAM: ${mem} GB" -ForegroundColor Gray
        }
    }
    
    # Disk space
    $drive = Get-PSDrive -Name (Get-Location).Drive.Name
    Write-Host "`n💾 DISK SPACE:" -ForegroundColor Blue
    Write-Host "   Free: $([math]::Round($drive.Free / 1GB, 1)) GB / Used: $([math]::Round($drive.Used / 1GB, 1)) GB" -ForegroundColor Gray
    
    Start-Sleep -Seconds 5
}
