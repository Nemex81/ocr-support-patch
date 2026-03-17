$filePath = "ocr_support_compatibility_pach\gui\vanilla\army_patch_vanilla.gui"
$lines = Get-Content -Path $filePath -Encoding UTF8
$depth = 0
$prevDepth = 0

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    foreach ($ch in $line.ToCharArray()) {
        if ($ch -eq '{') { $depth++ }
        elseif ($ch -eq '}') { $depth-- }
    }
    # Report when depth changes significantly or goes to specific levels
    if ($depth -ne $prevDepth) {
        # Show lines where depth reaches 1 or 0 (major structural boundaries)
        if ($depth -le 1 -or $prevDepth -le 1 -or $depth -lt 0) {
            $lineNum = $i + 1
            $trimmed = $line.Trim()
            if ($trimmed.Length -gt 80) { $trimmed = $trimmed.Substring(0, 80) + "..." }
            Write-Host "L$lineNum depth: $prevDepth -> $depth | $trimmed"
        }
    }
    $prevDepth = $depth
}
Write-Host "`nFinal depth: $depth"
