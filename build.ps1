# 文件清理工具 - 打包脚本
# 使用此脚本一键打包成exe文件

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "  文件清理工具 - 打包程序" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否安装了 pyinstaller
Write-Host "检查 PyInstaller..." -ForegroundColor Yellow
try {
    $null = pyinstaller --version
    Write-Host "✓ PyInstaller 已安装" -ForegroundColor Green
} catch {
    Write-Host "✗ PyInstaller 未安装，正在安装..." -ForegroundColor Red
    pip install pyinstaller
}

Write-Host ""
Write-Host "开始打包..." -ForegroundColor Yellow
Write-Host ""

# 清理之前的打包文件
if (Test-Path "build") {
    Write-Host "清理旧的 build 目录..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force build
}
if (Test-Path "dist") {
    Write-Host "清理旧的 dist 目录..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force dist
}

# 使用 build.spec 进行打包
Write-Host "执行打包命令..." -ForegroundColor Yellow
pyinstaller build.spec

Write-Host ""
if (Test-Path "dist\文件清理工具.exe") {
    Write-Host "=================================" -ForegroundColor Green
    Write-Host "  ✓ 打包成功！" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "可执行文件位置: dist\文件清理工具.exe" -ForegroundColor Cyan
    Write-Host ""
    
    # 询问是否打开文件夹
    $response = Read-Host "是否打开 dist 文件夹？(Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        explorer.exe "dist"
    }
} else {
    Write-Host "=================================" -ForegroundColor Red
    Write-Host "  ✗ 打包失败！" -ForegroundColor Red
    Write-Host "=================================" -ForegroundColor Red
    Write-Host "请检查上方的错误信息" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
