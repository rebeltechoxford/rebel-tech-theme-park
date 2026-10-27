#requires -Version 5.1
<#
.SYNOPSIS
Open official Frontier Toolkit and the two generated upload files.
.DESCRIPTION
Does not sign into Steam, submit anything, install software or change game files.
Run: powershell -NoProfile -File .\scripts\open_toolkit_upload.ps1
#>
$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$buildRoot = Join-Path $projectRoot "build\tmt"
$zip = Join-Path $buildRoot "rt_world_gateway.zip"
$preview = Join-Path $buildRoot "rt_world_gateway_preview.png"

if (-not (Test-Path -LiteralPath $zip)) {
    throw "Cannot find Toolkit ZIP: $zip. Run Blender generator first."
}
if (-not (Test-Path -LiteralPath $preview)) {
    throw "Cannot find Toolkit preview PNG: $preview. Run Blender generator first."
}
Write-Host "REBEL TECH WORLD: Upload candidate prepared on D:"
Write-Host "Toolkit ZIP: $zip"
Write-Host "Preview image (separate upload): $preview"
Write-Host "Name: Rebel Tech World Gateway"
Write-Host "Description: Original futuristic Rebel Tech World entrance sign."
Write-Host "Type: Static scenery"
Write-Host "WARNING: Conversion not yet validated by Frontier. Current FBX was exported from Blender 4.5."
Write-Host "Sign in to Frontier's Toolkit with your own Steam account; never share credentials."
Start-Process -FilePath explorer.exe -ArgumentList ('"' + $buildRoot + '"')
Start-Process "https://thememakers-toolkit.planetcoaster.com/"
Write-Host "Choose Create New Item; upload ZIP and preview PNG separately; monitor conversion result."
