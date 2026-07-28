@echo off
REM Script para iniciar Korva Nicaragua 2.0

echo.
echo ====================================
echo   KORVA NICARAGUA 2.0
echo   Iniciando Servidor...
echo ====================================
echo.

cd /d "%~dp0"

echo [*] Verificando conexion a base de datos...
python manage.py migrate --run-syncdb > nul 2>&1

echo [*] Iniciando servidor Django...
echo.
echo ====================================
echo   SERVIDOR ACTIVO
echo ====================================
echo.
echo URL: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin
echo.
echo Cuentas de prueba:
echo   admin / admin123
echo   panaderia_nicaraguena / test1234
echo.
echo Presiona Ctrl+C para detener el servidor
echo ====================================
echo.

python manage.py runserver 127.0.0.1:8000

pause
