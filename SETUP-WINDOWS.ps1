# Palawan Collective Studio - obtain official browser release archives for local preview
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$apps = @(@{Repo='photocraft';Port=8765},@{Repo='vectorcraft';Port=8766},@{Repo='pdfcraft';Port=8768})
$hasPython = [bool](Get-Command py -ErrorAction SilentlyContinue)
if (-not $hasPython -and -not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Install Python 3 and rerun this script.' }
$python = if ($hasPython) {'py'} else {'python'}
foreach ($app in $apps) {
  $name=$app.Repo; $destination=Join-Path $root "editors/$name"
  if (Test-Path (Join-Path $destination 'index.html')) { Write-Host "$name already available.";continue }
  Write-Host "Getting $name official GitHub web release..."
  try {
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/storytold/$name/releases/latest" -Headers @{'User-Agent'='PalawanStudioLocal'}
    $asset = $release.assets | Where-Object { $_.name -match 'web' -and $_.name -match '\.zip$' } | Select-Object -First 1
    if (-not $asset) { Write-Warning "No browser zip found in latest $name release. See README for Rust build alternative.";continue }
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
    $zip=Join-Path $env:TEMP "$name-web-$($release.tag_name).zip"
    Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zip
    Expand-Archive -LiteralPath $zip -DestinationPath $destination -Force
    $idx=Get-ChildItem -Path $destination -Filter 'index.html' -Recurse -File | Select-Object -First 1
    if (-not $idx) { Write-Warning "No index.html in $name release";continue }
    if ($idx.DirectoryName -ne $destination) { $app.WebPath=$idx.DirectoryName } else {$app.WebPath=$destination}
    Write-Host "Ready: $name"
  } catch { Write-Warning "Could not prepare ${name}: $($_.Exception.Message)" }
}
Write-Host "Launching installed web editors and launcher..."
foreach ($app in $apps) {
  $dir=Join-Path $root "editors/$($app.Repo)"
  $idx=Get-ChildItem -Path $dir -Filter index.html -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($idx) {Start-Process -FilePath $python -ArgumentList @('-m','http.server',"$($app.Port)",'--bind','127.0.0.1','--directory',('"'+$idx.DirectoryName+'"')) -WindowStyle Minimized}
}
Start-Process -FilePath $python -ArgumentList @('-m','http.server','8780','--bind','127.0.0.1','--directory',('"'+$root+'"')) -WindowStyle Minimized
Start-Sleep -Seconds 2
Start-Process 'http://127.0.0.1:8780'
Write-Host 'Studio preview: http://127.0.0.1:8780'
