#!/usr/bin/env bash
# Salir inmediatamente si un comando falla
set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Recolectar archivos estáticos (CSS/JS)
python manage.py collectstatic --no-input

# Aplicar migraciones de base de datos
python manage.py migrate