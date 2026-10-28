#requires -Version 5.1
# Read-only screenshot of Planet Coaster 2 foreground window, resized for inspection.
# Does not launch or control game; will fail closed if game is not foreground.
param([int]$Width = 1280, [int]$Height = 720)
$ErrorActionPreference = 'Stop'
$repo='D:\RebelTechWorld\rebel-tech-theme-park'
$py='D:\RebelTechWorld\.venv\Scripts\python.exe'
& $py "$repo\scripts\pc2_desktop_control.py" capture
if($LASTEXITCODE -ne 0){throw 'Game capture failed'}
Add-Type -AssemblyName System.Drawing
$p=Join-Path $repo 'build\probe'
$src=[System.Drawing.Image]::FromFile((Join-Path $p 'pc2-current.png'))
try {
    $dest=New-Object System.Drawing.Bitmap($Width,$Height)
    try {
        $g=[System.Drawing.Graphics]::FromImage($dest)
        try {
            $g.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $g.DrawImage($src,0,0,$Width,$Height)
        } finally {$g.Dispose()}
        $dest.Save((Join-Path $p 'pc2-preview.jpg'),[System.Drawing.Imaging.ImageFormat]::Jpeg)
    } finally {$dest.Dispose()}
} finally {$src.Dispose()}
Write-Output 'PC2_PREVIEW_READY'
