# Prueba Técnica de BircleAI.

Este proyecto fue realizado con el fin de cumplir con la prueba técnica de BircleAI.

## Requisitos.

Para poder correr este proyecto es necesario tener instalado en tu computadora:

- Una versión de Python 3.9 o superior. Se puede descargar desde la página oficial de [Python](https://www.python.org/downloads/). Personalmente, recomiendo tener instalada la versión 3.12.

- Una versión actual de `pip`.

## Decisiones tomadas.

Para la realización de este proyecto, se tomaron las siguientes decisiones:

1. Se utilizará `Groq` para generar una API Key gratuita y poder utilizar el modelo de `Llama 3` como LLM. Las ventajas de utilizar `Groq` es que nos proporciona LLMs de última generación y nos permite hacer uso de ellos de manera gratuita en la nube con una API Key. Además, los tiempos de respuesta son muy rápidos y la documentación es muy completa. Más adelante se explicará cómo crear una API Key en `Groq` y cómo configurarla en el proyecto.

2. Se utilizará `Hugging Face` para poder hacer un embedding de los textos que estarán en el directorio `/data`.

3. Se realizarán tests unitarios para comprobar el correcto funcionamiento de las funciones más importantes del proyecto. Para ello, se utilizará `pytest`.

4. Se configuraron los CORS para permitir el acceso a la API desde cualquier origen. De esa manera, se puede acceder a la API desde cualquier frontend sin problemas.

5. Se limitó para que solamente pueda cargar archivos de texto plano (.txt). Sin embargo, se puede modificar para que pueda cargar otros tipos de archivos simplemente modificando la constante `EXTENSION_FILES_ALLOWED` definida en el archivo `app/constants/llamaindex_constants.py`, aprovechando el hecho de que `SimpleDirectoryReader` permite tratar como texto plano otros tipos de archivos. Para más información, se puede leer la [Documentación de SimpleDirectoryReader](https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader/#supported-file-types).

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

   Y luego, ingresar a la carpeta del proyecto clonado:

   ```bash
   cd Prueba-Tecnica-BircleAI
   ```

2. Estando dentro de la carpeta `Prueba-Tecnica-BircleAI`, debemos crear un entorno virtual. Para ello, puedes ejecutar el siguiente comando en tu terminal:

   - En Windows:

     ```bash
     python -m venv .venv
     ```

   - En Linux o macOS:

     ```bash
     python3 -m venv .venv
     ```

   En caso de no tener instalado el módulo `venv`, puedes instalarlo ejecutando el siguiente comando:

   - En Windows:

     ```bash
     python -m pip install virtualenv
     ```

   - En Linux:

     ```bash
     sudo apt install python3-venv
     ```

     Este comando puede variar dependiendo de la distribución de Linux que estés utilizando. En caso de no funcionar, puedes buscar en la documentación oficial de tu distribución cómo instalar el módulo `venv`.

   - En macOS:

     ```bash
     python3 -m pip install virtualenv
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

   Esto instalará todas las dependencias necesarias para correr el proyecto. Puede tardar unos minutos en instalar todas las dependencias, dependiendo de la velocidad de conexión a internet.

5. Crear un archivo `.env` en la raíz del proyecto y agregar las siguientes variables de entorno:

   ```env
   GROQ_API_KEY = "API_KEY"
   ```

   Donde `API_KEY` es la API Key generada en Groq.

   Es importante que el archivo `.env` creado esté en la raíz del proyecto.

   Podemos crear el archivo `.env` ejecutando el siguiente comando en tu terminal (en la raíz del proyecto):

   ```bash
   echo GROQ_API_KEY="API_KEY" > .env
   ```

   Donde `API_KEY` es la API Key generada en Groq. Dicho comando debería funcionar en Windows (cmd únicamente), en Linux y macOS. En powershell no funciona ya que codifica el archivo en `UTF-16` por defecto y ese formato no es compatible con `os.getenv`.

   Para powershell, el comando sería:

   ```bash
   "GROQ_API_KEY=API_KEY" | Out-File -FilePath .env -Encoding utf8
   ```

   `Dato importante`: Una vez creado el archivo `.env`, debemos reiniciar la consola para que los cambios surtan efecto. Y, cada vez que modifiquemos el archivo `.env`, debemos reiniciar la consola para que los cambios surtan efecto.

## Ejecución.

Ya teniendo el proyecto instalado y configurado, podemos proceder a ejecutarlo.

Para ejecutar el proyecto, puedes ejecutar el siguiente comando en tu terminal:

```bash
uvicorn app.main:app --host=localhost --port=8000
```

Esto iniciará el servidor de desarrollo en la dirección `http://localhost:8000`. Y podrás acceder a la documentación de la API en la dirección `http://localhost:8000/docs`.

Cabe mencionar que el servidor antes de empezar tiene que embeber los textos que se encuentran en el directorio `/data`, lo cual puede tardar cuando se inicia el servidor.

## Tests.

Para correr los tests del proyecto, puedes ejecutar el siguiente comando en tu terminal:

```bash
pytest
```

Esto correrá todos los tests del proyecto y mostrará el resultado de los mismos.

No es necesario tener el servidor corriendo para correr los tests, ni tampoco es necesario tener el `.env` configurado. Los tests mockean todo lo necesario para tener aisladamente las pruebas.
