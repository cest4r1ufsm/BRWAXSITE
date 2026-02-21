# Generate images.json manifest for the grid
$gridPath = "assets/grid"
$outputPath = Join-Path $gridPath "images.json"

if (Test-Path $gridPath) {
    $images = Get-ChildItem -Path $gridPath -Include *.jpg, *.png, *.webp, *.jpeg, *.gif -Recurse | 
              Where-Object { $_.Name -ne "images.json" } |
              Select-Object -ExpandProperty Name
    
    $json = $images | ConvertTo-Json
    $json | Out-File -FilePath $outputPath -Encoding utf8
    Write-Host "Manifest generated successfully with $($images.Count) images at $outputPath"
} else {
    Write-Error "Directory $gridPath not found."
}
