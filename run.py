#!/usr/bin/env python3
"""
Script Python simplificado para instalar dependencias y ejecutar RAC Assistant
Compatible con Windows
"""

import subprocess
import sys
import os

def print_status(message, status="INFO"):
    """Imprimir mensaje con status"""
    status_colors = {
        "OK": "[OK] ",
        "ERROR": "[ERROR] ",
        "WARNING": "[WARNING] ",
        "INFO": "[INFO] "
    }
    print(f"{status_colors.get(status, '[INFO] ')}{message}")

def run_command(command, description=""):
    """Ejecutar comando y manejar errores"""
    try:
        if description:
            print_status(f"Ejecutando: {description}")
        
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    """Función principal"""
    print("=" * 60)
    print("RAC Assistant - Optimización de Procesos con IA")
    print("Modelos: Local, Hugging Face, OpenAI, DeepSeek")
    print("=" * 60)
    
    # Verificar Python
    print_status("Verificando Python...")
    success, output = run_command("python --version")
    if success:
        print_status(f"Python encontrado: {output.strip()}", "OK")
    else:
        print_status("Python no esta instalado o no esta en el PATH", "ERROR")
        print_status("Instala Python desde: https://www.python.org/downloads/")
        input("Presiona Enter para salir...")
        return
    
    # Verificar pip
    print_status("Verificando pip...")
    success, output = run_command("pip --version")
    if success:
        print_status("pip encontrado", "OK")
    else:
        print_status("pip no esta disponible", "ERROR")
        input("Presiona Enter para salir...")
        return
    
    # Instalar dependencias
    print_status("Instalando dependencias...")
    print_status("Esto puede tomar unos minutos...")
    
    # Verificar si requirements.txt existe
    if os.path.exists("requirements.txt"):
        success, output = run_command("pip install -r requirements.txt")
        if success:
            print_status("Dependencias instaladas correctamente", "OK")
        else:
            print_status("Error al instalar desde requirements.txt, instalando manualmente", "WARNING")
            install_manual()
    else:
        print_status("requirements.txt no encontrado, instalando manualmente", "WARNING")
        install_manual()
    
    # Verificar archivos
    print_status("Verificando archivos...")
    required_files = ["app.py", "config.py", "utils.py", "analysis_models.py", "ui_components.py"]
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print_status(f"{file} encontrado", "OK")
        else:
            print_status(f"{file} no encontrado", "WARNING")
            missing_files.append(file)
    
    if missing_files:
        print_status(f"Archivos faltantes: {', '.join(missing_files)}", "WARNING")
        print_status("La aplicacion puede no funcionar correctamente", "WARNING")
    
    # Ejecutar aplicación
    print_status("Iniciando RAC Assistant...")
    print_status("La aplicacion se abrira en tu navegador")
    print_status("URL: http://localhost:8501")
    print_status("Modelos disponibles:")
    print_status("- Local (Recomendado para pruebas)")
    print_status("- Hugging Face (Online)")
    print_status("- OpenAI (Requiere API Key)")
    print_status("- DeepSeek (Requiere API Key, más económico)")
    print_status("Para detener: Ctrl+C")
    print("=" * 60)
    
    try:
        subprocess.run(["python", "-m", "streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError:
        print_status("Error al ejecutar la aplicacion", "ERROR")
        print_status("Verifica que todas las dependencias esten instaladas", "ERROR")
    except KeyboardInterrupt:
        print_status("Aplicacion detenida por el usuario", "INFO")
    
    print_status("Gracias por usar RAC Assistant!", "OK")
    input("Presiona Enter para salir...")

def install_manual():
    """Instalar dependencias una por una"""
    packages = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
        "xlrd>=2.0.0",
        "requests>=2.28.0",
        "openai==0.28"
    ]
    
    for package in packages:
        print_status(f"Instalando {package}...")
        success, output = run_command(f"pip install {package}")
        if success:
            print_status(f"{package} instalado", "OK")
        else:
            print_status(f"Error instalando {package}", "WARNING")

if __name__ == "__main__":
    main()
