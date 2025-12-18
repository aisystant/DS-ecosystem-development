Param(
    [string]$VaultPath = "content",
    [string]$Remote = "origin",
    [string]$Branch = "main"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

try {
    $repoRoot = Resolve-Path "."
    Push-Location $repoRoot

    Write-Host "Checking working tree..."
    $status = git status --porcelain
    if ($status) {
        Write-Host "Uncommitted changes detected — skipping git pull to avoid overwriting." -ForegroundColor Yellow
        Write-Host "You can stage/commit or stash, then rerun for a full sync." -ForegroundColor Yellow
    } else {
        Write-Host "Fetching $Remote/$Branch..."
        git fetch $Remote $Branch | Out-Null

        Write-Host "Pulling with rebase..."
        git pull --rebase $Remote $Branch
    }

    # Nudge Obsidian: create+delete a temp file in the vault to trigger file watchers
    $vaultFull = Join-Path (Get-Location) $VaultPath
    if (-not (Test-Path $vaultFull)) {
        Write-Host "Vault path not found: $vaultFull" -ForegroundColor Yellow
    } else {
        $temp = Join-Path $vaultFull ".vault-refresh.tmp"
        Set-Content -Path $temp -Value ("refreshed at " + (Get-Date).ToString("s")) -Encoding UTF8
        Start-Sleep -Milliseconds 200
        Remove-Item $temp -Force -ErrorAction SilentlyContinue
        Write-Host "Vault refresh nudged for Obsidian at $VaultPath" -ForegroundColor Green
    }

    Write-Host "Sync complete." -ForegroundColor Green
} catch {
    Write-Host ("Error: " + $_.Exception.Message) -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}
