# Tarea 4 - CC5002 (Desarrollo de Aplicaciones WEB)

Hecho por **Sebastian Bravo**

## 1. Descripción del Proyecto

Esta tarea migra el backend del proyecto de adopción de mascotas de Python/Flask a **Java 17** con el framework **Spring Boot**.

El objetivo principal es implementar una nueva funcionalidad que permite a los usuarios **evaluar los avisos de adopción**.

### Funcionalidades Implementadas

* **Listado de Avisos:** Se despliega una nueva tabla con todos los avisos de adopción.
* **Cálculo de Promedio:** La tabla muestra una columna "Nota" que calcula el **promedio de las evaluaciones** recibidas. Si un aviso no tiene notas, muestra un guion "-".
* **Evaluación Asíncrona:** Al hacer clic en "evaluar", se abre un modal que solicita una nota del 1 al 7.
* **Actualización en Vivo:** La nota se envía al backend de Spring Boot mediante JavaScript, se guarda en la base de datos, y la celda "Nota" en la tabla **se actualiza automáticamente con el nuevo promedio**, sin necesidad de recargar la página.


## 2. Decisiones de Diseño

Siguiendo los requisitos de la tarea, se tomaron las siguientes decisiones:

1.  **Cálculo del Promedio:** En lugar de hacer una consulta SQL compleja para el promedio en cada carga de página, el promedio se calcula en el backend (Java). Se creó un método `getPromedioNotas()` en la entidad `AvisoAdocion` que procesa la lista de notas asociadas. Esto simplifica el controlador y mantiene la lógica de negocio en el modelo.
2.  **API REST para Notas:** Se creó un endpoint API  que recibe la evaluación. Este endpoint se encarga de validar la nota (1-7), guardarla, y devolver el **nuevo promedio calculado** como un string de texto.
3.  **Modal vs. Prompt:** Se reemplazó el `prompt()` nativo de JavaScript por un **modal HTML/CSS** más amigable. Esto mejora la experiencia de usuario y permite un mejor control sobre la validación de entrada.
4.  **Notificación "Toast":** Para una retroalimentación no intrusiva, el `alert()` de "evaluación guardada" se reemplazó por una notificación "toast" que aparece en la parte inferior de la pantalla y se desvanece automáticamente.

## 3. Cómo Ejecutar

1.  **Base de Datos:** Asegurarse de tener la base de datos `tarea2` con el usuario `cc5002` y la contraseña `programacionweb`. Ejecutar los scripts que se han entregado durante las tareas anteriores y esta.
2.  **Configuración:** Verificar que el archivo `src/main/resources/application.properties` tenga las credenciales correctas de la base de datos.
3.  **Ejecutar:** Iniciar la aplicación ejecutando el método `main` en `Tarea4Application.java`.
4.  **Acceder:** Abrir un navegador y visitar `http://localhost:8080`.