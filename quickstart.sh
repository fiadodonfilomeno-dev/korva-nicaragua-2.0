#!/bin/bash
# QUICK START - Korva Nicaragua 2.0

# Cambiar a directorio del proyecto
cd "C:\Users\harif\Desktop\Korva2.0" || exit

# Mostrar banner
echo "======================================"
echo "  KORVA NICARAGUA 2.0"
echo "  Plataforma Social para PyMEs"
echo "======================================"
echo ""

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "[ERROR] Python no está instalado o no está en PATH"
    exit 1
fi

echo "[*] Versión de Python:"
python --version
echo ""

# Verificar dependencias
echo "[*] Verificando dependencias..."
pip list | grep -E "Django|taggit|Pillow|google-generativeai"
echo ""

# Verificar base de datos
echo "[*] Verificando estado de la base de datos..."
if [ -f "db.sqlite3" ]; then
    echo "    [OK] Base de datos existe"
else
    echo "    [!] Creando base de datos..."
    python manage.py migrate
fi
echo ""

# Verificar superusuario
echo "[*] Verificando superusuario..."
python create_admin.py
echo ""

# Mostrar instrucciones
echo "[*] Para iniciar el servidor:"
echo ""
echo "    python manage.py runserver"
echo ""
echo "[*] Acceder a:"
echo "    http://127.0.0.1:8000"
echo ""
echo "[*] Panel de administración:"
echo "    http://127.0.0.1:8000/admin"
echo ""
echo "======================================"
echo "Cuentas de prueba:"
echo "  admin / admin123"
echo "  panaderia_nicaraguena / test1234"
echo "  artesanias_esteli / test1234"
echo "======================================"
echo ""
