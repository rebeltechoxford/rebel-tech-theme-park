#requires -Version 5.1
<#
.SYNOPSIS
Read-only inventory of Raven's disk space and likely Blender/Planet Coaster locations.
.DESCRIPTION
Prints results to the current terminal; makes no changes, downloads, or public uploads.
Run from the cloned repo: powershell -NoProfile -File .\scripts\preflight.ps1
#>
$ErrorActionPreference = "Continue"
Write-Host "=== REBEL TECH WORLD / RAVEN PREFLIGHT ==="
Write-Host "Timestamp: $(Get-Date -Format o)"
Write-Host "Working directory: $(Get-Location)"
Write-Host ""

foreach ($letter in @("C", "D")) {
    $drive = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$($letter):'" -ErrorAction SilentlyContinue
    if ($null -eq $drive) {
        Write-Host "$($letter): drive NOT PRESENT"
        continue
    }
    $freeGiB = [Math]::Round(([double]$drive.FreeSpace / 1GB), 2)
    $totalGiB = [Math]::Round(([double]$drive.Size / 1GB), 2)
    Write-Host "$($letter): drive: $freeGiB GiB free / $totalGiB GiB total"
}

Write-Host ""
Write-Host "Expected workspace: D:\RebelTechWorld (not created by this script)"
Write-Host "Workspace exists: $(Test-Path 'D:\RebelTechWorld')"

$blenderPaths = @()
$cmd = Get-Command blender.exe -ErrorAction SilentlyContinue
if ($null -ne $cmd) { $blenderPaths += $cmd.Source }
$blenderRoot = Join-Path $env:ProgramFiles "Blender Foundation"
if (Test-Path $blenderRoot) {
    $blenderPaths += Get-ChildItem -Path $blenderRoot -Recurse -Filter blender.exe -File -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty FullName
}
$blenderPaths = @($blenderPaths | Sort-Object -Unique)
Write-Host ""
if ($blenderPaths.Count -eq 0) {
    Write-Host "Blender: not found in PATH or default install directory (may be elsewhere)."
} else {
    foreach ($candidate in $blenderPaths) {
        Write-Host "Blender found: $candidate"
        try { & $candidate --version | Select-Object -First 1 } catch { Write-Host "Version check failed: $($_.Exception.Message)" }
    }
}
Write-Host ""
Write-Host "Searching common Planet Coaster Steam install locations:"
$steamRoots = @(
    (Join-Path ([Environment]::GetFolderPath("ProgramFilesX86")) "Steam"),
    (Join-Path $env:ProgramFiles "Steam"),
    "D:\SteamLibrary",
    "D:\Steam",
    "C:\SteamLibrary"
)
$found = $false
foreach ($root in $steamRoots) {
    if (-not $root) { continue }
    $game = Join-Path $root "steamapps\common\Planet Coaster"
    if (Test-Path $game) {
        Write-Host "FOUND: $game"
        $found = $true
    }
}
if (-not $found) { Write-Host "Not found in common locations; inspect Steam > Settings > Storage." }
Write-Host ""
$tmtPath = Join-Path $env:USERPROFILE 'Documents\Frontier Developments\Planet Coaster\TMT'
Write-Host "Typical Toolkit import folder: $tmtPath"
Write-Host "TMT folder exists: $(Test-Path $tmtPath)"
Write-Host ""
Write-Host "=== READ-ONLY PREFLIGHT COMPLETE ==="
