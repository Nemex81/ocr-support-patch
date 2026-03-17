$src = "c:\Users\nemex\OneDrive\Documenti\GitHub\ocr-support-patch\ocr_support_compatibility_pach\gui"
$dst = "C:\Users\nemex\OneDrive\Documenti\Paradox Interactive\Crusader Kings III\mod\ocr_support_compatibility_pach\gui"
$results = @()

# Files modified in Fasi 9-12
$files = @(
    "window_culture.gui",
    "window_military.gui",
    "window_faith.gui",
    "window_inventory.gui",
    "window_county_view.gui",
    "window_army.gui",
    "window_dynasty_house.gui",
    "window_my_realm.gui",
    "window_court.gui"
)

foreach ($name in $files) {
    $srcPath = Join-Path $src $name
    $dstPath = Join-Path $dst $name

    if (-not (Test-Path $srcPath)) {
        $results += "ERRORE: $name non trovato nel workspace"
        continue
    }

    Copy-Item -Path $srcPath -Destination $dstPath -Force

    # Verify hash
    $srcHash = (Get-FileHash -Path $srcPath -Algorithm MD5).Hash
    $dstHash = (Get-FileHash -Path $dstPath -Algorithm MD5).Hash

    if ($srcHash -eq $dstHash) {
        $results += "OK: $name (hash $srcHash)"
    } else {
        $results += "ERRORE HASH: $name src=$srcHash dst=$dstHash"
    }
}

$outFile = "c:\Users\nemex\OneDrive\Documenti\GitHub\ocr-support-patch\tools\_deploy_results.txt"
[System.IO.File]::WriteAllLines($outFile, $results)
