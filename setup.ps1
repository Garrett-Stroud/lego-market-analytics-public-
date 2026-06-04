Write-Host "=== LEGO Market Analytics Setup ==="

# ------------------------------------------------------------
# 1. Create virtual environment
# ------------------------------------------------------------
Write-Host "[1/5] Creating virtual environment (if missing)..."
if (!(Test-Path ".venv")) {
    python -m venv .venv
}

# ------------------------------------------------------------
# 2. Activate venv
# ------------------------------------------------------------
Write-Host "[2/5] Activating virtual environment..."
.\.venv\Scripts\activate

# ------------------------------------------------------------
# 3. Install Python dependencies
# ------------------------------------------------------------
Write-Host "[3/5] Installing Python dependencies..."
pip install -r requirements.txt

# ------------------------------------------------------------
# 4. Install UI dependencies
# ------------------------------------------------------------
Write-Host "[4/5] Installing UI dependencies..."
cd dashboard/ui
npm install
cd ../..

# ------------------------------------------------------------
# 5. Initialize database + insert demo opportunity
# ------------------------------------------------------------
Write-Host "[5/5] Initializing database with demo data..."
python init_db.py

Write-Host "`nSetup complete! You can now run start-dev.ps1"
