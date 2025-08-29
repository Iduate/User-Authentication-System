# README to Word Document Exporter PowerShell Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " README to Word Document Exporter" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Converting README.md to Word document..." -ForegroundColor Yellow
Write-Host ""

try {
    & "C:/Users/Hp/AppData/Local/Microsoft/WindowsApps/python3.11.exe" "export_readme_to_word.py"
    Write-Host ""
    Write-Host "✅ Export completed successfully!" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "❌ Error occurred during export:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
