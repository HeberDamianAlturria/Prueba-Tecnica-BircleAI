# Prueba Técnica de BircleAI.

Este proyecto fue realizado con el fin de cumplir con la prueba técnica de BircleAI.

## Requisitos.

Para poder correr este proyecto es necesario tener instalado en tu computadora:

- Una versión de Python 3.9 o superior.

## Instalación y configuración.

Los pasos para instalar y configurar el proyecto son los siguientes:

1. Clonar el repositorio en tu computadora. Para ello, puedes ejecutar el siguiente comando en tu terminal:

   ```bash
   git clone https://github.com/HeberDamianAlturria/Prueba-Tecnica-BircleAI.git
   ```

2. Crear un entorno virtual. Para ello, puedes ejecutar el siguiente comando en tu terminal:

   ```bash
   python -m venv .venv
   ```

   En caso de no tener instalado el módulo `venv`, puedes instalarlo ejecutando el siguiente comando:

   ```bash
   python -m pip install virtualenv
   ```

   Cabe destacar que el comando anterior creará un entorno virtual en la carpeta `.venv` del proyecto. Este paso solamente debemos hacerlo una vez.

3. Activar el entorno virtual. Para ello, puedes ejecutar el siguiente comando en tu terminal:

   - En Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - En Linux o macOS:

     ```bash
     source .venv/bin/activate
     ```

   Cabe destacar que este paso debemos hacerlo cada vez que deseemos trabajar en el proyecto.

4. Instalar las dependencias del proyecto. Para ello, puedes ejecutar el siguiente comando en tu terminal:

   ```bash
   pip install -r requirements.txt
   ```

   Esto instalará todas las dependencias necesarias para correr el proyecto.

## Ejecución.

Para ejecutar el proyecto, puedes ejecutar el siguiente comando en tu terminal estando posicionados en el directorio `app`:

```bash
python .\main.py
```
