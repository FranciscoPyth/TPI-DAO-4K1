
# Proyecto de Gestión de Préstamos de Libros

Este proyecto permite gestionar los préstamos de libros y genera reportes en formato PDF de los préstamos vencidos, libros más prestados, entre otros. A continuación se describen los pasos necesarios para configurar y ejecutar el proyecto correctamente.

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente:

- **Python 3.x**: Puedes descargarlo desde [aquí](https://www.python.org/downloads/).
- **pip**: Herramienta para gestionar paquetes de Python. Generalmente viene instalado con Python.

## Configuración del Entorno

Para evitar conflictos con las dependencias de tu sistema, se recomienda crear un entorno virtual para este proyecto. Sigue los pasos a continuación:

### 1. Crear el Entorno Virtual

En la terminal, navega hasta la carpeta raíz del proyecto y ejecuta el siguiente comando para crear un entorno virtual:

```bash
python -m venv env
```

Este comando creará una carpeta llamada `env` que contendrá el entorno virtual.

### 2. Activar el Entorno Virtual

Una vez creado el entorno virtual, debes activarlo. Los comandos para hacerlo dependen del sistema operativo que estés utilizando.

- En **Windows**:

    ```bash
    .\env\Scripts\activate
    ```

- En **macOS/Linux**:

    ```bash
    source env/bin/activate
    ```

Al activar el entorno, tu terminal debería mostrar el nombre del entorno (`env`) al principio de la línea de comandos.

### 3. Instalar Dependencias

Con el entorno virtual activado, ahora puedes instalar todas las dependencias necesarias. Para ello, ejecuta el siguiente comando:

```bash
pip install -r requirements.txt
```

Este comando instalará todos los paquetes listados en el archivo `requirements.txt`.

## Configuración Adicional

En algunos casos, como el archivo **LibraryApp.py** en el frontend, puede ser necesario modificar algunas rutas absolutas para evitar conflictos. Revisa y actualiza las rutas de los archivos o directorios que puedan estar utilizando rutas absolutas en el código. Asegúrate de que todas las rutas sean relativas o se ajusten correctamente a tu estructura de carpetas local.

## Ejecución del Proyecto

Una vez que hayas configurado el entorno y las dependencias, puedes ejecutar el proyecto de la siguiente manera:

### 1. Ejecutar el Script Principal

En la terminal, estando en el entorno virtual y en la carpeta raíz del proyecto, ejecuta el archivo principal `Main.py` con el siguiente comando:

```bash
python Main.py
```

Esto iniciará la ejecución del programa.

## Notas Adicionales

- Si encuentras algún error relacionado con las rutas de los archivos, revisa las configuraciones y asegúrate de que las rutas estén correctamente definidas.
- Si alguna dependencia falla al instalarse, asegúrate de tener la versión adecuada de Python y pip. Si el problema persiste, intenta actualizar pip con el comando `pip install --upgrade pip`.

## Contribución

Si deseas contribuir a este proyecto, por favor realiza un *fork* del repositorio, crea una rama con tu funcionalidad y abre un *pull request* explicando los cambios realizados.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
