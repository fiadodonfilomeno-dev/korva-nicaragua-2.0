@echo off
REM Script para ejecutar Korva Nicaragua con acceso público

echo.
echo ====================================
echo   KORVA NICARAGUA 2.0
echo   Servidor con Acceso Público
echo ====================================
echo.

cd /d "C:\Users\harif\AppData\Local\Temp\opencode\korva_deploy"

REM Verificar si ngrok está instalado
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] ngrok no está instalado
    echo [*] Instalando ngrok...
    pip install pyngrok
)

REM Iniciar servidor Django
echo [*] Iniciando servidor Django...
start /b python manage.py runserver 127.0.0.1:8080

REM Esperar a que el servidor inicie
timeout /t 3 /nobreak

REM Crear túnel público con ngrok
echo [*] Creando túnel público...
python -c "from pyngrok import ngrok; url = ngrok.connect(8080); print('[SUCCESS] URL PÚBLICA:', url)"

echo.
echo ====================================
echo   SERVIDOR KORVA ACTIVO
echo ====================================
echo.
echo Cuentas de prueba:
echo   admin / admin123
echo   panaderia_nicaraguena / test1234
echo.
echo Presiona Ctrl+C para detener
echo ====================================
echo.

pause
