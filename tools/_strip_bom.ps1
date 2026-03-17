$gui = "c:\Users\nemex\OneDrive\Documenti\GitHub\ocr-support-patch\ocr_support_compatibility_pach\gui"
$outFile = "c:\Users\nemex\OneDrive\Documenti\GitHub\ocr-support-patch\tools\_bom_results.txt"
$results = @()

foreach ($name in @("window_culture.gui","window_military.gui","window_faith.gui","window_inventory.gui")) {
    $path = Join-Path $gui $name
    $bytes = [System.IO.File]::ReadAllBytes($path)
    $hasBOM = ($bytes.Length -ge 3) -and ($bytes[0] -eq 0xEF) -and ($bytes[1] -eq 0xBB) -and ($bytes[2] -eq 0xBF)

    if ($hasBOM) {
        $noBom = New-Object byte[] ($bytes.Length - 3)
        [Array]::Copy($bytes, 3, $noBom, 0, $bytes.Length - 3)
        [System.IO.File]::WriteAllBytes($path, $noBom)
        $results += "STRIPPED: $name ($($bytes.Length) -> $($noBom.Length))"
    } else {
        $results += "NO-BOM: $name ($($bytes.Length))"
    }
}

$results += ""
$results += "--- VERIFICA ---"

foreach ($name in @("window_culture.gui","window_military.gui","window_faith.gui","window_inventory.gui")) {
    $path = Join-Path $gui $name
    $bytes = [System.IO.File]::ReadAllBytes($path)
    $hasBOM = ($bytes.Length -ge 3) -and ($bytes[0] -eq 0xEF) -and ($bytes[1] -eq 0xBB) -and ($bytes[2] -eq 0xBF)
    if ($hasBOM) {
        $results += "$name : ERRORE BOM PRESENTE ($($bytes.Length) bytes)"
    } else {
        $results += "$name : OK senza BOM ($($bytes.Length) bytes)"
    }
}

[System.IO.File]::WriteAllLines($outFile, $results)
