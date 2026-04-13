# Batch Obliterate All Working Models
# These will work on ANY Windows machine

$workingModels = @(
    @{Name="phi2"; HF="microsoft/phi-2"; Method="advanced"},
    @{Name="tinyllama"; HF="TinyLlama/TinyLlama-1.1B-Chat-v1.0"; Method="basic"},
    @{Name="distilgpt2"; HF="distilbert/distilgpt2"; Method="basic"},
    @{Name="gemma2b"; HF="google/gemma-2-2b"; Method="advanced"},
    @{Name="qwen25-3b"; HF="Qwen/Qwen2.5-3B-Instruct"; Method="advanced"},
    @{Name="smollm2"; HF="HuggingFaceTB/SmolLM2-1.7B-Instruct"; Method="basic"},
    @{Name="stablelm2"; HF="stabilityai/stablelm-2-1_6b"; Method="basic"},
    @{Name="falcon3"; HF="tiiuae/Falcon3-3B-Instruct"; Method="advanced"}
)

Write-Host "`n🔥 BATCH OBLITERATION - ${workingModels.Count} models`n" -ForegroundColor Cyan

foreach ($model in $workingModels) {
    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "📦 Obliterating: $($model.Name)" -ForegroundColor Green
    Write-Host "   HF: $($model.HF)" -ForegroundColor Gray
    Write-Host "   Method: $($model.Method)" -ForegroundColor Gray
    Write-Host "========================================`n" -ForegroundColor Yellow
    
    $outputDir = "./obliterated/$($model.Name)"
    
    obliteratus obliterate $model.HF --method $model.Method --output-dir $outputDir
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $($model.Name) obliterated successfully!" -ForegroundColor Green
        
        # Create portable zip for other machines
        Compress-Archive -Path $outputDir -DestinationPath "./obliterated/$($model.Name).zip" -Force
        Write-Host "   📦 Zipped to: ./obliterated/$($model.Name).zip" -ForegroundColor Cyan
    } else {
        Write-Host "❌ $($model.Name) failed" -ForegroundColor Red
    }
}

Write-Host "`n✅ Batch obliteration complete!" -ForegroundColor Green
Write-Host "`n📁 Obliterated models: ./obliterated/" -ForegroundColor Cyan
Get-ChildItem ./obliterated -Directory | Select-Object Name

Write-Host "`n📦 Portable zips (copy to other machines):" -ForegroundColor Cyan
Get-ChildItem ./obliterated -Filter "*.zip" | Select-Object Name, @{N="Size(MB)";E={[math]::Round($_.Length/1MB, 2)}}
