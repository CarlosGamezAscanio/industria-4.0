# Run script for PowerShell: crea entorno, instala dependencias y arranca la app
$venv = ".venv"
if (-not (Test-Path $venv)) {
    python -m venv $venv
}

Write-Output "Activando entorno virtual..."
. .venv\Scripts\Activate.ps1

Write-Output "Actualizando pip e instalando dependencias..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Output "Iniciando la aplicación..."
python main.py