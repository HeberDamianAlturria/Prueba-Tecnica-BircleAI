# Prueba Técnica de BircleAI.

Este proyecto fue realizado con el fin de cumplir con la prueba técnica de BircleAI.

## Requisitos.

Para poder correr este proyecto es necesario tener instalado en tu computadora:

- Una versión de Python 3.9 o superior.

## Decisiones tomadas.

Para la realización de este proyecto, se tomaron las siguientes decisiones:

1. Se utilizará `Groq` para generar una API Key gratuita y poder utilizar el modelo de `Llama 3` como LLM. Las ventajas de utilizar `Groq` es que nos proporciona LLMs de última generación y nos permite hacer uso de ellos de manera gratuita en la nube con una API Key. Además, los tiempos de respuesta son muy rápidos y la documentación es muy completa. Más adelante se explicará cómo crear una API Key en `Groq` y cómo configurarla en el proyecto.

2. Se utilizará `Hugging Face` para poder hacer un embedding de los textos.

3. Se realizarán tests unitarios para comprobar el correcto funcionamiento de las funciones. Para ello utilizaremos `pytest`.

## Crear una API Key en Groq.

Para poder crear una API Key en Groq, debemos seguir los siguientes pasos:

1. Ingresar a la página de [Groq](https://groq.com/).

2. Seleccionar la opción de `Developers` y luego seleccionar la opción de `FREE API Key`.

3. Registrarse en la página de Groq.

4. Una vez registrado, seleccionar la opción de `Create API Key`. Y copiar la API Key generada.

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

5. Crear un archivo `.env` en la raíz del proyecto y agregar las siguientes variables de entorno:

   ```env
   GROQ_API_KEY = "API_KEY"
   ```

   Donde `API_KEY` es la API Key generada en Groq.

## Ejecución.

Para ejecutar el proyecto, puedes ejecutar el siguiente comando en tu terminal:

```bash
uvicorn app.main:app --reload --host=localhost --port=8000
```

Esto iniciará el servidor de desarrollo en la dirección `http://localhost:8000`. Y podrás acceder a la documentación de la API en la dirección `http://localhost:8000/docs`.

## Tests.

Para correr los tests del proyecto, puedes ejecutar el siguiente comando en tu terminal:

```bash
pytest
```

Esto correrá todos los tests del proyecto y mostrará el resultado de los mismos.
