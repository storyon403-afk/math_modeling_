@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo 生成分析报告中的全部图表（报告复现配置）
echo 输出目录：generated_figures
echo ============================================================
python -c "import numpy, pandas, matplotlib, openpyxl" 2>nul
if errorlevel 1 (
    echo 正在安装所需依赖...
    python -m pip install -r requirements.txt
    if errorlevel 1 goto :error
)
python generate_all_figures.py --profile report --output generated_figures
if errorlevel 1 goto :error
echo.
echo 已完成。请打开 generated_figures 文件夹查看图片和 CSV。
pause
exit /b 0
:error
echo.
echo 运行失败，请确认已安装 Python 3.10 或更高版本，并查看上方错误信息。
pause
exit /b 1
