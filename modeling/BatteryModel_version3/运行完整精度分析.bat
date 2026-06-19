@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo 运行完整精度分析（更细时间步，500次蒙特卡洛）
echo ============================================================
python -c "import numpy, pandas, matplotlib, openpyxl" 2>nul
if errorlevel 1 (
    python -m pip install -r requirements.txt
    if errorlevel 1 goto :error
)
python generate_all_figures.py --profile full --mc-runs 500 --output full_results
if errorlevel 1 goto :error
echo.
echo 已完成。请打开 full_results 文件夹查看结果。
pause
exit /b 0
:error
echo.
echo 运行失败，请查看上方错误信息。
pause
exit /b 1
