# Tarea 5 - Administración y Seguridad con Spring Boot

## Descripción
Implementación de un panel de administración seguro para la gestión de fotos de avisos de adopción.

## Funcionalidades Agregadas
1. **Seguridad (Spring Security):**
   - Rutas protegidas (`/t5-admin-fotos`, `/mensajes-log`) solo accesibles para el usuario `cc5002`.
   - Login y Logout configurados.

2. **Administración de Fotos:**
   - Galería visual de todas las fotos activas.
   - Eliminación lógica (Soft Delete) con validación de motivo (5-200 caracteres).

3. **Auditoría (Logs):**
   - Registro automático en base de datos de cada eliminación.
   - Vista de historial de logs.

## Cómo Ejecutar
1. Ejecutar los scripts SQL en orden (incluyendo `modificaciones-base-datos.sql`).
2. Configurar `application.properties` con las credenciales de BD.
3. Ejecutar con Maven: `mvn spring-boot:run` o desde el IDE.
4. Acceder a `/t5-admin-fotos` con credenciales: `cc5002` / `examen`.