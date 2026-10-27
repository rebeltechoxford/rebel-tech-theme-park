#requires -Version 5.1
<# Prepare original-logo PC2 billboards on D:, then stage into the game's discovered UserMedia folder.
   Never modifies game saves, launches the game, or downloads music. #>
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$source=Join-Path $repo 'assets\branding\grid-v1'
$out=Join-Path $repo 'build\pc2\rebel-grid\media'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$logo=Join-Path $source 'rt-circle-original.png'
$hero=Join-Path $source 'rebel-tech-hero-original.jpg'
if((git -C $repo hash-object $logo) -ne '87cca2e4be73de45ad597a76eb40c674bce60b8e'){throw 'RT logo differs from owner upload'}
if((git -C $repo hash-object $hero) -ne 'b05a4cf9efa7e66efed39c8916c3edddb5cd0004'){throw 'Hero differs from owner upload'}
Add-Type -AssemblyName System.Drawing
$logoImage=[System.Drawing.Image]::FromFile($logo)
$signs=@(
    @('RT_GRID_GATE','THE REBEL GRID','REBEL TECH WORLD'),
    @('RT_GRID_FOOD','BYTE BITE','FOOD COURT'),
    @('RT_GRID_CAFE','OVERCLOCK CAFE','COFFEE + DRINKS'),
    @('RT_GRID_TOILETS','REBOOT RESTROOMS','RESTROOMS'),
    @('RT_GRID_SHOP','CACHE & CARRY','REBEL TECH MERCH'),
    @('RT_GRID_RESTAURANT','CORE KITCHEN','DINING'),
    @('RT_GRID_SERVICE','PATCH BAY','GUEST SERVICES')
)
try {
 foreach($s in $signs){
    $bmp=New-Object System.Drawing.Bitmap(1280,720)
    $g=[System.Drawing.Graphics]::FromImage($bmp)
    $fonts=@();$brushes=@()
    try {
        $g.Clear([System.Drawing.ColorTranslator]::FromHtml('#090B10'))
        $g.SmoothingMode=[System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $g.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.TextRenderingHint=[System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
        $red=New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#E10616'))
        $blue=New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#244CFF'))
        $white=New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
        $muted=New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#B8C3D5'))
        $brushes=@($red,$blue,$white,$muted)
        $g.FillRectangle($red,0,0,1280,16);$g.FillRectangle($blue,0,704,1280,16)
        $g.DrawImage($logoImage,56,220,256,256)
        $f1=New-Object System.Drawing.Font('Segoe UI',46,[System.Drawing.FontStyle]::Bold)
        $f2=New-Object System.Drawing.Font('Segoe UI',25,[System.Drawing.FontStyle]::Regular)
        $f3=New-Object System.Drawing.Font('Segoe UI',19,[System.Drawing.FontStyle]::Regular)
        $fonts=@($f1,$f2,$f3)
        $g.DrawString($s[1],$f1,$white,350,264)
        $g.DrawString($s[2],$f2,$muted,354,355)
        $g.FillRectangle($red,354,421,250,6);$g.FillRectangle($blue,615,421,250,6)
        $g.DrawString('CONNECTING. INSTALLING. SOLVING.',$f3,$white,354,473)
        $bmp.Save((Join-Path $out ($s[0]+'.png')),[System.Drawing.Imaging.ImageFormat]::Png)
    } finally {foreach($f in $fonts){$f.Dispose()};foreach($b in $brushes){$b.Dispose()};$g.Dispose();$bmp.Dispose()}
 }
} finally {$logoImage.Dispose()}
Copy-Item -LiteralPath $logo -Destination (Join-Path $out 'RT_GRID_LOGO_ORIGINAL.png') -Force
Copy-Item -LiteralPath $hero -Destination (Join-Path $out 'RT_GRID_HERO_ORIGINAL.jpg') -Force
$media=Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Frontier Developments\Planet Coaster 2\UserMedia'
if(-not(Test-Path $media)){throw 'PC2 UserMedia directory was not found; output remains safely on D:'}
$records=@()
foreach($f in Get-ChildItem $out -File | Where-Object {$_.Extension -in @('.png','.jpg')}){
    $target=Join-Path $media $f.Name
    if(Test-Path $target){
        if((Get-FileHash $target).Hash -ne (Get-FileHash $f.FullName).Hash){
            $bak=Join-Path $repo 'build\backups\pc2\usermedia-before-grid';New-Item -ItemType Directory -Force $bak | Out-Null
            Copy-Item $target (Join-Path $bak ((Get-Date -Format 'yyyyMMddHHmmss')+'-'+$f.Name))
        }
    }
    Copy-Item -LiteralPath $f.FullName -Destination $target -Force
    $h=(Get-FileHash $f.FullName -Algorithm SHA256).Hash
    if($h -ne (Get-FileHash $target -Algorithm SHA256).Hash){throw ('Staging hash failed: '+$f.Name)}
    $records+=@{file=$f.Name;bytes=$f.Length;sha256=$h;status='STAGED_IN_USERMEDIA_NOT_PLACED_IN_GAME'}
}
@{status='SOURCE_ASSETS_VERIFIED_AND_MEDIA_STAGED';music_downloaded=$false;in_game_placement_verified=$false;assets=$records} | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $out 'media_manifest.json') -Encoding UTF8
Write-Output ('GRID_MEDIA_STAGED '+$records.Count+' files; source-image hashes verified; no in-game placement claimed')
