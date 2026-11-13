$ErrorActionPreference = "Continue"
$baseDir = $PSScriptRoot
cd "$baseDir\frontend"
try {
    if (Test-Path ".next") {
        Remove-Item -Recurse -Force ".next" -ErrorAction SilentlyContinue
    }
} catch {}
npm run dev
