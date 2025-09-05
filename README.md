# Tarea 1 

- Nombre: Sebastian Bravo
- Curso: CC5002 - Desarrollo de Aplicaciones Web
- Fecha de Entrega: 5 de septiembre de 2025

## Decisiones de Implementación

### 1. Arquitectura del Proyecto
- Se optó por un único archivo HTML para simplificar la entrega y evaluación
- Todo el CSS y JavaScript está incluido en el mismo archivo para facilitar la portabilidad

### 2. Navegación entre Secciones
- Implementé un sistema de navegación mediante la función `showSection()` que muestra/oculta secciones
- Todas las secciones están presentes en el DOM pero ocultas con la clase `hidden`

### 3. Validaciones de Formulario
- Todas las validaciones se implementaron en JavaScript como se solicitó
- No se utilizó el atributo `required` de HTML5 para cumplir con los requisitos
- Las validaciones incluyen:
  - Campos obligatorios
  - Longitudes mínimas y máximas
  - Formato de email
  - Formato de teléfono chileno (+569 12345678)
  - Fechas posteriores a la hora actual más 3 horas

### 4. Manejo de Imágenes
- Para las imágenes se decargó imagenes de la web en formato jgp y se añadió usando img. Estan en el github
- Solamente implemente en la portada imagenes, aun asi se pueden agregar en los avisos.



