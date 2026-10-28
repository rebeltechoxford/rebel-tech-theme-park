#requires -Version 5.1
param([Parameter(Mandatory=$true)][string]$Tag)
$ErrorActionPreference='Stop'
if($Tag -notmatch '^[A-Za-z0-9_-]+$'){throw 'Invalid capture tag'}
$repo=Split-Path $PSScriptRoot -Parent
$out=Join-Path $repo 'build\probe\path-repair'
New-Item -ItemType Directory -Force -Path $out|Out-Null
$target=Join-Path $out ($Tag+'.jpg')
if(Test-Path $target){throw 'Capture tags must be unique'}
# A fresh verified game capture, copied into an isolated evidence file.
& 'D:\RebelTechWorld\.venv\Scripts\python.exe' (Join-Path $PSScriptRoot 'pc2_desktop_control.py') capture
if($LASTEXITCODE -ne 0){throw 'Capture failed'}
Add-Type -AssemblyName System.Drawing
$src=[System.Drawing.Image]::FromFile((Join-Path $repo 'build\probe\pc2-current.png'))
try {
  $bmp=New-Object System.Drawing.Bitmap(1440,810)
  try {
    $g=[System.Drawing.Graphics]::FromImage($bmp)
    try {$g.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$g.DrawImage($src,0,0,1440,810)} finally {$g.Dispose()}
    $bmp.Save($target,[System.Drawing.Imaging.ImageFormat]::Jpeg)
  } finally {$bmp.Dispose()}
} finally {$src.Dispose()}
Write-Output ('ISOLATED_CAPTURE '+$target)
