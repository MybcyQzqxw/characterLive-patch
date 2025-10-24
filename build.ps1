# characterLive-patch Build Script
# Use this script to build the exe file with one click

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "  characterLive-patch Builder" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check and activate conda environment
Write-Host "Checking conda environment..." -ForegroundColor Yellow
$condaEnvName = "characterLive-patch"

try {
    # Check if conda is available
    $condaInfo = conda info --envs 2>&1
    
    if ($condaInfo -match $condaEnvName) {
        Write-Host "✓ Found conda environment: $condaEnvName" -ForegroundColor Green
        Write-Host "Activating environment..." -ForegroundColor Yellow
        
        # Activate conda environment
        conda activate $condaEnvName
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Environment activated successfully" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to activate environment" -ForegroundColor Red
            Write-Host "Please run: conda activate $condaEnvName" -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit 1
        }
    } else {
        Write-Host "✗ Conda environment '$condaEnvName' not found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please create the environment first:" -ForegroundColor Yellow
        Write-Host "  conda create -n $condaEnvName python=3.9" -ForegroundColor Cyan
        Write-Host "  conda activate $condaEnvName" -ForegroundColor Cyan
        Write-Host "  pip install pyinstaller" -ForegroundColor Cyan
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "✗ Conda not found or error occurred" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please make sure conda is installed and in your PATH" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if PyInstaller is installed
Write-Host "Checking PyInstaller..." -ForegroundColor Yellow
try {
    $null = pyinstaller --version
    Write-Host "✓ PyInstaller installed" -ForegroundColor Green
}
catch {
    Write-Host "✗ PyInstaller not found, installing..." -ForegroundColor Red
    pip install pyinstaller
}

Write-Host ""
Write-Host "Starting build process..." -ForegroundColor Yellow
Write-Host ""

# Clean previous build files
if (Test-Path "build") {
    Write-Host "Cleaning old build directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force build
}
if (Test-Path "dist") {
    Write-Host "Cleaning old dist directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force dist
}

# Build using build.spec
Write-Host "Executing build command..." -ForegroundColor Yellow
pyinstaller build.spec

Write-Host ""
if (Test-Path "dist\characterLive-patch.exe") {
    Write-Host "=================================" -ForegroundColor Green
    Write-Host "  ✓ Build successful!" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: dist\characterLive-patch.exe" -ForegroundColor Cyan
    Write-Host ""
    
    # Ask to open dist folder
    $response = Read-Host "Open dist folder? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        explorer.exe "dist"
    }
}
else {
    Write-Host "=================================" -ForegroundColor Red
    Write-Host "  ✗ Build failed!" -ForegroundColor Red
    Write-Host "=================================" -ForegroundColor Red
    Write-Host "Please check the error messages above" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
