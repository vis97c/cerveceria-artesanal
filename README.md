# La cervecería artesanal

Proyecto de la asignatura "Programación orientada a objetos"

El archivo principal de la aplicación es `app.py`. Este organiza todos los modulos de la misma y define las vistas principales.

[https://heavy-lauren-vis97c-a4ac716f.koyeb.app](https://heavy-lauren-vis97c-a4ac716f.koyeb.app)

Una maquina con python >= 3.9.10 es necesaria.

## Prerequisitos

Se requiere instalar las librerías necesarias para correr la aplicación (Una única vez).

```bash
# Install packages
pip install -r requirements.txt
```

## Iniciar aplicación

La aplicación se puede iniciar al ejecutar el archivo app.py, ya sea desde la consola o desde el IDLE.

## Generar ejecutable

```bash
# Pyinstaller
pyinstaller -w -F --add-data \"templates;templates\" --add-data \"static;static\" --add-data \"wkhtmltopdf;wkhtmltopdf\" app.py
```

Para generar un ejecutable se debe ejecutar el siguiente comando:
