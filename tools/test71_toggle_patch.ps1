# test71_toggle_patch.ps1 — Test diagnostico Fase 7.1
# Abilita/disabilita la nostra patch nel dlc_load.json per isolare il crash.
#
# USO:
#   .\tools\test71_toggle_patch.ps1 -Mode disable   # rimuove ocr support patch
#   .\tools\test71_toggle_patch.ps1 -Mode enable     # ripristina ocr support patch
#   .\tools\test71_toggle_patch.ps1 -Mode status     # mostra stato attuale

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("disable","enable","status")]
    [string]$Mode
)

$dlcPath = "C:\Users\nemex\OneDrive\Documenti\Paradox Interactive\Crusader Kings III\dlc_load.json"
$bakPath = "$dlcPath.bak_test71"

$withPatch    = '{"enabled_mods":["mod/ck3 italian translate.mod","mod/ugc_2848213069.mod","mod/ocr support compatibilty pach.mod"],"disabled_dlcs":[]}'
$withoutPatch = '{"enabled_mods":["mod/ck3 italian translate.mod","mod/ugc_2848213069.mod"],"disabled_dlcs":[]}'

$current = Get-Content $dlcPath -Raw

switch ($Mode) {
    "status" {
        if ($current -match "ocr support compatibilty pach") {
            Write-Host "STATO: patch ATTIVA (ocr support compatibilty pach.mod presente)"
        } else {
            Write-Host "STATO: patch DISABILITATA (test 7.1 attivo)"
        }
    }
    "disable" {
        if ($current -match "ocr support compatibilty pach") {
            # Salva backup
            Set-Content -Path $bakPath -Value $current -NoNewline
            # Disabilita patch
            Set-Content -Path $dlcPath -Value $withoutPatch -NoNewline
            Write-Host "PATCH DISABILITATA. Avvia CK3 e verifica se il crash persiste."
            Write-Host "  - Se crasha ancora: crash di OCR upstream (non nostra patch)"
            Write-Host "  - Se NON crasha: crash causato dalla nostra patch -> Fase 7.2"
            Write-Host ""
            Write-Host "Per ripristinare: .\tools\test71_toggle_patch.ps1 -Mode enable"
        } else {
            Write-Host "INFO: patch gia' disabilitata"
        }
    }
    "enable" {
        if (Test-Path $bakPath) {
            $bak = Get-Content $bakPath -Raw
            Set-Content -Path $dlcPath -Value $bak -NoNewline
            Remove-Item $bakPath
            Write-Host "PATCH RIPRISTINATA dal backup."
        } else {
            Set-Content -Path $dlcPath -Value $withPatch -NoNewline
            Write-Host "PATCH RIPRISTINATA (configurazione standard)."
        }
    }
}
