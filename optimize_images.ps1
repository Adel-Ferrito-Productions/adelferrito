# Requires ImageMagick installed and 'magick' in PATH
# Run from project root

$root = "Assets/images"
$sizes = @(400, 800, 1200, 2000)
$watermarkText = "© Adel Ferrito"
$watermarkColor = "rgba(255,255,255,0.5)"
$watermarkFont = "Arial"
$watermarkSize = 24
$mapping = @()

Get-ChildItem -Path $root -Recurse -Include *.jpg | ForEach-Object {
    $img = $_.FullName
    $folder = Split-Path $img -Parent
    $base = [System.IO.Path]::GetFileNameWithoutExtension($img)
    $relFolder = $folder.Substring($root.Length).TrimStart('\/')
    $entry = @{ folder = $relFolder; original = $_.Name; sizes = @() }

    foreach ($w in $sizes) {
        $jpgOut = Join-Path $folder ("${base}_${w}.jpg")
        $webpOut = Join-Path $folder ("${base}_${w}.webp")
        $label = "${w}px"
        # Only create if missing
        if (!(Test-Path $jpgOut)) {
            magick convert "$img" -resize ${w}x -gravity southeast -pointsize $watermarkSize -fill $watermarkColor -font $watermarkFont -annotate +10+10 "$watermarkText" "$jpgOut"
        }
        if (!(Test-Path $webpOut)) {
            magick convert "$img" -resize ${w}x -gravity southeast -pointsize $watermarkSize -fill $watermarkColor -font $watermarkFont -annotate +10+10 "$watermarkText" "$webpOut"
        }
        $entry.sizes += @{ label = $label; jpg = ("${base}_${w}.jpg"); webp = ("${base}_${w}.webp") }
    }
    $mapping += $entry
}

# Output mapping as JSON
$mapping | ConvertTo-Json -Depth 5 | Out-File -Encoding UTF8 "$root/galleries.json"

Write-Host "Image optimization complete. Mapping written to $root/galleries.json" 