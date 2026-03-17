$vanillaDir = "ocr_support_compatibility_pach\gui\vanilla"
$files = Get-ChildItem -Path $vanillaDir -Filter "*.gui" | Sort-Object Name

Write-Host "Files found: $($files.Count)"
Write-Host ("=" * 120)

$results = @()

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $lines = $content -split "`n"
    $lineCount = $lines.Count
    $sizeKB = [math]::Round($file.Length / 1024, 1)

    # 1. Brace count
    $openBraces = ($content.ToCharArray() | Where-Object { $_ -eq '{' }).Count
    $closeBraces = ($content.ToCharArray() | Where-Object { $_ -eq '}' }).Count
    $bracesOK = $openBraces -eq $closeBraces

    # 2. First significant line
    $firstLine = ""
    foreach ($l in $lines) {
        $trimmed = $l.Trim()
        if ($trimmed -and -not $trimmed.StartsWith('#')) {
            $firstLine = $trimmed
            break
        }
    }
    $headerOK = $firstLine -match 'types\s+OCR_PATCH_VANILLA'

    # 3. Visible guard
    $guardCount = ([regex]::Matches($content, "visible\s*=\s*""\[GetVariableSystem\.Exists\(\s*'ocr'\s*\)\]""")).Count

    # 4. Forbidden properties
    $forbiddenProps = @("state = {", "widgetid =", "layer =", "attachto =", "movable =")
    $forbiddenFound = @{}
    foreach ($prop in $forbiddenProps) {
        $matchLines = @()
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -match [regex]::Escape($prop)) {
                $matchLines += ($i + 1)
            }
        }
        if ($matchLines.Count -gt 0) {
            $forbiddenFound[$prop] = $matchLines
        }
    }

    # 5. Unmatched quotes
    $unmatchedQuotes = @()
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $trimmed = $lines[$i].Trim()
        if ($trimmed.StartsWith('#')) { continue }
        $qCount = ($trimmed.ToCharArray() | Where-Object { $_ -eq '"' }).Count
        if ($qCount % 2 -ne 0) {
            $unmatchedQuotes += ($i + 1)
        }
    }

    # 6. Depth check
    $depth = 0
    $negLine = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        foreach ($ch in $lines[$i].ToCharArray()) {
            if ($ch -eq '{') { $depth++ }
            elseif ($ch -eq '}') {
                $depth--
                if ($depth -lt 0 -and $negLine -eq -1) { $negLine = $i + 1 }
            }
        }
    }

    # Build issues list
    $issues = @()
    if (-not $bracesOK) { $issues += "BRACE_MISMATCH($openBraces/$closeBraces)" }
    if ($depth -ne 0) { $issues += "DEPTH=$depth" }
    if ($negLine -ne -1) { $issues += "NEG_DEPTH@L$negLine" }
    if (-not $headerOK) { $issues += "NO_HEADER" }
    if ($guardCount -eq 0) { $issues += "NO_GUARD" }
    $totalForbidden = 0
    foreach ($k in $forbiddenFound.Keys) { $totalForbidden += $forbiddenFound[$k].Count }
    if ($totalForbidden -gt 0) { $issues += "FORBIDDEN($totalForbidden)" }
    if ($unmatchedQuotes.Count -gt 0) { $issues += "QUOTES($($unmatchedQuotes.Count))" }

    $status = if ($issues.Count -eq 0) { "OK" } else { "PROBLEMI" }

    Write-Host "FILE: $($file.Name)"
    Write-Host "  Size: ${sizeKB}KB, Lines: $lineCount"
    Write-Host "  Braces: open=$openBraces close=$closeBraces -> $(if($bracesOK){'OK'}else{'MISMATCH!'})"
    Write-Host "  Final depth: $depth"
    if ($negLine -ne -1) { Write-Host "  WARNING: Negative depth at line $negLine" }
    Write-Host "  Header OCR_PATCH_VANILLA: $(if($headerOK){'YES'}else{'NO!'})"
    Write-Host "  First line: $($firstLine.Substring(0, [math]::Min(80, $firstLine.Length)))"
    Write-Host "  Guard count: $guardCount"
    if ($forbiddenFound.Count -gt 0) {
        Write-Host "  FORBIDDEN properties:"
        foreach ($k in $forbiddenFound.Keys) {
            $lnList = ($forbiddenFound[$k] | Select-Object -First 5) -join ", "
            $extra = if ($forbiddenFound[$k].Count -gt 5) { " ... +$($forbiddenFound[$k].Count - 5) more" } else { "" }
            Write-Host "    '$k' at lines: $lnList$extra"
        }
    } else {
        Write-Host "  Forbidden: NONE (OK)"
    }
    if ($unmatchedQuotes.Count -gt 0) {
        $qList = ($unmatchedQuotes | Select-Object -First 10) -join ", "
        Write-Host "  Unmatched quotes at lines: $qList"
    } else {
        Write-Host "  Unmatched quotes: NONE (OK)"
    }
    Write-Host "  STATUS: $status $(if($issues){' -> ' + ($issues -join '; ')})"
    Write-Host ("-" * 120)

    $results += [PSCustomObject]@{
        File = $file.Name
        SizeKB = $sizeKB
        Lines = $lineCount
        OpenBr = $openBraces
        CloseBr = $closeBraces
        Depth = $depth
        Header = if($headerOK){"Y"}else{"N"}
        Guards = $guardCount
        Forbidden = $totalForbidden
        Quotes = $unmatchedQuotes.Count
        Status = $status
        Issues = ($issues -join "; ")
    }
}

Write-Host "`n`n===== TABELLA RIEPILOGATIVA ====="
$results | Format-Table -AutoSize
Write-Host "Totale: $(($results | Where-Object Status -eq 'OK').Count)/$($results.Count) file OK"
