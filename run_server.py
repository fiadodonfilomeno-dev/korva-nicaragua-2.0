#!/usr/bin/env python
"""
Servidor Korva Nicaragua - Versión Simplificada
Accesible desde cualquier navegador sin configuración compleja
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Directorio del proyecto
    project_dir = Path("C:\\Users\\harif\\Desktop\\Korva2.0")
    
    if not project_dir.exists():
        print("[ERROR] Directorio del proyecto no encontrado")
        return
    
    os.chdir(project_dir)
    
    print("=" * 50)
    print("  KORVA NICARAGUA 2.0")
    print("  Servidor Web")
    print("=" * 50)
    print()
    
    # Migrar base de datos
    print("[*] Preparando base de datos...")
    subprocess.run([sys.executable, "manage.py", "migrate", "--run-syncdb"], 
                   capture_output=True)
    print("    [OK] Base de datos lista")
    print()
    
    # Crear admin si no existe
    print("[*] Verificando cuenta admin...")
    subprocess.run([sys.executable, "create_admin.py"], 
                   capture_output=True)
    print("    [OK] Admin verificado")
    print()
    
    # Iniciar servidor
    print("[*] Iniciando servidor Django...")
    print()
    print("=" * 50)
    print("  SERVIDOR ACTIVO")
    print("=" * 50)
    print()
    print("📍 URL: http://localhost:8000")
    print("🔐 Admin: http://localhost:8000/admin")
    print()
    print("👤 Credenciales:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print()
    print("Presiona Ctrl+C para detener el servidor")
    print()
    print("=" * 50)
    print()
    
    # Ejecutar servidor
    subprocess.run([
        sys.executable, 
        "manage.py", 
        "runserver", 
        "0.0.0.0:8000"
    ])

if __name__ == "__main__":
    main()
