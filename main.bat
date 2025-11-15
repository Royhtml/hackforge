@echo off
setlocal
echo ==============================
echo   Build & Upload to PyPI
echo ==============================

REM --- SET ENVIRONMENT VARIABLES ---
echo Mengatur kredensial PyPI...
set "TWINE_USERNAME=__token__"
set "TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcCJDUzZTAwMjVhLTMxYWEtNGE5MS05YzdkLTgwM2IxNWY1MzhhNQACKlszLCIyMjI2NTRkZi01NDFmLTRhYWEtOWQzMC1hNjk0MmZiN2ZjMzQiXQAABiA0GgG4e294CphqorQC3WfDszyrSRYkNgD6_e9fJMm-gw"
REM --- HAPUS FOLDER DIST SEBELUM BUILD ---
if exist dist (
    echo Menghapus folder dist lama...
    rmdir /s /q dist
)

REM --- BANGUN PAKET (SDIST & WHEEL) ---
echo.
echo Membuat paket Python (sdist & wheel)...
python -m build
if errorlevel 1 (
    echo Gagal membuat paket. Periksa error di atas.
    pause
    exit /b 1
)

REM --- UPLOAD KE PYPI ---
echo.
echo Mengunggah ke PyPI (https://pypi.org/project/lioncix/)...
twine upload dist/* --verbose
if errorlevel 1 (
    echo Upload gagal. Periksa kredensial atau koneksi internet.
    pause
    exit /b 1
)

echo.
echo ======================================
echo ✅ Upload selesai! Cek di PyPI:
echo 🔗 https://pypi.org/project/lioncix/
echo ======================================
pause
endlocal
