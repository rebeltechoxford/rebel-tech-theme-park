#requires -Version 5.1
<#
.SYNOPSIS
Build and offline-validate the original Rebel Tech World Gateway scenery.
.DESCRIPTION
Uses local Blender, requires no credentials or Planet Coaster changes.
Produces .blend, .fbx, six-LOD textures, ZIP and PNG preview under build/ (ignored).
Usage: powershell -NoProfile -File .\scripts\build_gateway.ps1
Optional: -BlenderExe "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
#>
param([string]$BlenderExe = "")

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
if(-not $BlenderExe) {
    $found = Get-Command "blender.exe" -ErrorAction SilentlyContinue
    if($found) {
        $BlenderExe = $found.Source
    } else {
        $searchRoot = Join-Path $env:ProgramFiles "Blender Foundation"
        if(Test-Path $searchRoot) {
            $choice = Get-ChildItem -Path $searchRoot -Filter blender.exe -File -Recurse -ErrorAction SilentlyContinue |
                Sort-Object FullName -Descending | Select-Object -First 1
            if($choice) { $BlenderExe = $choice.FullName }
        }
    }
}
if(-not (Test-Path $BlenderExe -PathType Leaf)) { throw "Cannot find Blender executable: $BlenderExe" }
$tmp = Join-Path $repo "build\tmp"
New-Item -ItemType Directory -Path $tmp -Force | Out-Null
$env:TEMP = $tmp
$env:TMP = $tmp

Write-Host "=== Rebel Tech World Gateway Build ==="
Write-Host "Blender: $BlenderExe"
Write-Host "Build folder: $(Join-Path $repo 'build\tmt')"
foreach($file in @('blender\create_gateway.py', 'blender\validate_gateway.py')) {
    Write-Host "Running: $file"
    & $BlenderExe --background --factory-startup --python (Join-Path $repo $file)
    if($LASTEXITCODE -ne 0) { throw "Blender failed ($file), exit code $LASTEXITCODE" }
}
Write-Host ""
Write-Host "Offline checks passed. Frontier web conversion still required."
Write-Host "ZIP: $(Join-Path $repo 'build\tmt\rt_world_gateway.zip')"
Write-Host "Preview: $(Join-Path $repo 'build\tmt\rt_world_gateway_preview.png')"
Write-Host "Validation: $(Join-Path $repo 'build\tmt\rt_world_gateway_validation.json')"
