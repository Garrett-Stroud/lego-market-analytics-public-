Write-Host "=== Starting LEGO Market Analytics ==="

# Start backend
Start-Process powershell -ArgumentList "cd '$PSScriptRoot'; .\.venv\Scripts\activate; uvicorn dashboard.api.main:app --reload --port 8000"

# Start frontend
Start-Process powershell -ArgumentList "cd '$PSScriptRoot\dashboard\ui'; npm run dev"

# Open browser
Start-Sleep -Seconds 2
Start-Process 'http://localhost:5173'

Write-Host "All systems running!"
